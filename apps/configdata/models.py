from __future__ import annotations

from django.db import models


class LLMModelConfig(models.Model):
    provider = models.CharField(max_length=100)
    model_key = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    supports_temperature = models.BooleanField(default=True)
    supports_top_p = models.BooleanField(default=True)
    supports_max_tokens = models.BooleanField(default=True)
    supports_system_prompt = models.BooleanField(default=True)
    supports_streaming = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'display_name']

    def __str__(self) -> str:
        return self.display_name
