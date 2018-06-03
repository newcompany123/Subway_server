from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Product, Breads

User = get_user_model()

__all__ = (
    'ProductSerializer',
)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'product_maker',
            'breads',
            'vegetables',
            'img_profile',
            'img_profile_thumbnail',
        )
