import re

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status

from utils.exceptions.custom_exception import CustomException
from utils.permission.custom_permission import IsOwnerOrReadOnly
from ..models import BookmarkCollection
from ..serializers.collection import BookmarkCollectionSerializer

from utils.exceptions.get_object_or_404 import get_object_or_404_customed

User = get_user_model()


class BookmarkCollectionListCreateView(generics.ListCreateAPIView):
    # queryset = BookmarkCollection.objects.all()
    serializer_class = BookmarkCollectionSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        user = get_object_or_404_customed(User, pk=self.kwargs['pk'])
        value = BookmarkCollection.objects.all().filter(user=user)
        return value

    def perform_create(self, serializer):
        # user = get_object_or_404_customed(User, pk=self.kwargs['pk'])
        # serializer.save(user=user)
        user = self.request.user
        serializer.save(user=user)


class BookmarkCollectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = BookmarkCollection.objects.all()
    serializer_class = BookmarkCollectionSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        path = self.request._request.path
        result = re.search(r'.+?(\d+).+?', path)
        pk = result.group(1)
        user = get_object_or_404_customed(User, pk=pk)
        if not user == self.request.user:
            raise CustomException(
                detail="Authenticated user and user from request uri do not match",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        value = BookmarkCollection.objects.all().filter(user=self.request.user)
        return value
