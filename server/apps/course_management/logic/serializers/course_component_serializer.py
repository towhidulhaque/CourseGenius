from django.db.models import Max
from rest_framework import serializers

from server.apps.course_management.models.course_component import (
    CourseComponent,
)


class CourseComponentSerializer(serializers.ModelSerializer):
    """
    Serializer for CourseComponent model.

    Handles serialization and deserialization of CourseComponent instances.
    Also includes validation for the serial number field.
    """

    class Meta(object):
        model = CourseComponent
        fields = (
            'id',
            'name',
            'serial_number',
        )
        read_only_fields = (
            'id',
        )
        extra_kwargs = {
            'serial_number': {'required': False},
        }

    def create(self, validated_data):
        """
        Create Component.

        If the serial number is not provided, calculate the next serial number
        based on the existing components of the associated course.
        """
        course = validated_data['course']
        if 'serial_number' not in validated_data:
            max_serial_number = CourseComponent.objects.filter(
                course=course,
            ).aggregate(Max('serial_number'))['serial_number__max'] or 0
            validated_data['serial_number'] = max_serial_number + 1
        return super().create(validated_data)
