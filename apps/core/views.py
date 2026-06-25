from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView

from apps.configdata.models import LLMModelConfig
from apps.configdata.services import import_model_configs
from apps.consults.models import ConsultNote
from apps.formats.models import NoteFormat
from apps.generation.models import GenerationSession
from apps.patients.models import Patient
from apps.patients.services import import_patient_seed
from apps.prompts.models import Prompt


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_approved:
                return redirect('core:dashboard')
            return redirect('accounts:awaiting_approval')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prompt_queryset = Prompt.objects.all() if self.request.user.is_superuser else Prompt.objects.filter(user=self.request.user)
        format_queryset = NoteFormat.objects.all() if self.request.user.is_superuser else NoteFormat.objects.filter(user=self.request.user)
        note_queryset = ConsultNote.objects.all() if self.request.user.is_superuser else ConsultNote.objects.filter(user=self.request.user)
        session_queryset = (
            GenerationSession.objects.all() if self.request.user.is_superuser else GenerationSession.objects.filter(user=self.request.user)
        )
        context['counts'] = {
            'patients': Patient.objects.count(),
            'prompts': prompt_queryset.count(),
            'formats': format_queryset.count(),
            'notes': note_queryset.count(),
            'sessions': session_queryset.count(),
            'models': LLMModelConfig.objects.filter(is_active=True).count(),
        }
        context['latest_notes'] = note_queryset.select_related('patient', 'user')[:5]
        return context


class ImportPatientSeedView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        created, updated = import_patient_seed()
        messages.success(request, f'Patient seed import complete: {created} created, {updated} updated.')
        return redirect(request.POST.get('next') or 'patients:list')


class RefreshModelCatalogView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        created, updated = import_model_configs()
        messages.success(request, f'Model catalog refreshed: {created} created, {updated} updated.')
        return redirect(request.POST.get('next') or 'core:dashboard')
