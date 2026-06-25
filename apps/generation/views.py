from __future__ import annotations

import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, UpdateView

from apps.consults.models import ConsultNote
from apps.patients.models import Patient
from services.aws_llm import generate_dummy_note
from services.docx_export import attach_docx_to_consult
from services.note_formatter import render_note_html
from services.prompt_builder import build_generation_payload

from .forms import GenerationSettingsForm
from .models import GenerationSession


class StartGenerationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        session = GenerationSession.objects.create(user=request.user)
        session.ensure_defaults()
        return redirect('generation:patient', pk=session.pk)


class GenerationSessionMixin(LoginRequiredMixin):
    model = GenerationSession

    def get_queryset(self):
        return GenerationSession.objects.filter(user=self.request.user).select_related(
            'selected_patient', 'selected_system_prompt', 'selected_user_prompt', 'selected_edit_prompt', 'selected_format', 'selected_model'
        )


class GenerationPatientSelectView(GenerationSessionMixin, DetailView):
    template_name = 'generation/patient_select.html'
    context_object_name = 'session'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patients'] = Patient.objects.all()[:25]
        return context


class GenerationSetPatientView(GenerationSessionMixin, View):
    def get(self, request, *args, **kwargs):
        session = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        session.selected_patient = patient
        session.save(update_fields=['selected_patient', 'updated_at'])
        messages.success(request, f'{patient.patient_name} selected for generation.')
        return redirect('generation:settings', pk=session.pk)


class GenerationRandomPatientView(GenerationSessionMixin, View):
    def get(self, request, *args, **kwargs):
        session = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        patient_ids = list(Patient.objects.values_list('id', flat=True))
        if not patient_ids:
            messages.warning(request, 'No patients are available yet. Import or create one first.')
            return redirect('patients:list')
        session.selected_patient_id = random.choice(patient_ids)
        session.save(update_fields=['selected_patient', 'updated_at'])
        return redirect('generation:settings', pk=session.pk)


class GenerationSettingsView(GenerationSessionMixin, UpdateView):
    form_class = GenerationSettingsForm
    template_name = 'generation/settings.html'
    context_object_name = 'session'

    def get_object(self, queryset=None):
        return super().get_object(queryset).ensure_defaults()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data['set_system_active'] and self.object.selected_system_prompt:
            self.object.selected_system_prompt.is_active = True
            self.object.selected_system_prompt.save()
        if form.cleaned_data['set_user_active'] and self.object.selected_user_prompt:
            self.object.selected_user_prompt.is_active = True
            self.object.selected_user_prompt.save()
        if form.cleaned_data['set_edit_active'] and self.object.selected_edit_prompt:
            self.object.selected_edit_prompt.is_active = True
            self.object.selected_edit_prompt.save()
        if form.cleaned_data['set_format_active'] and self.object.selected_format:
            self.object.selected_format.is_active = True
            self.object.selected_format.save()
        self.object.settings_snapshot_json = self.object.snapshot()
        self.object.save(update_fields=['settings_snapshot_json', 'updated_at'])
        messages.success(self.request, 'Generation settings saved.')
        return response

    def get_success_url(self):
        return reverse('generation:summary', kwargs={'pk': self.object.pk})


class GenerationSummaryView(GenerationSessionMixin, DetailView):
    template_name = 'generation/summary.html'
    context_object_name = 'session'

    def get_object(self, queryset=None):
        return super().get_object(queryset).ensure_defaults()


class GenerateConsultNoteView(GenerationSessionMixin, View):
    def post(self, request, *args, **kwargs):
        session = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        session.ensure_defaults()
        if not session.selected_patient:
            messages.error(request, 'Please select a patient first.')
            return redirect('generation:patient', pk=session.pk)

        system_prompt, user_prompt = build_generation_payload(session)
        note_text = generate_dummy_note(
            patient=session.selected_patient,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            edit_prompt=session.selected_edit_prompt.content if session.selected_edit_prompt else '',
            user_instructions=session.user_instructions,
        )
        consult_note = ConsultNote.objects.create(
            user=request.user,
            patient=session.selected_patient,
            title=session.selected_patient.consult_title,
            status=ConsultNote.Status.GENERATED,
            note_text=note_text,
            note_html=render_note_html(note_text),
            prompt_system_used=system_prompt,
            prompt_user_used=user_prompt,
            prompt_edit_used=session.selected_edit_prompt.content if session.selected_edit_prompt else '',
            format_snapshot_json=session.selected_format.snapshot() if session.selected_format else {},
            llm_model_key=session.selected_model.model_key if session.selected_model else '',
            temperature=session.temperature,
            top_p=session.top_p,
            max_tokens=session.max_tokens,
            presence_penalty=session.presence_penalty,
            frequency_penalty=session.frequency_penalty,
            user_instructions=session.user_instructions,
            generation_settings_json=session.snapshot(),
        )
        attach_docx_to_consult(consult_note)
        session.settings_snapshot_json = session.snapshot()
        session.save(update_fields=['settings_snapshot_json', 'updated_at'])
        messages.success(request, 'Dummy consult note generated.')
        return redirect('consults:detail', pk=consult_note.pk)
