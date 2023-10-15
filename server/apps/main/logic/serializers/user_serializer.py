from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from rest_framework import serializers

from server.apps.main.models import User
from server.apps.main.models.institute import Institute


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for new user register."""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    institute = serializers.PrimaryKeyRelatedField(queryset=Institute.objects.all(), required=True)

    class Meta(object):
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'institute',
            'is_faculty',
        )

    def validate(self, attrs):
        """Validate register user."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."},
            )
        validate_email(attrs['username'])
        return attrs


class MiniUserSerializer(serializers.ModelSerializer):
    """Serializer for user short info."""

    class Meta(object):
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user info."""

    class Meta(object):
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_admin',
            'is_institutional_admin',
            'institute',
            'created_at',
        )


class AdminUserModifySerializer(serializers.ModelSerializer):
    """Serializer for user modify by admin."""

    class Meta(object):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_verified',
            'is_admin',
            'is_active',
            'is_institutional_admin',
            'institute',
        )


class InstitutionalAdminUserModifySerializer(serializers.ModelSerializer):
    """Serializer for user modify by institutional admin."""

    class Meta(object):
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'is_verified',
            'is_active',
            'is_institutional_admin',
        )


class RegularUserModifySerializer(serializers.ModelSerializer):
    """Serializer for user modify by regular user."""

    class Meta(object):
        model = User
        fields = (
            'first_name',
            'last_name',
        )


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

    def validate(self, serialized_data):
        """Validate password change request."""
        if serialized_data['new_password'] != serialized_data['new_password2']:
            raise serializers.ValidationError({'new_password': "New password fields didn't match."})
        return serialized_data
