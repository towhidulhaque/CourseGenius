from django.db import models

from server.apps.main.models import User
from server.apps.utility.base_mixin import BaseMixin
from server.apps.utility.blameable_mixin import BlameableMixin
from server.apps.utility.institute_mixin import InstituteMixin


class Course(BaseMixin, BlameableMixin, InstituteMixin):
    """Represents a course offered by an educational institute."""

    STATUS_CHOICES = (  # noqa: WPS115
        ('OPEN', 'Open'),
        ('DRAFT', 'Draft'),
        ('CLOSE', 'Close'),
    )

    name = models.CharField(max_length=100, help_text='Name of the course.')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    teacher = models.ForeignKey(
        User,
        related_name='teacher_course_map',
        on_delete=models.DO_NOTHING,
    )

    class Meta(object):
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        """Return string self name."""
        return self.name
