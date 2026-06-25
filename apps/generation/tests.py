from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.configdata.models import LLMModelConfig
from apps.consults.models import ConsultNote
from apps.patients.models import Patient

from .models import GenerationSession


class GenerationFlowTests(TestCase):
    def setUp(self):
        call_command('import_llm_models')
        call_command('import_patient_seed')
        self.user = User.objects.create_user(username='generator', password='StrongPassA1', is_approved=True)
        self.client.force_login(self.user)

    def test_generation_flow_creates_dummy_consult_note(self):
        patient = Patient.objects.first()
        session = GenerationSession.objects.create(user=self.user, selected_patient=patient)
        session.ensure_defaults()

        response = self.client.post(reverse('generation:generate', kwargs={'pk': session.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConsultNote.objects.filter(user=self.user).count(), 1)
        note = ConsultNote.objects.get(user=self.user)
        self.assertIn('MEDICAL ONCOLOGY CONSULT NOTE', note.note_text)
        self.assertTrue(note.docx_file.name)
        self.assertEqual(note.llm_model_key, LLMModelConfig.objects.first().model_key)
