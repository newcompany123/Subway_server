import re

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.exceptions import CustomAPIException
from utils.permission.custom_permission import IsOwnerOrReadOnly
from ..models import Collection
from ..serializers.collection import CollectionSerializer

from utils.exceptions.get_object_or_404 import get_object_or_404_customed

User = get_user_model()

__all__ = (
    'CollectionListCreateView',
    'CollectionRetrieveUpdateDestroyView',
    'CollectionRetrieveDefault',
)


class CollectionListCreateView(generics.ListCreateAPIView):
    # queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        user = get_object_or_404_customed(User, pk=self.kwargs['pk'])
        value = Collection.objects.filter(user=user)
        return value

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CollectionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        path = self.request._request.path
        result = re.search(r'.+?(\d+).+?', path)
        pk = result.group(1)
        user = get_object_or_404_customed(User, pk=pk)
        value = Collection.objects.filter(user=user)
        return value
