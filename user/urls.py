from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView, UserDetailView
from .views import RecoveryQuestionView, PasswordResetView

urlpatterns = [
    # Registration & login
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # User self-only endpoint
    path('me/', UserDetailView.as_view(), name='user-detail'),

    path('recovery-question/', RecoveryQuestionView.as_view(), name='recovery-question'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
]
