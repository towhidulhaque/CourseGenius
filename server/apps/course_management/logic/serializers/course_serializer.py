from rest_framework import serializers

from server.apps.course_management.models.course import Course
from server.apps.main.logic.serializers.user_serializer import (
    MiniUserSerializer,
)
from server.apps.main.models import User


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.

    Fields:
    - id (read-only): The unique identifier for the course.
    - name: The name of the course.
    - status: The status of the course (OPEN, DRAFT, CLOSE).
    - institute: The institute associated with the course.
    - created_by: The user who created the course.
    """

    teacher = serializers.SerializerMethodField()

    class Meta(object):
        model = Course
        fields = (
            'id',
            'name',
            'status',
            'institute',
            'teacher',
            'created_by',
        )
        read_only_fields = (
            'id',
        )

    def get_teacher(self, objt):  # noqa: WPS615
        """Teacher field populate."""
        if isinstance(objt.teacher, User):
            return MiniUserSerializer(objt.teacher).data
        return objt.teacher
