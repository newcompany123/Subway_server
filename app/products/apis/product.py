from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from utils.permission.custom_permission import IsProductMakerOrReadOnly, IsSuperUserOrReadOnly

from ..serializers.product import ProductSerializer
from ..models import Product

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
