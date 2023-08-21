from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView

from server.apps.course_management.logic.serializers.course_serializer import (
    CourseSerializer,
)
from server.apps.course_management.models.course import Course


class CourseListCreateView(ListCreateAPIView):
    """
    API view to list and create courses.

    - Admin users see all courses regardless of status.
    - Institutional admins see courses for their institute only, regardless of status.
    - Faculty members see courses where they are the teacher, regardless of status.
    """

    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['created_at', 'id']
    filterset_fields = {
        'id': ['exact'],
        'status': ['exact'],
        'institute': ['exact'],
        'teacher': ['exact'],
        'created_at': ['lte', 'gte'],
        'updated_at': ['lte', 'gte'],
    }

    def get_queryset(self):
        """Queryset for courses."""
        user = self.request.user

        # Admin users see all courses
        if user.is_admin or user.is_staff:
            return Course.objects.select_related('teacher').all()

        # Institutional admins see courses for their institute only
        if user.is_institutional_admin:
            return Course.objects.filter(institute=user.institute).select_related('teacher')

        # Faculty members see courses where they are the teacher
        if user.is_faculty:
            return Course.objects.filter(teacher=user).select_related('teacher')

        return Course.objects.none().select_related('teacher')

    def perform_create(self, serializer):
        """
        Create a new course based on the user's role and institute context.

        Admin users can create courses for any institute.
        Institutional admins and faculty members can create courses for their own institute.
        """
        user = self.request.user

        # Admin users can create courses for any institute
        if user.is_staff or user.is_admin:
            serializer.save(created_by=user)

        # Institutional admins and faculty members can create courses for their institute
        elif user.is_institutional_admin:
            serializer.save(created_by=user, institute=user.institute)
        elif user.is_faculty:
            serializer.save(created_by=user, institute=user.institute, teacher=user)
