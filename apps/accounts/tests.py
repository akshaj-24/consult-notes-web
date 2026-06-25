from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import User


class AccountFlowTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_creates_unapproved_user_with_default_format(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "username": "newuser",
                "password1": "StrongPassA1",
                "password2": "StrongPassA1",
                "challenge_answer": "A",
            },
        )

        self.assertRedirects(response, reverse("accounts:login"))
        user = User.objects.get(username="newuser")
        self.assertFalse(user.is_approved)
        self.assertIsNotNone(user.active_format)
        self.assertEqual(user.active_format.name, "Default Format")

    def test_unapproved_user_is_redirected_to_waiting_page(self):
        user = User.objects.create_user(
            username="pendinguser",
            password="StrongPassA1",
            is_approved=False,
        )

        self.client.force_login(user)
        response = self.client.get(reverse("core:dashboard"))

        self.assertRedirects(response, reverse("accounts:awaiting_approval"))

    def test_approved_user_can_access_dashboard(self):
        user = User.objects.create_user(
            username="approveduser",
            password="StrongPassA1",
            is_approved=True,
        )

        self.client.force_login(user)
        response = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.status_code, 200)
