# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group

# Local imports
from server.apps.utility.base_mixin import BaseMixin
from server.apps.utility.blameable_mixin import BlameableMixin

# Django imports

max_length_large = 500
max_length_medium = 255
max_length_small = 8
max_height = 2024
max_width = 2024
image_height = 50
image_width = 100


class PermissionGroup(BaseMixin, BlameableMixin, Group):
    """Extends django user with extra optional fields."""

    class Meta(object):
        verbose_name = 'PermissionGroup'
        verbose_name_plural = 'PermissionGroups'

    def __str__(self):
        """Return string self username."""
        return self.id
