from rest_framework import serializers

from server.apps.main.models.institute import Institute


class InstituteSerializer(serializers.ModelSerializer):
    """Serializer for new institute."""

    class Meta(object):
        model = Institute
        fields = (
            'id',
            'name',
            'description',
        )
        read_only_fields = (
            'id',
        )
