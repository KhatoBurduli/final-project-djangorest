from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView, UserDetailView, RecoveryQuestionView, PasswordResetView, EmailVerifyView, LogoutView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='user-register'),
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('me/', UserDetailView.as_view(), name='user-detail'),

    path('recovery-question/', RecoveryQuestionView.as_view(), name='recovery-question'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),

    path('verify-email/<uuid:token>/', EmailVerifyView.as_view(), name='verify-email'),
]
