from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from server.apps.main.logic.serializers.login_serializer import (
    UserLoginSerializer,
)
from server.apps.main.logic.services.login_service import LoginService


class UserLoginAPI(GenericAPIView):
    """Will authenticate app user username password."""

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        """After validating will return jwt token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = LoginService.authenticate_user(serializer.validated_data)
        return Response(response['data'], status=response['status'])
