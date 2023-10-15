from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from gitdb.utils.encoding import force_text
from rest_framework import serializers

from server.apps.main.models import User


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer for requesting a password reset."""

    email = serializers.EmailField(write_only=True, required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming a password reset."""

    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):  # noqa: WPS210
        """Validate the password reset confirmation request."""
        uidb64 = attrs['uidb64']
        token = attrs['token']
        new_password = attrs['new_password']
        confirm_new_password = attrs['confirm_new_password']

        try:  # noqa: WPS229
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid verification link.')

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError('Invalid or expired verification token.')

        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                {'confirm_new_password': "New password fields didn't match."},
            )

        attrs['user'] = user
        return attrs
