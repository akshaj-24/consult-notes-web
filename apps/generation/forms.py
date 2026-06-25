from __future__ import annotations

from django import forms

from apps.configdata.models import LLMModelConfig
from apps.core.forms import BootstrapFormMixin
from apps.formats.models import NoteFormat
from apps.prompts.models import Prompt

from .models import GenerationSession


class GenerationSettingsForm(BootstrapFormMixin, forms.ModelForm):
    set_system_active = forms.BooleanField(required=False, label='Set selected system prompt active')
    set_user_active = forms.BooleanField(required=False, label='Set selected user prompt active')
    set_edit_active = forms.BooleanField(required=False, label='Set selected edit prompt active')
    set_format_active = forms.BooleanField(required=False, label='Set selected format active')

    class Meta:
        model = GenerationSession
        fields = (
            'selected_system_prompt',
            'selected_user_prompt',
            'selected_edit_prompt',
            'selected_format',
            'selected_model',
            'temperature',
            'top_p',
            'max_tokens',
            'presence_penalty',
            'frequency_penalty',
            'user_instructions',
        )
        widgets = {
            'user_instructions': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['selected_system_prompt'].queryset = Prompt.objects.filter(user=user, prompt_type=Prompt.PromptType.SYSTEM)
        self.fields['selected_user_prompt'].queryset = Prompt.objects.filter(user=user, prompt_type=Prompt.PromptType.USER)
        self.fields['selected_edit_prompt'].queryset = Prompt.objects.filter(user=user, prompt_type=Prompt.PromptType.EDIT)
        self.fields['selected_format'].queryset = NoteFormat.objects.filter(user=user)
        self.fields['selected_model'].queryset = LLMModelConfig.objects.filter(is_active=True)
