# flake8: noqa WPS201

from typing import List

from django.urls import path

from server.apps.course_management.views.course_api_view import CourseListCreateView

app_name = 'course_management'

urlpatterns: List[str] = [
    path('courses/', CourseListCreateView.as_view(), name='courses'),
]
