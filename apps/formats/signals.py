from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import User

from .models import NoteFormat


@receiver(post_save, sender=User)
def ensure_default_note_format(sender, instance, created, **kwargs):
    if not created:
        return

    note_format = NoteFormat.objects.create(
        user=instance,
        name='Default Format',
        is_active=True,
    )
    sender.objects.filter(pk=instance.pk, active_format__isnull=True).update(active_format=note_format)
