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
