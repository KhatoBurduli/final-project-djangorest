from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from user.models import CustomUser, EmailVerificationToken, PasswordRecoveryToken


class UserViewTests(APITestCase):

    def test_register_user(self):
        url = reverse("user-register")
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "recovery_question": "Your pet's name?",
            "recovery_answer": "Rex",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)

    def test_me_endpoint_requires_auth(self):
        url = reverse("user-detail")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        user = CustomUser.objects.create_user(username="testuser", password="1234pass")
        self.client.force_authenticate(user=user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_verification_view(self):
        user = CustomUser.objects.create_user(username="john", password="StrongPass123!", is_active=False)
        token = EmailVerificationToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(hours=1)
        )
        url = reverse("verify-email", args=[str(token.token)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_recovery_question_view(self):
        user = CustomUser.objects.create_user(username="john", password="StrongPass123!")
        user.set_recovery_answer("Rex")
        user.save()
        url = reverse("recovery-question")
        response = self.client.post(url, {"username": "john"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("recovery_question", response.data)

    def test_reset_password_view(self):
        user = CustomUser.objects.create_user(username="john", password="StrongPass123!")
        user.set_recovery_answer("Rex")
        user.save()
        token = PasswordRecoveryToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=15)
        )
        url = reverse("reset-password")
        payload = {
            "token": str(token.token),
            "recovery_answer": "Rex",
            "new_password": "NewStrongPass123!",
            "confirm_password": "NewStrongPass123!"
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)

    def test_logout_view(self):
        # Create a user
        user = CustomUser.objects.create_user(username="john", password="StrongPass123!")

        # Obtain access and refresh tokens
        token_url = reverse("token-obtain-pair")
        response = self.client.post(token_url, {"username": "john", "password": "StrongPass123!"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data["access"]
        refresh = response.data["refresh"]

        # Logout (blacklist refresh token)
        logout_url = reverse("logout")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = self.client.post(logout_url, {"refresh": refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to refresh access token using blacklisted refresh
        refresh_url = reverse("token-refresh")
        response = self.client.post(refresh_url, {"refresh": refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

