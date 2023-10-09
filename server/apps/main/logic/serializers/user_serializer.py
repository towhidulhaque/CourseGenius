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
            'is_admin',
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
            'is_institutional_admin',
            'institute',
        )


class RegularUserModifySerializer(serializers.ModelSerializer):
    """Serializer for user modify by regular user."""

    class Meta(object):
        model = User
        fields = (
            'first_name',
            'last_name',
        )
