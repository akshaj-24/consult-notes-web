from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from django.conf import settings

from .models import Patient

PATIENT_FIELD_MAP = {
    'synthetic_patient_id': 'synthetic_patient_id',
    'fake_name': 'patient_name',
    'fake_phn_or_mrn': 'mrn',
    'province_context': 'province_context',
    'consult_date': 'consult_date',
    'consult_type': 'consult_type',
    'referral_source': 'referral_source',
    'reason_for_referral': 'reason_for_referral',
    'age': 'age',
    'sex': 'sex',
    'gender_identity_if_relevant': 'gender_identity',
    'language': 'language',
    'interpreter_needed': 'interpreter_needed',
    'crc_site': 'cancer_site',
    'tumour_location_detail': 'tumour_location_detail',
    'right_left_rectal_category': 'laterality_category',
    'histology': 'histology',
    'grade': 'grade',
    'disease_setting': 'disease_setting',
    'clinical_stage': 'clinical_stage',
    'pathologic_stage': 'pathologic_stage',
    'metastatic_sites': 'metastatic_sites',
    'disease_burden': 'disease_burden',
    'treatment_intent': 'treatment_intent',
    'presentation_mode': 'presentation_mode',
    'presenting_symptoms': 'presenting_symptoms',
    'symptom_duration': 'symptom_duration',
    'diagnostic_timeline': 'diagnostic_timeline',
    'current_symptoms': 'current_symptoms',
    'weight_loss': 'weight_loss',
    'ECOG': 'ecog',
    'PMHx': 'past_medical_history',
    'past_surgical_history': 'past_surgical_history',
    'home_medications': 'home_medications',
    'medication_adherence': 'medication_adherence',
    'allergies': 'allergies',
    'social_living_situation': 'living_situation',
    'occupation_or_retired': 'occupation_status',
    'supports': 'supports',
    'family_dynamics': 'family_dynamics',
    'ADLs_IADLs': 'adls_iadls',
    'mobility_aids': 'mobility_aids',
    'transportation_barriers': 'transportation_barriers',
    'financial_or_drug_coverage_issues': 'financial_coverage_issues',
    'smoking_history': 'smoking_history',
    'alcohol_history': 'alcohol_history',
    'substance_history': 'substance_history',
    'extended_health_benefits': 'extended_health_benefits',
    'family_history_cancer': 'family_history_cancer',
    'family_history_autoimmune': 'family_history_autoimmune',
    'hereditary_risk_flag': 'hereditary_risk_flag',
    'key_labs': 'key_labs',
    'tumour_markers': 'tumour_markers',
    'imaging_summary': 'imaging_summary',
    'colonoscopy_or_endoscopy': 'endoscopy_findings',
    'pathology_summary': 'pathology_summary',
    'molecular_summary': 'molecular_summary',
    'pending_tests': 'pending_tests',
    'prior_cancer_treatment': 'prior_cancer_treatment',
    'prior_interventions': 'prior_interventions',
    'line_of_therapy': 'line_of_therapy',
    'proposed_management': 'proposed_management',
    'supportive_care_plan': 'supportive_care_plan',
    'referrals': 'referrals',
    'tumour_board_needed': 'tumour_board_needed',
    'follow_up_plan': 'follow_up_plan',
    'provider_style': 'provider_style',
    'note_imperfection_level': 'note_imperfection_level',
    'intentional_documentation_gaps': 'intentional_documentation_gaps',
}

PATIENT_DETAIL_SECTIONS = [
    ('Overview', ['mrn', 'patient_name', 'consult_date', 'consult_type', 'province_context', 'age', 'sex', 'language', 'interpreter_needed']),
    ('Referral', ['referral_source', 'reason_for_referral', 'referring_physician', 'primary_care_physician']),
    ('Disease', ['cancer_site', 'tumour_location_detail', 'laterality_category', 'histology', 'grade', 'disease_setting', 'clinical_stage', 'pathologic_stage', 'tnm_stage', 'metastatic_sites', 'disease_burden', 'treatment_intent']),
    ('Symptoms and Timeline', ['presentation_mode', 'presenting_symptoms', 'symptom_duration', 'diagnostic_timeline', 'current_symptoms', 'weight_loss', 'ecog']),
    ('Medical History', ['past_medical_history', 'past_surgical_history', 'home_medications', 'medication_adherence', 'allergies']),
    ('Social', ['living_situation', 'occupation_status', 'supports', 'family_dynamics', 'adls_iadls', 'mobility_aids', 'transportation_barriers', 'financial_coverage_issues', 'smoking_history', 'alcohol_history', 'substance_history', 'extended_health_benefits']),
    ('Family and Genetics', ['family_history_cancer', 'family_history_autoimmune', 'hereditary_risk_flag']),
    ('Investigations', ['key_labs', 'tumour_markers', 'imaging_summary', 'endoscopy_findings', 'pathology_summary', 'molecular_summary', 'pending_tests']),
    ('Plan', ['prior_cancer_treatment', 'prior_interventions', 'line_of_therapy', 'proposed_management', 'supportive_care_plan', 'referrals', 'tumour_board_needed', 'follow_up_plan', 'provider_style', 'note_imperfection_level', 'intentional_documentation_gaps']),
]

FIELD_LABELS = {field.name: field.verbose_name.replace('_', ' ').title() for field in Patient._meta.fields}


def _clean_value(value: str):
    value = (value or '').strip()
    return value or ''


def _parse_date(value: str):
    value = _clean_value(value)
    if not value:
        return None
    return date.fromisoformat(value)


def _parse_int(value: str):
    value = _clean_value(value)
    if not value:
        return None
    return int(value)


def import_patient_seed(csv_path: Path | None = None):
    csv_path = csv_path or settings.BASE_DIR / 'data' / 'patient_seed.csv'
    created = 0
    updated = 0
    if not csv_path.exists():
        return created, updated

    with csv_path.open(newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            defaults = {'source_type': Patient.SourceType.SEED, 'source_payload': row}
            for csv_field, model_field in PATIENT_FIELD_MAP.items():
                raw_value = row.get(csv_field, '')
                if model_field == 'consult_date':
                    defaults[model_field] = _parse_date(raw_value)
                elif model_field == 'age':
                    defaults[model_field] = _parse_int(raw_value)
                else:
                    defaults[model_field] = _clean_value(raw_value)
            _, was_created = Patient.objects.update_or_create(mrn=defaults['mrn'], defaults=defaults)
            if was_created:
                created += 1
            else:
                updated += 1
    return created, updated


def patient_detail_sections(patient: Patient):
    sections = []
    for title, fields in PATIENT_DETAIL_SECTIONS:
        rows = []
        for field_name in fields:
            value = getattr(patient, field_name)
            if value not in (None, ''):
                rows.append((FIELD_LABELS.get(field_name, field_name.replace('_', ' ').title()), value))
        if rows:
            sections.append((title, rows))
    return sections


def copy_patient_initial(patient: Patient):
    initial = {}
    for field in Patient._meta.fields:
        if field.name in {'id', 'created_at', 'updated_at'}:
            continue
        initial[field.name] = getattr(patient, field.name)
    initial['mrn'] = f'{patient.mrn}-COPY'
    initial['patient_name'] = f'{patient.patient_name} Copy'
    initial['source_type'] = Patient.SourceType.COPY
    initial['synthetic_patient_id'] = ''
    return initial
