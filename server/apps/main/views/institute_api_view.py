from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from server.apps.main.logic.serializers.institue_serializer import (
    InstituteSerializer,
)
from server.apps.main.models.institute import Institute


class InstituteListCreateView(ListCreateAPIView):
    """
    API view to list and create institutes.

    Admin can create institutes, and any authenticated user can view the list.
    """

    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer

    def get_permissions(self):
        """
        Return a list of permission classes based on the request method.

        - For the 'List' action (GET request): Any user can access.
        - For the 'Create' action (POST request): Requires admin user.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAdminUser()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Create of the institute."""
        # todo: if creator required then add here
        serializer.save()
