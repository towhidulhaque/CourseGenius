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
