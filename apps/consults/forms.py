from __future__ import annotations

from django import forms

from apps.core.forms import BootstrapFormMixin


class ReviewAutosaveForm(BootstrapFormMixin, forms.Form):
    rating = forms.DecimalField(min_value=0, max_value=5, decimal_places=1, required=False)
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}))


class RegenerationForm(BootstrapFormMixin, forms.Form):
    edit_instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the edits you want to see in the regenerated note.'}),
    )
