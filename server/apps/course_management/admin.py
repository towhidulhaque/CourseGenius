from django.contrib import admin

from server.apps.course_management.models.course import Course
from server.apps.course_management.models.course_component import (
    CourseComponent,
)

admin.site.register(Course)
admin.site.register(CourseComponent)
