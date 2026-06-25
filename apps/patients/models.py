from __future__ import annotations

from django.conf import settings
from django.db import models


class Patient(models.Model):
    class SourceType(models.TextChoices):
        SEED = 'seed', 'Bundled Seed'
        MANUAL = 'manual', 'Manual Entry'
        COPY = 'copy', 'Copied Record'
        IMPORT = 'import', 'Imported'

    synthetic_patient_id = models.CharField(max_length=64, blank=True)
    mrn = models.CharField(max_length=128, unique=True)
    patient_name = models.CharField(max_length=255)
    fake_phn = models.CharField(max_length=128, blank=True)
    province_context = models.CharField(max_length=255, blank=True)
    consult_date = models.DateField(null=True, blank=True)
    consult_type = models.CharField(max_length=255, blank=True)
    referral_source = models.CharField(max_length=255, blank=True)
    reason_for_referral = models.TextField(blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=64, blank=True)
    gender_identity = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=255, blank=True)
    interpreter_needed = models.TextField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    referring_physician = models.CharField(max_length=255, blank=True)
    primary_care_physician = models.CharField(max_length=255, blank=True)
    cancer_site = models.CharField(max_length=255, blank=True)
    tumour_location_detail = models.TextField(blank=True)
    laterality_category = models.CharField(max_length=255, blank=True)
    histology = models.CharField(max_length=255, blank=True)
    grade = models.CharField(max_length=255, blank=True)
    disease_setting = models.CharField(max_length=255, blank=True)
    clinical_stage = models.CharField(max_length=255, blank=True)
    pathologic_stage = models.CharField(max_length=255, blank=True)
    tnm_stage = models.CharField(max_length=255, blank=True)
    metastatic_sites = models.TextField(blank=True)
    disease_burden = models.TextField(blank=True)
    treatment_intent = models.CharField(max_length=255, blank=True)
    presentation_mode = models.TextField(blank=True)
    presenting_symptoms = models.TextField(blank=True)
    symptom_duration = models.CharField(max_length=255, blank=True)
    diagnostic_timeline = models.TextField(blank=True)
    current_symptoms = models.TextField(blank=True)
    weight_loss = models.CharField(max_length=255, blank=True)
    ecog = models.CharField(max_length=32, blank=True)
    past_medical_history = models.TextField(blank=True)
    past_surgical_history = models.TextField(blank=True)
    home_medications = models.TextField(blank=True)
    medication_adherence = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    living_situation = models.TextField(blank=True)
    occupation_status = models.CharField(max_length=255, blank=True)
    supports = models.TextField(blank=True)
    family_dynamics = models.TextField(blank=True)
    adls_iadls = models.TextField(blank=True)
    mobility_aids = models.TextField(blank=True)
    transportation_barriers = models.TextField(blank=True)
    financial_coverage_issues = models.TextField(blank=True)
    smoking_history = models.TextField(blank=True)
    alcohol_history = models.TextField(blank=True)
    substance_history = models.TextField(blank=True)
    extended_health_benefits = models.TextField(blank=True)
    family_history_cancer = models.TextField(blank=True)
    family_history_autoimmune = models.TextField(blank=True)
    hereditary_risk_flag = models.TextField(blank=True)
    key_labs = models.TextField(blank=True)
    tumour_markers = models.TextField(blank=True)
    imaging_summary = models.TextField(blank=True)
    endoscopy_findings = models.TextField(blank=True)
    pathology_summary = models.TextField(blank=True)
    molecular_summary = models.TextField(blank=True)
    pending_tests = models.TextField(blank=True)
    prior_cancer_treatment = models.TextField(blank=True)
    prior_interventions = models.TextField(blank=True)
    line_of_therapy = models.CharField(max_length=255, blank=True)
    proposed_management = models.TextField(blank=True)
    supportive_care_plan = models.TextField(blank=True)
    referrals = models.TextField(blank=True)
    tumour_board_needed = models.TextField(blank=True)
    follow_up_plan = models.TextField(blank=True)
    provider_style = models.CharField(max_length=255, blank=True)
    note_imperfection_level = models.CharField(max_length=255, blank=True)
    intentional_documentation_gaps = models.TextField(blank=True)
    source_type = models.CharField(max_length=16, choices=SourceType.choices, default=SourceType.MANUAL)
    source_payload = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_patients',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['patient_name', 'mrn']

    def __str__(self) -> str:
        return f'{self.patient_name} ({self.mrn})'

    @property
    def consult_title(self) -> str:
        date_text = self.consult_date.isoformat() if self.consult_date else 'undated'
        return f'{self.patient_name} consult {date_text}'
