# flake8: noqa WPS202
import copy
from typing import Dict, List

from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """Custom django model permission override."""

    perms_map: Dict[str, List[str]]

    def __init__(self):
        """Override permission mapping."""
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = [
            '%(app_label)s.view_%(model_name)s',  # noqa: WPS323
        ]
