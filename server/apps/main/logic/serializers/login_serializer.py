from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    """User login serializers."""

    username = serializers.CharField()
    password = serializers.CharField()
