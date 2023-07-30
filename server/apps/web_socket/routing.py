from django.urls import re_path

from server.apps.web_socket.consumers import CoreConsumer

websocket_urlpatterns = [
    re_path('^ws/ping-pong/$', CoreConsumer),
]
