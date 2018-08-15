from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsOwnerOrReadOnly
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


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Data caching by Redis
    # queryset = cache.get_or_set('users', User.objects.all(), 3600)

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
