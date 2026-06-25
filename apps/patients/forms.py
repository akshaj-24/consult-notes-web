from __future__ import annotations

from django import forms

from apps.core.forms import BootstrapFormMixin

from .models import Patient

PATIENT_FIELDSETS = [
    ('Identifiers', ['synthetic_patient_id', 'mrn', 'patient_name', 'fake_phn', 'province_context', 'consult_date', 'consult_type']),
    ('Referral', ['referral_source', 'reason_for_referral', 'referring_physician', 'primary_care_physician']),
    ('Demographics', ['age', 'sex', 'gender_identity', 'language', 'interpreter_needed', 'city']),
    ('Cancer Details', ['cancer_site', 'tumour_location_detail', 'laterality_category', 'histology', 'grade', 'disease_setting', 'clinical_stage', 'pathologic_stage', 'tnm_stage', 'metastatic_sites', 'disease_burden', 'treatment_intent']),
    ('Presentation', ['presentation_mode', 'presenting_symptoms', 'symptom_duration', 'diagnostic_timeline', 'current_symptoms', 'weight_loss', 'ecog']),
    ('Past History', ['past_medical_history', 'past_surgical_history', 'home_medications', 'medication_adherence', 'allergies']),
    ('Social History', ['living_situation', 'occupation_status', 'supports', 'family_dynamics', 'adls_iadls', 'mobility_aids', 'transportation_barriers', 'financial_coverage_issues', 'smoking_history', 'alcohol_history', 'substance_history', 'extended_health_benefits']),
    ('Family History', ['family_history_cancer', 'family_history_autoimmune', 'hereditary_risk_flag']),
    ('Investigations', ['key_labs', 'tumour_markers', 'imaging_summary', 'endoscopy_findings', 'pathology_summary', 'molecular_summary', 'pending_tests']),
    ('Treatment Planning', ['prior_cancer_treatment', 'prior_interventions', 'line_of_therapy', 'proposed_management', 'supportive_care_plan', 'referrals', 'tumour_board_needed', 'follow_up_plan']),
    ('Variability', ['provider_style', 'note_imperfection_level', 'intentional_documentation_gaps', 'source_type']),
]


class PatientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ('created_by', 'source_payload', 'created_at', 'updated_at')
        widgets = {
            'consult_date': forms.DateInput(attrs={'type': 'date'}),
        }

    fieldsets = PATIENT_FIELDSETS
