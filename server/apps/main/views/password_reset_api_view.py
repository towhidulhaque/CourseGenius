from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from server.apps.main.logic.serializers.password_reset_serializer import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
)
from server.apps.main.logic.services.password_reset_service import (
    PasswordResetService,
)
from server.apps.main.models import User


class PasswordResetRequestAPIView(CreateAPIView):
    """
    API view for handling password reset requests.

    Users provide their email address to receive a password reset link.

    Methods:
    - **create(request, *args, **kwargs)**: Handles the password reset request
    and sends a reset email to the user.

    Attributes:
    - **serializer_class**: Serializer class for handling password reset request data.
    - **permission_classes**: Specifies the permission classes for the
    view (AllowAny for password reset requests).
    """

    serializer_class = PasswordResetRequestSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Handle the request for password reset and send a reset email to the user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: HTTP response indicating the result of the password reset request.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user and user.is_active:
            PasswordResetService.handle_password_reset_request(user)
        # sending all same message to protect internal information
        return Response(
            {'message': 'Password reset link sent successfully.'},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(CreateAPIView):
    """
    API view for handling password reset confirmations.

    Users confirm their password reset by providing a new password along
    with a verification link.

    Methods:
    - **create(request, *args, **kwargs)**: Handles the password reset
    confirmation and updates the user's password.

    Attributes:
    - **serializer_class**: Serializer class for handling password
    reset confirmation data.
    - **permission_classes**: Specifies the permission classes for the
    view (AllowAny for password reset requests).
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Handle the password reset confirmation and update the user's password.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: HTTP response indicating the result of the password reset confirmation.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        new_password = serializer.validated_data['new_password']

        PasswordResetService.reset_password(user, new_password)

        return Response(
            {'message': 'Password reset successfully.'},
            status=status.HTTP_200_OK,
        )
