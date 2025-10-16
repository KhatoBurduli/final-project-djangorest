from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserRegisterSerializer

# Register (anyone can create)
class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # TODO: send email verification link here


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
