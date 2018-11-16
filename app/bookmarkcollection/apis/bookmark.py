import re

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsOwnerOrReadOnly
from ..serializers.bookmark import BookmarkSerializer
from recipes.models import Bookmark
from utils.exceptions.get_object_or_404 import get_object_or_404_customed

User = get_user_model()

__all__ = (
    'BookmarkListCreateView',
    'BookmarkRetrieveUpdateDestroyView',
)


class BookmarkListCreateView(generics.ListCreateAPIView):

    serializer_class = BookmarkSerializer

    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        user = get_object_or_404_customed(User, pk=self.kwargs['pk'])
        values = Bookmark.objects.filter(user=user)
        return values

    # Unnecessary since Bookmark POST request is not used
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class BookmarkRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BookmarkSerializer

    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        path = self.request._request.path
        result = re.search(r'.+?(\d+).+?', path)
        pk = result.group(1)
        user = get_object_or_404_customed(User, pk=pk)
        values = Bookmark.objects.filter(user=user)
        return values
