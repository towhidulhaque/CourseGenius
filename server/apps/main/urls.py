# flake8: noqa WPS201

from typing import List

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from server.apps.main.views.change_password_api_view import ChangePasswordAPIView
from server.apps.main.views.institute_api_view import InstituteListCreateView
from server.apps.main.views.login_api_view import UserLoginAPI
from server.apps.main.views.password_reset_api_view import PasswordResetRequestAPIView, PasswordResetConfirmAPIView
from server.apps.main.views.register_api_view import RegisterAPIView, UserEmailVerificationAPI
from server.apps.main.views.user_api_view import UserListView, UserModifyView

app_name = 'main'

urlpatterns: List[str] = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterAPIView.as_view(), name='user_register'),
    path('email-verify/<str:uidb64>/<str:token>/', UserEmailVerificationAPI.as_view(), name='email_verify'),
    path('login/', UserLoginAPI.as_view(), name='user_login'),
    path('password-change/', ChangePasswordAPIView.as_view(), name='password_change'),
    path('password-reset/request/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    # institution
    path('institutes/', InstituteListCreateView.as_view(), name='user_login'),
    # user list manage
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<uuid:pk>/', UserModifyView.as_view(), name='user_modify'),
]
