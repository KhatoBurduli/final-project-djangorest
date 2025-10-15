from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # unique email for verification
    recovery_question = models.CharField(max_length=255, blank=True, null=True)
    recovery_answer = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    # New fields
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    # keep username as login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # email is required

    def __str__(self):
        return self.username

