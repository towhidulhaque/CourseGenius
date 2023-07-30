import json
from pathlib import Path
from typing import List

from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand

from server.apps.main.models.permission_category import PermissionCategory


class Command(BaseCommand):
    """Load default permission category."""

    def create_permission_category(self, permission_data) -> None:
        """Create permission categories."""
        category, created = PermissionCategory.objects.get_or_create(
            name=permission_data['name'],
        )

        permissions = self.get_permissions_ids(permission_data)
        if permissions:
            category.permissions.clear()
            category.permissions.add(*permissions)

    def get_permissions_ids(self, group_data) -> List[int]:
        """Add permission by ids."""
        return list(
            Permission.objects.filter(
                codename__in=group_data['permissions'],
            ).values_list('id', flat=True),
        )

    def load_permission_category(self) -> None:
        """Load permissions."""
        script_location = Path(__file__).absolute().parent
        file_location = script_location / './dump/application_default_permissions_category.json'  # NOQA : E501
        permission_file = file_location.open()
        data_dict = json.load(permission_file)
        permission_file.close()
        PermissionCategory.objects.all().delete()
        for permission_data in data_dict:
            print(permission_data['name'])  # noqa: WPS421
            self.create_permission_category(permission_data)

    def handle(self, *args, **options):  # noqa: WPS213, WPS110
        """Command handler."""
        self.load_permission_category()
