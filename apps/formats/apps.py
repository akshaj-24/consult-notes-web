from django.apps import AppConfig


class FormatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.formats'
    verbose_name = 'Formats'

    def ready(self) -> None:
        from . import signals  # noqa: F401
