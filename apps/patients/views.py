from __future__ import annotations

import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from apps.core.mixins import SuperuserRequiredMixin

from .forms import PatientForm
from .models import Patient
from .services import copy_patient_initial, patient_detail_sections


class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(patient_name__icontains=query)
                | Q(mrn__icontains=query)
                | Q(cancer_site__icontains=query)
                | Q(disease_setting__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/patient_detail.html'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = patient_detail_sections(self.object)
        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        if not form.instance.source_type:
            form.instance.source_type = Patient.SourceType.MANUAL
        messages.success(self.request, 'Patient record created.')
        return super().form_valid(form)

    def get_success_url(self):
        session_id = self.request.GET.get('session') or self.request.POST.get('session')
        if session_id:
            return reverse('generation:set_patient', kwargs={'pk': session_id, 'patient_id': self.object.pk})
        return reverse('patients:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Patient'
        context['session_id'] = self.request.GET.get('session', '')
        return context


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'

    def form_valid(self, form):
        if not form.instance.created_by_id:
            form.instance.created_by = self.request.user
        messages.success(self.request, 'Patient record updated.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patients:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Patient'
        context['session_id'] = ''
        return context


class PatientCopyView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/patient_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.source_patient = get_object_or_404(Patient, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        return copy_patient_initial(self.source_patient)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.source_type = Patient.SourceType.COPY
        messages.success(self.request, 'Patient record copied.')
        return super().form_valid(form)

    def get_success_url(self):
        session_id = self.request.GET.get('session') or self.request.POST.get('session')
        if session_id:
            return reverse('generation:set_patient', kwargs={'pk': session_id, 'patient_id': self.object.pk})
        return reverse('patients:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Copy Patient: {self.source_patient.patient_name}'
        context['session_id'] = self.request.GET.get('session', '')
        return context


class RandomPatientRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        patient_ids = list(Patient.objects.values_list('id', flat=True))
        if not patient_ids:
            messages.warning(request, 'No patients are available yet. Import or create one first.')
            return redirect('patients:list')
        return redirect('patients:detail', pk=random.choice(patient_ids))


class PatientDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        patient = get_object_or_404(Patient, pk=kwargs['pk'])
        patient_name = patient.patient_name
        for note in patient.consult_notes.all():
            if note.docx_file:
                note.docx_file.delete(save=False)
        patient.delete()
        messages.success(request, f'{patient_name} was deleted.')
        return redirect('patients:list')
