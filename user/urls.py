from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView, UserDetailView

urlpatterns = [
    # Registration & login
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # User self-only endpoint
    path('me/', UserDetailView.as_view(), name='user-detail'),
]
