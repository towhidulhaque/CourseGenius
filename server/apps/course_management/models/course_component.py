from django.db import models

from server.apps.course_management.models.course import Course
from server.apps.utility.base_mixin import BaseMixin
from server.apps.utility.blameable_mixin import BlameableMixin
from server.apps.utility.institute_mixin import InstituteMixin


class CourseComponent(BaseMixin, BlameableMixin, InstituteMixin):
    """Represents a component of a course."""

    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course,
        on_delete=models.DO_NOTHING,
        related_name='course_components_map',
    )
    serial_number = models.PositiveIntegerField()
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

    class Meta(object):
        verbose_name = 'Course Component'
        verbose_name_plural = 'Course Components'
        unique_together = ('course', 'serial_number')

    def __str__(self):
        """Return string self name."""
        return self.name
