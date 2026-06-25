from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class UppercasePasswordValidator:
    def validate(self, password, user=None):
        if not any(character.isupper() for character in password):
            raise ValidationError(
                _('This password must contain at least one uppercase letter.'),
                code='password_requires_uppercase',
            )

    def get_help_text(self):
        return _('Your password must contain at least one uppercase letter.')
