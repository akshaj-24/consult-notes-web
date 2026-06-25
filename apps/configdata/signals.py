from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import LLMModelConfig
from .services import import_model_configs


@receiver(post_migrate)
def ensure_model_catalog(sender, **kwargs):
    if sender.name != 'apps.configdata':
        return
    if not LLMModelConfig.objects.exists():
        import_model_configs()
