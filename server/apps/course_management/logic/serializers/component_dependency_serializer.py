from rest_framework import serializers

from server.apps.course_management.models.course_component import (
    CourseComponent,
)


class CourseComponentDependenciesSerializer(serializers.Serializer):
    """Serializer class for dependency add."""

    component_id = serializers.IntegerField()
    dependency_ids = serializers.ListField(child=serializers.IntegerField())

    def validate(self, attrs):
        """Validate dependency add request."""
        component_id = attrs.get('component_id')
        dependency_ids = attrs.get('dependency_ids', [])

        try:  # noqa: WPS229
            component = CourseComponent.objects.get(id=component_id)
            dependencies = CourseComponent.objects.exclude(id=component_id).filter(
                id__in=dependency_ids,
                course=component.course,
            )
        except CourseComponent.DoesNotExist:
            raise serializers.ValidationError('Invalid component or dependency IDs.')

        attrs['component'] = component
        attrs['dependencies'] = dependencies
        return attrs
