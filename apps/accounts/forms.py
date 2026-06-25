from __future__ import annotations

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            field.widget.attrs.setdefault('class', css_class)


class AlphabetChallengeMixin(forms.Form):
    challenge_answer = forms.CharField(
        label="What's the first letter in the alphabet?",
        max_length=1,
    )

    def clean_challenge_answer(self) -> str:
        value = self.cleaned_data['challenge_answer'].strip()
        if value.lower() != 'a':
            raise forms.ValidationError('Please enter A or a to continue.')
        return value


class ApprovalAwareAuthenticationForm(StyledFormMixin, AlphabetChallengeMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))


class SignupForm(StyledFormMixin, AlphabetChallengeMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.is_approved = False
        if commit:
            user.save()
        return user
