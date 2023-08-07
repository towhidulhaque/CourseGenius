from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from server.apps.main.logic.serializers.user_serializer import (
    RegisterSerializer,
)
from server.apps.main.logic.services.register_service import RegisterService
from server.apps.main.models import User


class RegisterAPIView(CreateAPIView):
    """Register API."""

    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request):
        """Add User."""
        serializer = self.serializer_class(data=request.data, many=False)
        if serializer.is_valid(raise_exception=True):
            user = RegisterService.register_user(serializer.validated_data)
            response_data = {
                'user': str(user.username),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
