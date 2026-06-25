from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_approved = models.BooleanField(default=False)
    active_format = models.ForeignKey(
        'formats.NoteFormat',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='active_for_users',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['username']

    def __str__(self) -> str:
        return self.username
