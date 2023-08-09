from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from gitdb.utils.encoding import force_text
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from server.apps.main.logic.serializers.user_serializer import (
    RegisterSerializer,
)
from server.apps.main.logic.services.register_service import RegisterService
from server.apps.main.models import User


class RegisterAPIView(CreateAPIView):
    """Register API."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request):
        """Add User."""
        serializer = self.serializer_class(data=request.data, many=False)
        if serializer.is_valid(raise_exception=True):
            user = RegisterService.register_user(serializer.validated_data)
            response_data = {
                'user': str(user.username),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEmailVerificationAPI(RetrieveAPIView):
    """User email verification API that verifies the user's email address."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        """
        Handle email verification process.

        This method validates the provided UID and token from the URL, and
        verifies if the token is valid for the user. If the token is valid,
        the user's email verification status is updated.

        Args:
            request (HttpRequest): The HTTP request object.
            uidb64 (str): Base64-encoded user ID.
            token (str): Email verification token.

        Returns:
            Response: HTTP response indicating the result of email verification.
        """
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = get_object_or_404(User, pk=uid)
        if default_token_generator.check_token(user, token):
            if user.is_email_confirmed:
                return Response(
                    {'message': 'Email is already verified.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Todo custom check if the verification link is within the valid time period
            RegisterService.verify_email(user)
            return Response(
                {'message': 'Email verified successfully.'},
                status=status.HTTP_200_OK,
            )
        return Response(
            {'message': 'Invalid/Expired verification token.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
