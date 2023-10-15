from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing user password."""

    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, cpwd):
        """Validation of current password."""
        request = self.context.get('request')
        user = request.user

        if not authenticate(request=request, username=user.username, password=cpwd):
            raise serializers.ValidationError('Incorrect old password.')
        return cpwd

    def validate(self, attrs):
        """Validate password change request."""
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': "New password fields didn't match."})
        return attrs
