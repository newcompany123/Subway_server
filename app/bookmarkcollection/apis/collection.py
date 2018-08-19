from django.contrib.auth import get_user_model
from rest_framework import generics

from utils.permission.custom_permission import IsOwnerOrReadOnly
from ..models import BookmarkCollection
from ..serializers.collection import BookmarkCollectionSerializer

from utils.exceptions.get_object_or_404 import get_object_or_404_customed

User = get_user_model()


class BookmarkCollectionListCreateView(generics.ListCreateAPIView):
    # queryset = BookmarkCollection.objects.all()
    serializer_class = BookmarkCollectionSerializer

    permission_classes = (
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        user = get_object_or_404_customed(User, pk=self.kwargs['pk'])
        value = BookmarkCollection.objects.all().filter(user=user)
        return value

    def perform_create(self, serializer):
        user = get_object_or_404_customed(User, pk=self.kwargs['pk'])
        serializer.save(user=user)
