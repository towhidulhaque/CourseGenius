from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from server.apps.main.logic.serializers.password_change_serializer import (
    ChangePasswordSerializer,
)


class ChangePasswordAPIView(UpdateAPIView):
    """API view for changing user password."""

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Returning self user."""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Update user's password."""
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
