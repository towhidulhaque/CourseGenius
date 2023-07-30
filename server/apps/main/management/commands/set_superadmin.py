from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from server.apps.main.models import User


class Command(BaseCommand):
    """Management class for setting a user as superadmin."""

    def add_arguments(self, parser):
        """Adds commandline arguments to the parser."""
        parser.add_argument('username', type=str)

    def set_superadmin(self, username) -> None:
        """Set super admin."""
        user = User.objects.get(username=username)
        user.is_superuser = True
        permissions = Permission.objects.filter(
        ).values_list('id', flat=True)

        user.user_permissions.add(*permissions)
        user.save()

    def handle(self, *args, **options):  # noqa: WPS213, WPS110
        """Command handler."""
        self.set_superadmin(options['username'])
