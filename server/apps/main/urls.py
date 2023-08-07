# flake8: noqa WPS201

from typing import List

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from server.apps.main.views.register_api_view import RegisterAPIView

app_name = 'main'

urlpatterns: List[str] = [
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/register/', RegisterAPIView.as_view(), name='user-register'),

]
