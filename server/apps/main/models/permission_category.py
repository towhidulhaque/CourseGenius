from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

max_length_large = 2000


class PermissionCategory(models.Model):
    """Custom permission category."""

    name = models.CharField(
        _('name'),
        max_length=max_length_large,
        unique=True,
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )

    class Meta(object):
        verbose_name = 'PermissionCategory'
        verbose_name_plural = 'PermissionCategories'

    def __str__(self) -> str:
        """Return string self.pk."""
        return str(self.pk)
