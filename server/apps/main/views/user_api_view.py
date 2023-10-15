# flake8:noqa
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from server.apps.main.logic.serializers.user_serializer import (
    AdminUserModifySerializer,
    InstitutionalAdminUserModifySerializer,
    RegularUserModifySerializer,
    UserSerializer,
)
from server.apps.main.models import User


class UserListView(ListAPIView):
    """
    API endpoint for listing users based on user type.

    For admins: List all users
    For institutional admins: List users belonging to their institute
    For regular users: List only their own profile
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_fields = {
        'is_admin': ['exact'],
        'is_institutional_admin': ['exact'],
        'institute': ['exact'],
        'created_at': ['lte', 'gte'],
    }
    ordering_fields = ['created_at', 'id', 'institute']
    search_fields = ['username']

    def get_queryset(self):
        """
        Get the queryset of users based on the user type.

        This method filters the queryset of users based on the requesting user's type:
        - If the user is an admin, it returns all users.
        - If the user is an institutional admin, it returns users belonging to their institute.
        - If the user is a regular user, it returns only their own profile.

        Returns:
            QuerySet: A filtered queryset of users based on the user's type.
        """
        user = self.request.user
        if user.is_admin:
            # If the user is admin, return all users
            return User.objects.all()
        elif user.is_institutional_admin:
            # If the user is institutional admin, return users from their institute
            return User.objects.filter(institute=user.institute)
            # For regular users, return only their own profile
        return User.objects.filter(id=user.id)


class UserModifyView(RetrieveUpdateAPIView):
    """
    API endpoint for modifying user details based on user type.

    Admins can modify all fields.
    Institutional admins can modify name, verify/unverify, and activate/deactivate fields.
    Regular users can change their first name and last name only.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if user.is_admin:
            return AdminUserModifySerializer
        elif user.is_institutional_admin:
            return InstitutionalAdminUserModifySerializer
        else:
            return RegularUserModifySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            # If the user is admin, return all users
            return User.objects.all()
        elif user.is_institutional_admin:
            # If the user is institutional admin, return users from their institute
            return User.objects.filter(institute=user.institute)
        else:
            # For regular users, return only their own profile
            return User.objects.filter(id=user.id)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL),
                'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'is_admin': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'is_institutional_admin': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'institute': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['first_name', 'last_name'],
        ),
        responses={
            200: "User details successfully updated.",
            400: "Bad Request: Invalid input data.",
            403: "Forbidden: You do not have permission to perform this action.",
            404: "Not Found: User not found.",
        },
        operation_description="Partially modify user details based on user type. Admins can modify all fields, institutional admins can modify name, verify/unverify, and activate/deactivate fields, and regular users can change their first name and last name only."
    )
    def patch(self, request, *args, **kwargs):
        """
        Handle HTTP PATCH request.

        This method allows partial updates of user details.
        """
        return self.partial_update(request, *args, **kwargs)
