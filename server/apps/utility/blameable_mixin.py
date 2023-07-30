# -*- coding: utf-8 -*-

from django.db import models

# local imports


class BlameableMixin(models.Model):
    """Base fields: created, modified, version."""

    created_by = models.ForeignKey(
        'main.User',
        related_name='%(app_label)s_%(class)s_created_by_user_related',  # NOQA : WPS323 NOQA : E501
        on_delete=models.CASCADE,
        null=True,
    )
    updated_by = models.ForeignKey(
        'main.User',
        related_name='%(app_label)s_%(class)s_updated_by_user_related',  # NOQA : WPS323 NOQA : E501
        on_delete=models.CASCADE,
        null=True,
    )
    deleted_by = models.ForeignKey(
        'main.User',
        related_name='%(app_label)s_%(class)s_deleted_by_user_related',  # NOQA : WPS323 NOQA : E501
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta(object):
        abstract = True

    def __str__(self) -> str:
        """Return string self id."""
        return str(self.pk)
