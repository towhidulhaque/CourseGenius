# flake8: noqa WPS201
"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""
from typing import List, Union

from django.conf import settings  # noqa: WPS201
from django.contrib import admin
from django.http import HttpResponse
from django.urls import URLPattern, include, path
from django.views import View
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from health_check import urls as health_urls
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

from server.apps.main import urls as main_urls

admin.autodiscover()

# Schema view for api docs
schema_view = get_schema_view(
    openapi.Info(
        title='Course Genius API',
        default_version='v1',
        description='Endpoints of the API Backend',
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=(SessionAuthentication, BasicAuthentication)
)


class HealthCheck(View):
    """View for base url."""

    def get(self, request):
        """To return a 200 response."""
        return HttpResponse('All Good Here.')


urlpatterns = [
    # Apps:
    path('api/v1/main/', include(main_urls, namespace='main')),
    # Health checks:
    path('', HealthCheck.as_view()),
    path('health/', include(health_urls)),  # noqa: DJ05

    # Text and xml static files:
    path('robots.txt', TemplateView.as_view(
        template_name='txt/robots.txt',
        content_type='text/plain',
    )),
    path('humans.txt', TemplateView.as_view(
        template_name='txt/humans.txt',
        content_type='text/plain',
    )),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# Serving media files in development only:
if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433
    from django.conf.urls.static import static  # noqa: WPS433

    urlpatterns: List[Union[URLPattern, URLPattern]] = [  # type: ignore
                                                           path('__debug__/', include(debug_toolbar.urls)),
                                                       ] + urlpatterns + static(settings.MEDIA_URL,
                                                                                document_root=settings.MEDIA_ROOT)
