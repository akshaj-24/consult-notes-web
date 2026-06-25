from __future__ import annotations

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q


class Prompt(models.Model):
    class PromptType(models.TextChoices):
        SYSTEM = 'system', 'System'
        USER = 'user', 'User'
        EDIT = 'edit', 'Edit'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prompts')
    name = models.CharField(max_length=150)
    prompt_type = models.CharField(max_length=16, choices=PromptType.choices)
    content = models.TextField()
    is_active = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['prompt_type', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'prompt_type'],
                condition=Q(is_active=True),
                name='unique_active_prompt_per_user_and_type',
            )
        ]

    def __str__(self) -> str:
        return f'{self.name} ({self.get_prompt_type_display()})'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_active and self.user_id:
                type(self).objects.filter(
                    user_id=self.user_id,
                    prompt_type=self.prompt_type,
                    is_active=True,
                ).exclude(pk=self.pk).update(is_active=False)
            super().save(*args, **kwargs)
