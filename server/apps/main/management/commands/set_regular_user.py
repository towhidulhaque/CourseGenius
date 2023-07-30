import logging

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from server.apps.main.models import User

logger = logging.getLogger('django')


class Command(BaseCommand):
    """Management class for setting user permission to all users."""

    def add_arguments(self, parser):
        """Adds commandline arguments to the parser."""
        parser.add_argument('groupname', type=str)

    def set_regular_user(self, groupname) -> None:
        """Set regular user permission."""
        user_group = Group.objects.filter(name=groupname).first()
        users = User.objects.all().values_list('id', flat=True)
        if user_group:
            user_group.user_set.add(*users)  # type:ignore
            logger.info('group {groupname} added to all users.'.format(
                groupname=groupname,
            ))
        else:
            logger.info('group {groupname} not found'.format(groupname=groupname))

    def handle(self, *args, **options):  # noqa: WPS213, WPS110
        """Command handler."""
        self.set_regular_user(options['groupname'])
