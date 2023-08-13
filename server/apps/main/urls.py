# flake8: noqa WPS201

from typing import List

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from server.apps.main.views.institute_api_view import InstituteListCreateView
from server.apps.main.views.login_api_view import UserLoginAPI
from server.apps.main.views.register_api_view import RegisterAPIView, UserEmailVerificationAPI

app_name = 'main'

urlpatterns: List[str] = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='user_register'),
    path('email-verify/<str:uidb64>/<str:token>/', UserEmailVerificationAPI.as_view(), name='email_verify'),
    path('login/', UserLoginAPI.as_view(), name='user_login'),
    # institution
    path('institutes/', InstituteListCreateView.as_view(), name='user_login'),
]
