# -*- coding: utf-8 -*-

from concurrency.fields import IntegerVersionField
from django.db import models

# local imports


class BaseMixin(models.Model):  # type: ignore
    """Base fields: deleted at."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    version = IntegerVersionField()

    class Meta(object):
        abstract = True

    def __str__(self) -> str:
        """Return string self id."""
        return str(self.pk)

    def is_deleted(self):
        """Utility function to check deleted flag."""
        return self.deleted_at is not None
