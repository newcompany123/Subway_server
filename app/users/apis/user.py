from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsOneselfOrReadOnly
from ..serializers.user import UserSerializer

User = get_user_model()

__all__ = (
    'UserListCreateView',
    'UserRetrieveUpdateDestroyView',
)


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Data caching by Redis∂
    # queryset = cache.get_or_set('users', User.objects.all(), 3600)

    # 2018.11.14
    # Pass self.request data as context
    # : to represent token data in to_representation

    # 2018.11.15
    # Revoke the change above to allow serializer to get the original context data.
    # (Original context data could be needed in the future)
    def get_serializer_context(self):
        context = super().get_serializer_context()
        # context = self.request
        return context


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Data caching by Redis
    # queryset = cache.get_or_set('users', User.objects.all(), 3600)

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOneselfOrReadOnly,
    )
