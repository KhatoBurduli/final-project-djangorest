from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser, EmailVerificationToken
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    recovery_answer = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'password', 'password2',
            'recovery_question', 'recovery_answer', 'profile_pic', 'age'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        raw_answer = validated_data.pop('recovery_answer')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_recovery_answer(raw_answer)
        user.is_active = False
        user.save()

        token = EmailVerificationToken.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(hours=24)
        )

        # Send verification email
        verification_link = f"{settings.FRONTEND_URL}/api/verify-email/{token.token}/"
        send_mail(
            subject="Verify your Recipe App email",
            message=f"Hi {user.username},\n\nClick this link to verify your email:\n{verification_link}\nLink expires in 24 hours.",
            from_email=None,  # uses DEFAULT_FROM_EMAIL in settings
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user



# user/serializers.py
from rest_framework import serializers
from .models import CustomUser, PasswordRecoveryToken
from django.utils import timezone
from datetime import timedelta
import uuid

class RecoveryQuestionSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            user = CustomUser.objects.get(username=value)
            self.context['user'] = user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No user found with this username.")
        return value

    def create(self, validated_data):
        user = self.context['user']
        # create a one-time token for password reset
        token = PasswordRecoveryToken.objects.create(
            user=user,
            token=uuid.uuid4(),
            expires_at=timezone.now() + timedelta(minutes=15)
        )
        return {
            "recovery_question": user.recovery_question,
            "token": str(token.token)
        }


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    recovery_answer = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        try:
            token_obj = PasswordRecoveryToken.objects.get(token=attrs['token'])
        except PasswordRecoveryToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid or expired token."})

        if token_obj.is_expired():
            raise serializers.ValidationError({"token": "Token has expired."})

        # ✅ Use check_recovery_answer instead of accessing non-existent field
        if not token_obj.user.check_recovery_answer(attrs['recovery_answer']):
            raise serializers.ValidationError({"recovery_answer": "Incorrect recovery answer."})

        attrs['user'] = token_obj.user
        attrs['token_obj'] = token_obj
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        # delete token after use
        self.validated_data['token_obj'].delete()
        return user


# user/serializers.py
class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate_token(self, value):
        try:
            token_obj = EmailVerificationToken.objects.get(token=value)
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")

        if token_obj.is_expired():
            raise serializers.ValidationError("Token expired.")

        self.context['token_obj'] = token_obj
        return value

    def save(self):
        token_obj = self.context['token_obj']
        user = token_obj.user
        user.is_active = True
        user.save()
        token_obj.delete()
        return user
