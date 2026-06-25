from django.apps import AppConfig


class ConfigdataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.configdata'
    verbose_name = 'Config Data'

    def ready(self) -> None:
        from . import signals  # noqa: F401
