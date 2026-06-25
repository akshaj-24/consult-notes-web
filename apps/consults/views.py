from __future__ import annotations

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from apps.core.mixins import SuperuserRequiredMixin
from services.aws_llm import generate_dummy_note
from services.docx_export import attach_docx_to_consult
from services.note_formatter import render_note_html

from .forms import RegenerationForm, ReviewAutosaveForm
from .models import ConsultNote


def consult_note_queryset(user):
    queryset = ConsultNote.objects.select_related('patient', 'user')
    if user.is_superuser:
        return queryset
    return queryset.filter(user=user)


class ConsultNoteListView(LoginRequiredMixin, TemplateView):
    template_name = 'consults/consult_note_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notes = list(consult_note_queryset(self.request.user))
        selected_note = None
        if self.kwargs.get('pk'):
            selected_note = get_object_or_404(consult_note_queryset(self.request.user), pk=self.kwargs['pk'])
        elif notes:
            selected_note = notes[0]
        context['notes'] = notes
        context['selected_note'] = selected_note
        context['review_form'] = ReviewAutosaveForm(
            initial={
                'rating': selected_note.rating if selected_note else None,
                'comment': selected_note.comment if selected_note else '',
            }
        )
        context['rating_choices'] = [Decimal(index) / 2 for index in range(1, 11)]
        context['regeneration_form'] = RegenerationForm()
        return context


class ConsultReviewAutosaveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        note = get_object_or_404(consult_note_queryset(request.user), pk=kwargs['pk'])
        form = ReviewAutosaveForm(request.POST)
        if not form.is_valid():
            return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
        note.rating = form.cleaned_data.get('rating')
        note.comment = form.cleaned_data.get('comment', '')
        note.save(update_fields=['rating', 'comment', 'updated_at'])
        return JsonResponse({'ok': True, 'updated_at': note.updated_at.isoformat()})


class ConsultRegenerateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        note = get_object_or_404(consult_note_queryset(request.user), pk=kwargs['pk'])
        form = RegenerationForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Please provide valid edit instructions.')
            return redirect('consults:detail', pk=note.pk)

        edit_instructions = form.cleaned_data['edit_instructions'].strip()
        regenerated_note = generate_dummy_note(
            patient=note.patient,
            system_prompt=note.prompt_system_used,
            user_prompt=note.prompt_user_used,
            edit_prompt=note.prompt_edit_used,
            user_instructions=note.user_instructions,
            previous_note=note.note_text,
            edit_instructions=edit_instructions,
        )
        note.note_text = regenerated_note
        note.note_html = render_note_html(regenerated_note)
        note.last_regeneration_reason = edit_instructions
        note.status = ConsultNote.Status.EDITED
        note.save()
        attach_docx_to_consult(note)
        messages.success(request, 'Dummy regeneration complete.')
        return redirect('consults:detail', pk=note.pk)


class LoadSettingsFromConsultView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        note = get_object_or_404(consult_note_queryset(request.user), pk=kwargs['pk'])
        from apps.generation.models import GenerationSession

        session = GenerationSession.from_consult_note(request.user, note)
        messages.success(request, 'Generation settings loaded into a new session.')
        return redirect('generation:settings', pk=session.pk)


class ConsultDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        note = get_object_or_404(ConsultNote, pk=kwargs['pk'])
        note_title = note.title
        if note.docx_file:
            note.docx_file.delete(save=False)
        note.delete()
        messages.success(request, f'{note_title} was deleted.')
        return redirect('consults:list')
