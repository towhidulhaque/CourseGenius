from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from server.apps.main.logic.serializers.user_serializer import UserSerializer
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
