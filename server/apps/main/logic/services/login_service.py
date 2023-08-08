from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from server.apps.main.models import User


class LoginService(object):
    """Service class for user login related logic."""

    @classmethod
    def authenticate_user(cls, validated_data):  # noqa: WPS212
        """Authenticate user and generate JWT token."""
        username = validated_data['username']
        password = validated_data['password']

        user = User.objects.filter(username=username).first()
        if not user:
            return {
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': {'message': 'Authentication failed.'},
            }
        if not user.check_password(password):
            return {
                'status': status.HTTP_401_UNAUTHORIZED,
                'data': {'message': 'Authentication failed.'},
            }
        if not user.is_active:
            return {
                'status': status.HTTP_403_FORBIDDEN,
                'data': {
                    'user': str(user.username),
                    'status': 'Inactive',
                    'message': 'Your account is inactive. Please activate your account',
                },
            }
        if not user.is_verified:
            return {
                'status': status.HTTP_403_FORBIDDEN,
                'data': {
                    'user': str(user.username),
                    'status': 'Not Verified',
                    'message': 'Please verify your email via admin',
                },
            }
        if not user.is_email_confirmed:
            return {
                'status': status.HTTP_403_FORBIDDEN,
                'data': {
                    'user': str(user.username),
                    'status': 'Inactive',
                    'message': 'Please confirm your email',
                },
            }

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        return {
            'status': status.HTTP_200_OK,
            'data': tokens,
        }
