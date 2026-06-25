from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from apps.accounts.models import User

from .models import Prompt

DEFAULT_PROMPTS = {
    Prompt.PromptType.SYSTEM: {
        'name': 'Default System Prompt',
        'description': 'Baseline system instructions for consult note generation.',
        'content': 'You are generating an oncology-style consult note. Preserve clear headings, concise clinical language, and a practical treatment plan.',
    },
    Prompt.PromptType.USER: {
        'name': 'Default User Prompt',
        'description': 'Baseline user prompt for turning patient data into a note.',
        'content': 'Write a complete consult note from the patient data provided. Include past history, medications, allergies, social history, family history, HPI, investigations, and assessment/plan.',
    },
    Prompt.PromptType.EDIT: {
        'name': 'Default Edit Prompt',
        'description': 'Baseline prompt for note regeneration and edits.',
        'content': 'Revise the existing consult note using the requested edits while preserving the overall note structure and clinically relevant details.',
    },
}


def ensure_default_prompts_for_user(user: User) -> None:
    for prompt_type, payload in DEFAULT_PROMPTS.items():
        if Prompt.objects.filter(user=user, prompt_type=prompt_type).exists():
            continue
        Prompt.objects.create(user=user, prompt_type=prompt_type, is_active=True, **payload)


@receiver(post_save, sender=User)
def ensure_default_prompts(sender, instance, created, **kwargs):
    if not created:
        return
    ensure_default_prompts_for_user(instance)


@receiver(post_migrate)
def ensure_missing_default_prompts(sender, **kwargs):
    if sender.name != 'apps.prompts':
        return
    for user in User.objects.all():
        ensure_default_prompts_for_user(user)
