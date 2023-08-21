# flake8: noqa WPS201

from typing import List

from django.urls import path

from server.apps.course_management.views.course_api_view import CourseListCreateView
from server.apps.course_management.views.course_component_api_view import CourseComponentListCreateView, \
    AddDependenciesView

app_name = 'course_management'

urlpatterns: List[str] = [
    path('courses/', CourseListCreateView.as_view(), name='courses'),
    path('courses/<int:course_id>/components/', CourseComponentListCreateView.as_view(), name='course_components'),
    path('components/add-dependencies/', AddDependenciesView.as_view(), name='add_component_dependencies'),
]
