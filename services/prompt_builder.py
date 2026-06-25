from __future__ import annotations

from apps.generation.models import GenerationSession


def _format_directives(note_format):
    if not note_format:
        return ''
    directives = [
        f'Use heading font {note_format.heading_font_family} size {note_format.heading_font_size}.',
        f'Use body font {note_format.body_font_family} size {note_format.body_font_size}.',
        'Include separator lines between sections.'
        if note_format.show_lines_between_sections
        else 'Do not include separator lines between sections unless needed for clarity.',
    ]
    if note_format.header_text:
        directives.append(f'Header text: {note_format.header_text}.')
    if note_format.footer_text:
        directives.append(f'Footer text: {note_format.footer_text}.')
    return '\n'.join(directives)


def _patient_context(patient):
    lines = [
        f'Patient: {patient.patient_name}',
        f'MRN: {patient.mrn}',
        f'Age/Sex: {patient.age or ""} / {patient.sex}',
        f'Consult date: {patient.consult_date or ""}',
        f'Reason for referral: {patient.reason_for_referral}',
        f'Disease setting: {patient.disease_setting}',
        f'Cancer site: {patient.cancer_site}',
        f'Histology: {patient.histology}',
        f'Clinical stage: {patient.clinical_stage}',
        f'Pathologic stage: {patient.pathologic_stage}',
        f'Current symptoms: {patient.current_symptoms}',
        f'Past medical history: {patient.past_medical_history}',
        f'Past surgical history: {patient.past_surgical_history}',
        f'Home medications: {patient.home_medications}',
        f'Allergies: {patient.allergies}',
        f'Social history: {patient.living_situation}; {patient.occupation_status}; {patient.smoking_history}; {patient.alcohol_history}',
        f'Family history: {patient.family_history_cancer}',
        f'Investigations: {patient.key_labs}; {patient.imaging_summary}; {patient.endoscopy_findings}; {patient.pathology_summary}; {patient.molecular_summary}',
        f'Proposed management: {patient.proposed_management}',
        f'Supportive care plan: {patient.supportive_care_plan}',
        f'Follow-up plan: {patient.follow_up_plan}',
        f'Provider style: {patient.provider_style}',
        f'Intentional documentation gaps: {patient.intentional_documentation_gaps}',
    ]
    return '\n'.join(line for line in lines if line.split(': ', 1)[-1].strip())


def build_generation_payload(session: GenerationSession):
    system_prompt = session.selected_system_prompt.content if session.selected_system_prompt else ''
    user_prompt = session.selected_user_prompt.content if session.selected_user_prompt else ''
    format_directives = _format_directives(session.selected_format)
    patient_context = _patient_context(session.selected_patient)
    instructions_block = ''
    if session.user_instructions:
        instructions_block = f'\n\nFollow these specific user instructions: {session.user_instructions}'
    final_system_prompt = '\n\n'.join(part for part in [system_prompt, format_directives] if part) + instructions_block
    final_user_prompt = '\n\n'.join(part for part in [user_prompt, patient_context] if part) + instructions_block
    return final_system_prompt.strip(), final_user_prompt.strip()
