from rest_framework import generics, permissions

from utils.permission.custom_permission import IsSuperUserOrReadOnly
from .models import Post
from .serializers import NoticeboardSerializer


class NoticeboardListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = NoticeboardSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnly,
    )
