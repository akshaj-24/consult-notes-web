from __future__ import annotations

from django import forms

from apps.core.forms import BootstrapFormMixin

from .models import NoteFormat


class NoteFormatForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = NoteFormat
        exclude = ('user', 'created_at', 'updated_at')
