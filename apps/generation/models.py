from __future__ import annotations

from django.conf import settings
from django.db import models


class GenerationSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='generation_sessions')
    selected_patient = models.ForeignKey('patients.Patient', null=True, blank=True, on_delete=models.SET_NULL, related_name='generation_sessions')
    selected_system_prompt = models.ForeignKey('prompts.Prompt', null=True, blank=True, on_delete=models.SET_NULL, related_name='system_prompt_sessions')
    selected_user_prompt = models.ForeignKey('prompts.Prompt', null=True, blank=True, on_delete=models.SET_NULL, related_name='user_prompt_sessions')
    selected_edit_prompt = models.ForeignKey('prompts.Prompt', null=True, blank=True, on_delete=models.SET_NULL, related_name='edit_prompt_sessions')
    selected_format = models.ForeignKey('formats.NoteFormat', null=True, blank=True, on_delete=models.SET_NULL, related_name='generation_sessions')
    selected_model = models.ForeignKey('configdata.LLMModelConfig', null=True, blank=True, on_delete=models.SET_NULL, related_name='generation_sessions')
    temperature = models.DecimalField(max_digits=4, decimal_places=2, default=0.30)
    top_p = models.DecimalField(max_digits=4, decimal_places=2, default=0.90)
    max_tokens = models.PositiveIntegerField(default=1800)
    presence_penalty = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    frequency_penalty = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    user_instructions = models.TextField(blank=True)
    settings_snapshot_json = models.JSONField(default=dict, blank=True)
    source_consult_note = models.ForeignKey('consults.ConsultNote', null=True, blank=True, on_delete=models.SET_NULL, related_name='loaded_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self) -> str:
        patient = self.selected_patient.patient_name if self.selected_patient else 'No patient'
        return f'Session {self.pk} - {patient}'

    def ensure_defaults(self):
        from apps.configdata.models import LLMModelConfig
        from apps.formats.models import NoteFormat
        from apps.prompts.models import Prompt

        changed = False
        if not self.selected_system_prompt_id:
            self.selected_system_prompt = Prompt.objects.filter(user=self.user, prompt_type=Prompt.PromptType.SYSTEM, is_active=True).first()
            changed = changed or self.selected_system_prompt is not None
        if not self.selected_user_prompt_id:
            self.selected_user_prompt = Prompt.objects.filter(user=self.user, prompt_type=Prompt.PromptType.USER, is_active=True).first()
            changed = changed or self.selected_user_prompt is not None
        if not self.selected_edit_prompt_id:
            self.selected_edit_prompt = Prompt.objects.filter(user=self.user, prompt_type=Prompt.PromptType.EDIT, is_active=True).first()
            changed = changed or self.selected_edit_prompt is not None
        if not self.selected_format_id:
            self.selected_format = NoteFormat.objects.filter(user=self.user, is_active=True).first()
            changed = changed or self.selected_format is not None
        if not self.selected_model_id:
            self.selected_model = LLMModelConfig.objects.filter(is_active=True).first()
            changed = changed or self.selected_model is not None
        if changed:
            self.save()
        return self

    def snapshot(self):
        return {
            'patient_id': self.selected_patient_id,
            'system_prompt_id': self.selected_system_prompt_id,
            'user_prompt_id': self.selected_user_prompt_id,
            'edit_prompt_id': self.selected_edit_prompt_id,
            'format_id': self.selected_format_id,
            'model_id': self.selected_model_id,
            'temperature': str(self.temperature),
            'top_p': str(self.top_p),
            'max_tokens': self.max_tokens,
            'presence_penalty': str(self.presence_penalty),
            'frequency_penalty': str(self.frequency_penalty),
            'user_instructions': self.user_instructions,
        }

    @classmethod
    def from_consult_note(cls, user, note):
        from apps.configdata.models import LLMModelConfig
        from apps.formats.models import NoteFormat
        from apps.prompts.models import Prompt

        settings_json = note.generation_settings_json or {}
        session = cls.objects.create(
            user=user,
            selected_patient=note.patient,
            selected_system_prompt=Prompt.objects.filter(pk=settings_json.get('system_prompt_id'), user=user).first(),
            selected_user_prompt=Prompt.objects.filter(pk=settings_json.get('user_prompt_id'), user=user).first(),
            selected_edit_prompt=Prompt.objects.filter(pk=settings_json.get('edit_prompt_id'), user=user).first(),
            selected_format=NoteFormat.objects.filter(pk=settings_json.get('format_id'), user=user).first(),
            selected_model=LLMModelConfig.objects.filter(pk=settings_json.get('model_id')).first(),
            temperature=settings_json.get('temperature') or note.temperature or 0.30,
            top_p=settings_json.get('top_p') or note.top_p or 0.90,
            max_tokens=settings_json.get('max_tokens') or note.max_tokens or 1800,
            presence_penalty=settings_json.get('presence_penalty') or note.presence_penalty or 0,
            frequency_penalty=settings_json.get('frequency_penalty') or note.frequency_penalty or 0,
            user_instructions=settings_json.get('user_instructions') or note.user_instructions,
            source_consult_note=note,
            settings_snapshot_json=settings_json,
        )
        session.ensure_defaults()
        return session
