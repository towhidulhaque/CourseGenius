from django.utils import timezone


class CourseComponentService(object):
    """Course component service."""

    @classmethod
    def add_dependency(cls, validated_data, user) -> None:
        """Add dependencies to component."""
        component = validated_data.get('component')
        dependencies = validated_data.get('dependencies')
        for dependency in dependencies:
            component.prerequisites.add(dependency)
        component.updated_at = timezone.now()
        component.updated_by = user
        component.save()
