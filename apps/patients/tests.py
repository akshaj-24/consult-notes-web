from apps.accounts.models import User

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Patient


class PatientSeedImportTests(TestCase):
    def test_import_patient_seed_creates_patients(self):
        call_command('import_patient_seed')
        self.assertGreaterEqual(Patient.objects.count(), 1)
        patient = Patient.objects.first()
        self.assertTrue(patient.mrn)
        self.assertTrue(patient.patient_name)


class PatientViewTests(TestCase):
    def setUp(self):
        call_command('import_patient_seed')
        self.user = User.objects.create_user(username='patientuser', password='StrongPassA1', is_approved=True)
        self.superuser = User.objects.create_superuser(username='rootpatient', password='StrongPassA1')

    def test_patient_create_page_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('patients:create'))
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_delete_patient(self):
        patient = Patient.objects.first()
        self.client.force_login(self.superuser)
        response = self.client.post(reverse('patients:delete', kwargs={'pk': patient.pk}))
        self.assertRedirects(response, reverse('patients:list'))
        self.assertFalse(Patient.objects.filter(pk=patient.pk).exists())
