import random
import string
import uuid
from typing import final

from django.contrib.auth.models import AbstractUser, Group
from django.db import models

max_length_large = 255
max_length_medium = 50
max_length_small = 20


def get_random_activation_code():
    """Random number generator method."""
    return ''.join(random.choice(string.digits) for _ in range(max_length_small))  # NOQA S311


@final
class User(AbstractUser):
    """
    This model is used just as an example.

    With it, we show how one can:
    - Use fixtures and factories
    - Use migrations testing

    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(Group)
    activation_code = models.CharField(
        max_length=max_length_medium,
        blank=True,
        default=get_random_activation_code,
    )
    show_tips = models.BooleanField(default=True)
    is_email_confirmed = models.BooleanField(default=False)

    class Meta(object):
        """Meta class."""

        verbose_name = 'User'  # You can probably use `gettext` for this
        verbose_name_plural = 'Users'
        permissions = [
            ('change_user_group', 'Can change user group'),
            ('manage_all_employee', 'Can manage all employee'),
        ]

    def __str__(self) -> str:
        """All django models should have this method."""
        return str(self.id)
