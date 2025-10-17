from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password
import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    recovery_question = models.CharField(max_length=255, blank=True, null=True)
    recovery_answer_hash = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def set_recovery_answer(self, raw_answer):
        self.recovery_answer_hash = make_password(raw_answer)

    def check_recovery_answer(self, raw_answer):
        if not self.recovery_answer_hash:
            return False
        return check_password(raw_answer, self.recovery_answer_hash)

    def __str__(self):
        return self.username


class PasswordRecoveryToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recovery_tokens')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)  # token valid for 15 minutes
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.username} - {self.token}"


class EmailVerificationToken(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='email_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
