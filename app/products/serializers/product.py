import json

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ..models import Product, Bread, Vegetables

User = get_user_model()

__all__ = (
    'ProductSerializer',
)


# class BreadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Bread
#         fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    # bread = BreadSerializer()

    # bread = serializers.

    class Meta:
        model = Product
        fields = (
            'id',
            'product_maker',
            'bread',
            'vegetables',
            'img_profile',
            'img_profile_thumbnail',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        print(ret)

        # Response에서 bread의 형태를 기존의 pk에서 {"1": "Lettuce"} 형태로 변환
        bread_obj = get_object_or_404(Bread, pk=ret['bread'])
        ret['bread'] = {bread_obj.pk: bread_obj.name}

        # Response에서 vegetables의 형태를 기존의 pk에서 [{"1": "Lettuce"} 형태로 변환
        vege_pk_list = ret['vegetables']
        vege_list = []
        for vege_pk in vege_pk_list:
            vege_obj = Vegetables.objects.get(pk=vege_pk)
            vege_list.append({vege_pk: vege_obj.name})
        ret['vegetables'] = vege_list
        return ret
