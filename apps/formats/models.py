from __future__ import annotations

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q


class NoteFormat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note_formats')
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)
    heading_font_family = models.CharField(max_length=100, default='Arial')
    heading_font_size = models.PositiveSmallIntegerField(default=14)
    heading_bold = models.BooleanField(default=True)
    subheading_font_family = models.CharField(max_length=100, default='Arial')
    subheading_font_size = models.PositiveSmallIntegerField(default=12)
    subheading_bold = models.BooleanField(default=True)
    body_font_family = models.CharField(max_length=100, default='Arial')
    body_font_size = models.PositiveSmallIntegerField(default=11)
    body_bold = models.BooleanField(default=False)
    show_lines_between_sections = models.BooleanField(default=False)
    section_spacing = models.FloatField(default=1.0)
    left_margin = models.FloatField(default=1.0)
    right_margin = models.FloatField(default=1.0)
    top_margin = models.FloatField(default=1.0)
    bottom_margin = models.FloatField(default=1.0)
    header_text = models.CharField(max_length=255, blank=True)
    footer_text = models.CharField(max_length=255, blank=True)
    template_style_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(is_active=True),
                name='unique_active_note_format_per_user',
            )
        ]

    def __str__(self) -> str:
        return f'{self.name} ({self.user.username})'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_active and self.user_id:
                type(self).objects.filter(user_id=self.user_id, is_active=True).exclude(pk=self.pk).update(is_active=False)
            super().save(*args, **kwargs)
            if self.is_active:
                type(self.user).objects.filter(pk=self.user_id).update(active_format=self)

    def snapshot(self):
        return {
            'name': self.name,
            'heading_font_family': self.heading_font_family,
            'heading_font_size': self.heading_font_size,
            'heading_bold': self.heading_bold,
            'subheading_font_family': self.subheading_font_family,
            'subheading_font_size': self.subheading_font_size,
            'subheading_bold': self.subheading_bold,
            'body_font_family': self.body_font_family,
            'body_font_size': self.body_font_size,
            'body_bold': self.body_bold,
            'show_lines_between_sections': self.show_lines_between_sections,
            'section_spacing': self.section_spacing,
            'left_margin': self.left_margin,
            'right_margin': self.right_margin,
            'top_margin': self.top_margin,
            'bottom_margin': self.bottom_margin,
            'header_text': self.header_text,
            'footer_text': self.footer_text,
            'template_style_json': self.template_style_json,
        }
