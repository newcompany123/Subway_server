from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsOwnerOrReadOnly
from ..serializers.product import ProductSerializer
from ..models import Product

User = get_user_model()

__all__ = (
    'ProductListCreateView',
    'UserRetrieveUpdataeDestroyView',
)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserRetrieveUpdataeDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )