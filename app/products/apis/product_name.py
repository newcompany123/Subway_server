from rest_framework import generics, permissions

from utils.permission.custom_permission import IsSuperUserOrReadOnly
from ..serializers.product import ProductNameSerializer
from ..models import ProductName


class ProductNameListCreateView(generics.ListCreateAPIView):
    queryset = ProductName.objects.all()
    serializer_class = ProductNameSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnly,
    )
