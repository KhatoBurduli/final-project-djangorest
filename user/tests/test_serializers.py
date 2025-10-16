from django.test import TestCase
from user.serializers import (
    UserRegisterSerializer,
    RecoveryQuestionSerializer,
    PasswordResetSerializer,
    EmailVerificationSerializer
)
from user.models import CustomUser, PasswordRecoveryToken, EmailVerificationToken
from django.utils import timezone
from datetime import timedelta
import uuid


class UserRegisterSerializerTest(TestCase):
    def test_valid_registration(self):
        data = {
            "username": "john",
            "email": "john@example.com",
            "password": "StrongPass123!",
            "password2": "StrongPass123!",
            "recovery_question": "Your pet's name?",
            "recovery_answer": "Rex",
            "age": 25
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertFalse(user.is_active)  # user inactive until verified
        self.assertTrue(user.recovery_answer_hash)
        self.assertEqual(user.email, "john@example.com")

    def test_invalid_registration_password_mismatch(self):
        data = {
            "username": "jane",
            "email": "jane@example.com",
            "password": "abc12345",
            "password2": "abc54321",
            "recovery_question": "Question?",
            "recovery_answer": "Ans",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class RecoveryAndResetSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="john",
            email="john@example.com",
            password="StrongPass123!"
        )
        self.user.set_recovery_answer("Rex")
        self.user.save()

    def test_recovery_question_valid_username(self):
        data = {"username": "john"}
        serializer = RecoveryQuestionSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save()
        self.assertIn("recovery_question", result)
        self.assertIn("token", result)

    def test_password_reset_valid(self):
        token = PasswordRecoveryToken.objects.create(
            user=self.user,
            expires_at=timezone.now() + timedelta(minutes=15)
        )
        data = {
            "token": str(token.token),
            "recovery_answer": "Rex",
            "new_password": "NewStrongPass123!",
            "confirm_password": "NewStrongPass123!",
        }
        serializer = PasswordResetSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.assertFalse(PasswordRecoveryToken.objects.filter(id=token.id).exists())

    def test_password_reset_invalid_answer(self):
        token = PasswordRecoveryToken.objects.create(
            user=self.user,
            expires_at=timezone.now() + timedelta(minutes=15)
        )
        data = {
            "token": str(token.token),
            "recovery_answer": "Wrong",
            "new_password": "NewStrongPass123!",
            "confirm_password": "NewStrongPass123!",
        }
        serializer = PasswordResetSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class EmailVerificationSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="john",
            email="john@example.com",
            password="StrongPass123!",
            is_active=False
        )
        self.token = EmailVerificationToken.objects.create(
            user=self.user,
            expires_at=timezone.now() + timedelta(hours=1)
        )

    def test_valid_token(self):
        data = {"token": str(self.token.token)}
        serializer = EmailVerificationSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
