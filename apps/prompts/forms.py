from __future__ import annotations

from django import forms

from apps.core.forms import BootstrapFormMixin

from .models import Prompt


class PromptForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ('name', 'prompt_type', 'description', 'content', 'is_active')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 12}),
        }
