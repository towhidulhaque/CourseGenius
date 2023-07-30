# flake8: noqa E501
import json
from pathlib import Path
from typing import Any

from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from server.apps.main.models.permission_group import PermissionGroup


class Command(BaseCommand):
    """Import permissions in recruitment database."""

    def create_group(self, group_data) -> None:
        """Create group."""
        group, created = PermissionGroup.objects.get_or_create(
            name=group_data['group_name'],
        )
        permissions = self.get_permissions_ids(group_data)
        if permissions:
            group.permissions.clear()
            group.permissions.add(*permissions)

    def get_permissions_ids(self, group_data) -> Any:  # type: ignore[misc] # noqa: F821
        """Add permission by ids."""
        return Permission.objects.filter(
            codename__in=group_data['permissions'],
        ).values_list('id', flat=True)

    def load_groups(self) -> None:
        """Load permissions."""
        script_location = Path(__file__).absolute().parent
        file_location = script_location / './dump/application_default_groups.json'  # NOQA : E501
        permission_file = file_location.open()
        data_dict = json.load(permission_file)  # deserialises it
        permission_file.close()

        for group_data in data_dict:
            print(group_data['group_name'])  # noqa: WPS421
            self.create_group(group_data)

    def handle(self, *args, **options):  # noqa: WPS213, WPS110
        """Command handler."""
        self.load_groups()
