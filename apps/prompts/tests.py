from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User

from .models import Prompt


class PromptSuperuserAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='promptowner', password='StrongPassA1', is_approved=True)
        self.superuser = User.objects.create_superuser(username='rootprompt', password='StrongPassA1')
        self.prompt = Prompt.objects.create(
            user=self.owner,
            name='Owner Prompt',
            prompt_type=Prompt.PromptType.SYSTEM,
            content='hello',
            is_active=True,
        )

    def test_superuser_can_view_all_prompts(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('prompts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Owner Prompt')

    def test_superuser_can_delete_any_prompt(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse('prompts:delete', kwargs={'pk': self.prompt.pk}))
        self.assertRedirects(response, reverse('prompts:list'))
        self.assertFalse(Prompt.objects.filter(pk=self.prompt.pk).exists())
