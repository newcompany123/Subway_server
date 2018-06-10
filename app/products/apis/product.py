from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsProductMakerOrReadOnly
from ..serializers.product import ProductSerializer, ProductNameSerializer
from ..models import Product, ProductName

User = get_user_model()

__all__ = (
    'ProductListCreateView',
    'ProductRetrieveUpdateDestroyView',
)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(product_maker=self.request.user)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsProductMakerOrReadOnly,
    )


class ProductNameListCreateView(generics.ListCreateAPIView):
    queryset = ProductName.objects.all()
    serializer_class = ProductNameSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
