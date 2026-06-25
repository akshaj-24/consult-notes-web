from django.core.management.base import BaseCommand

from apps.patients.services import import_patient_seed


class Command(BaseCommand):
    help = 'Import or refresh the bundled patient seed CSV.'

    def handle(self, *args, **options):
        created, updated = import_patient_seed()
        self.stdout.write(self.style.SUCCESS(f'Imported patient seed: {created} created, {updated} updated.'))
