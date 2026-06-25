from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.db import models


def consult_docx_upload_to(instance, filename):
    suffix = Path(filename).suffix or '.docx'
    return f'consult_notes/{instance.created_at:%Y/%m}/{instance.patient.mrn}-{instance.pk or "draft"}{suffix}'


class ConsultNote(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        GENERATED = 'generated', 'Generated'
        EDITED = 'edited', 'Edited'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consult_notes')
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='consult_notes')
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    note_text = models.TextField(blank=True)
    note_html = models.TextField(blank=True)
    docx_file = models.FileField(upload_to=consult_docx_upload_to, blank=True)
    source_storage_path = models.CharField(max_length=255, blank=True)
    prompt_system_used = models.TextField(blank=True)
    prompt_user_used = models.TextField(blank=True)
    prompt_edit_used = models.TextField(blank=True)
    format_snapshot_json = models.JSONField(default=dict, blank=True)
    llm_model_key = models.CharField(max_length=150, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    top_p = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    max_tokens = models.PositiveIntegerField(null=True, blank=True)
    presence_penalty = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    frequency_penalty = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    user_instructions = models.TextField(blank=True)
    generation_settings_json = models.JSONField(default=dict, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    comment = models.TextField(blank=True)
    last_regeneration_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return self.title
