from django.core.management.base import BaseCommand

from apps.configdata.services import import_model_configs


class Command(BaseCommand):
    help = 'Import or refresh the bundled LLM model catalog.'

    def handle(self, *args, **options):
        created, updated = import_model_configs()
        self.stdout.write(self.style.SUCCESS(f'Imported model catalog: {created} created, {updated} updated.'))
