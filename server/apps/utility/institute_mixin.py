from django.db import models


class InstituteMixin(models.Model):
    """Mixin to add Institute foreign key to models."""

    institute = models.ForeignKey(
        'main.Institute',
        related_name='%(app_label)s_%(class)s_institute_user_related',  # NOQA : WPS323 NOQA : E501
        on_delete=models.CASCADE,
        null=False,
    )

    class Meta(object):
        abstract = True

    def __str__(self) -> str:
        """Return string self id."""
        return str(self.pk)
