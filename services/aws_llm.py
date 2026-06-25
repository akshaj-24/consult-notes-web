from __future__ import annotations

from pathlib import Path

from django.conf import settings
from docx import Document

SAMPLE_NOTE_PATH = settings.BASE_DIR / 'data' / 'synthetic_crc_v2_consult_note_CRCV2-001.docx'


def load_sample_note_text() -> str:
    if not Path(SAMPLE_NOTE_PATH).exists():
        return ''
    document = Document(SAMPLE_NOTE_PATH)
    return '\n'.join(paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip())


def _line(text: str, fallback: str = 'Not documented') -> str:
    value = (text or '').strip()
    return value or fallback


def generate_dummy_note(
    *,
    patient,
    system_prompt: str,
    user_prompt: str,
    edit_prompt: str = '',
    user_instructions: str = '',
    previous_note: str = '',
    edit_instructions: str = '',
) -> str:
    sample_note = load_sample_note_text()
    note_lines = [
        'MEDICAL ONCOLOGY CONSULT NOTE',
        f'Patient ID: {patient.patient_name} is a {patient.age or ""} year old {patient.sex or "patient"} from {patient.province_context or patient.city or "British Columbia"}',
        f'Referring physician: {_line(patient.referring_physician or patient.referral_source)}',
        f'Primary care physician: {_line(patient.primary_care_physician)}',
        f'MRN: {patient.mrn}',
        f'{patient.patient_name.split()[0] if patient.patient_name else "The patient"} was referred for {_line(patient.reason_for_referral)}.',
        'PAST MEDICAL HISTORY',
        f'-- {_line(patient.past_medical_history)}',
        'SURGICAL HISTORY',
        f'-- {_line(patient.past_surgical_history)}',
        'HOME MEDICATIONS',
        f'-- {_line(patient.home_medications)}',
        'ALLERGIES',
        _line(patient.allergies),
        'SOCIAL HISTORY',
        f'{_line(patient.living_situation)} {_line(patient.occupation_status, "")} {_line(patient.supports, "")}'.strip(),
        'FAMILY HISTORY',
        _line(patient.family_history_cancer),
        'HISTORY OF PRESENTING ILLNESS',
        _line(patient.diagnostic_timeline),
        _line(patient.current_symptoms or patient.presenting_symptoms),
        'PHYSICAL EXAM',
        f'Performance status ECOG {_line(patient.ecog)}. Dummy exam placeholder while AWS generation is disabled.',
        'INVESTIGATIONS',
        f'Bloodwork and biomarkers: {_line(patient.key_labs)}',
        f'Imaging: {_line(patient.imaging_summary)}',
        f'Endoscopy: {_line(patient.endoscopy_findings)}',
        f'Pathology: {_line(patient.pathology_summary)}',
        f'Molecular: {_line(patient.molecular_summary)}',
        'ASSESSMENT AND PLAN',
        f'{patient.age or ""}{patient.sex[:1] if patient.sex else "P"} with {patient.disease_setting or patient.cancer_site or "colorectal cancer"}. This deterministic sample note is being used because AWS integration is disabled.',
        f'-- Proposed management: {_line(patient.proposed_management)}',
        f'-- Supportive care: {_line(patient.supportive_care_plan)}',
        f'-- Referrals: {_line(patient.referrals)}',
        f'-- Follow-up: {_line(patient.follow_up_plan)}',
    ]
    if user_instructions:
        note_lines.extend(['USER INSTRUCTIONS', user_instructions])
    if edit_instructions:
        note_lines.extend(
            [
                'ADDENDUM / REGENERATION NOTES',
                'This dummy regeneration preserved the structured placeholder note and recorded the requested revision.',
                f'-- Requested edits: {edit_instructions}',
            ]
        )
    if sample_note:
        note_lines.extend(['REFERENCE SAMPLE NOTE BASIS', sample_note.splitlines()[0]])
    if system_prompt:
        note_lines.extend(['SYSTEM PROMPT SNAPSHOT', system_prompt[:500]])
    if user_prompt:
        note_lines.extend(['USER PROMPT SNAPSHOT', user_prompt[:500]])
    if previous_note and edit_instructions:
        note_lines.extend(['PREVIOUS NOTE SNAPSHOT', previous_note[:500]])
    if edit_prompt:
        note_lines.extend(['EDIT PROMPT SNAPSHOT', edit_prompt[:300]])
    return '\n'.join(line for line in note_lines if line is not None and str(line).strip())
