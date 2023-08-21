# flake8: noqa RST210
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from server.apps.course_management.logic.serializers.component_dependency_serializer import (
    CourseComponentDependenciesSerializer,
)
from server.apps.course_management.logic.serializers.course_component_serializer import (
    CourseComponentSerializer,
)
from server.apps.course_management.logic.services.course_component_service import (
    CourseComponentService,
)
from server.apps.course_management.models.course import Course
from server.apps.course_management.models.course_component import (
    CourseComponent,
)
from server.apps.course_management.utils.permissions import (
    CourseComponentPermission,
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
        if CourseComponentPermission.user_has_permission(user, course):
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

        if CourseComponentPermission.user_has_permission(user, course):
            serializer.validated_data['course'] = course
            serializer.validated_data['institute'] = course.institute
            serializer.validated_data['created_by'] = user
            serializer.save()


class AddDependenciesView(APIView):
    """
    API view to add dependencies to a course component.

    - Admin users, institutional admins or teacher can add dependencies.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=CourseComponentDependenciesSerializer(many=False))
    def post(self, request, *args, **kwargs):
        """
        Add dependencies to a course component.

        Args:
            request: The HTTP request.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The API response.
        """
        user = request.user
        serializer = CourseComponentDependenciesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        CourseComponentService.add_dependency(serializer.validated_data, user)

        return Response(
            {'detail': 'Dependencies added successfully.'},
            status=status.HTTP_201_CREATED,
        )
