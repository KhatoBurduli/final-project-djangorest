from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserRegisterSerializer, EmailVerificationSerializer

# Register (anyone can create)
class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email verification link sent to your email."})


# Retrieve, update, delete logged-in user's profile
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Always return the logged-in user's object
        return self.request.user

# user/views.py
from rest_framework import generics
from rest_framework.response import Response
from .serializers import RecoveryQuestionSerializer, PasswordResetSerializer

# Get recovery question + token
class RecoveryQuestionView(generics.CreateAPIView):
    serializer_class = RecoveryQuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result)


# Reset password
class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"detail": "Password reset successfully."})


class EmailVerifyView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request, token, *args, **kwargs):
        serializer = self.get_serializer(data={'token': token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email verified successfully. You can now login."})
