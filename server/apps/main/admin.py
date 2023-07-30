from django.contrib import admin

from server.apps.main.models.email_template import EmailTemplate
from server.apps.main.models.permission_category import PermissionCategory
from server.apps.main.models.permission_group import PermissionGroup
from server.apps.main.models.user import User

admin.site.register(User)
admin.site.register(PermissionGroup)
admin.site.register(PermissionCategory)
admin.site.register(EmailTemplate)
