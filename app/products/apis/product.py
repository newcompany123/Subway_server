from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

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
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    filter_backends = (DjangoFilterBackend, OrderingFilter)

    filter_fields = ('main_ingredient',)
    ordering_fields = ('id', 'like_count', 'save_count',)
    ordering = ('-like_save_count', '-save_count', '-like_count',)

    def perform_create(self, serializer):
        serializer.save(product_maker=self.request.user)


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsProductMakerOrReadOnly,
    )
