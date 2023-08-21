from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, get_object_or_404

from server.apps.course_management.logic.serializers.course_component_serializer import (
    CourseComponentSerializer,
)
from server.apps.course_management.models.course import Course
from server.apps.course_management.models.course_component import (
    CourseComponent,
)


class CourseComponentListCreateView(ListCreateAPIView):
    """
    API view to list and create course components.

    - Admin users see all course components.
    - Institutional admins see components for their institute only.
    - Faculty members see components for their courses.
    """

    serializer_class = CourseComponentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get component list."""
        user = self.request.user
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        if user.is_admin or user.is_staff:
            return CourseComponent.objects.filter(course=course)
        if user.is_institutional_admin and course.institute == user.institute:
            return CourseComponent.objects.filter(course=course)
        if user.is_faculty and course.teacher == user:
            return CourseComponent.objects.filter(course=course)
        return CourseComponent.objects.none()

    def perform_create(self, serializer):
        """
        Create a new course component based on the user's role and course context.

        Admin users and institutional admins can create components for the course.
        Faculty members can create components for their courses.
        """
        user = self.request.user
        course_id = self.kwargs.get('course_id')

        course = get_object_or_404(Course, id=course_id)

        if user.is_staff or user.is_admin or (user.is_institutional_admin and course.institute == user.institute) or (user.is_faculty and course.teacher == user):  # noqa: WPS222, E501, WPS221
            serializer.validated_data['course'] = course
            serializer.validated_data['institute'] = course.institute
            serializer.validated_data['created_by'] = user
            serializer.save()
