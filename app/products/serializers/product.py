import json

from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..models import Product, Breads, Vegetables

User = get_user_model()

__all__ = (
    'ProductSerializer',
)


# class BreadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Breads
#         fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    # breads = BreadSerializer()

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

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # print(ret)

        # Response에서 breads의 형태를 기존의 pk에서 {"1": "Lettuce"} 형태로 변환
        bread_obj = Breads.objects.get(pk=ret['breads'])
        ret['breads'] = {bread_obj.pk: bread_obj.name}

        # Response에서 vegetables의 형태를 기존의 pk에서 [{"1": "Lettuce"} 형태로 변환
        vege_pk_list = ret['vegetables']
        vege_list = []
        for vege_pk in vege_pk_list:
            vege_obj = Vegetables.objects.get(pk=vege_pk)
            vege_list.append({vege_pk: vege_obj.name})
        ret['vegetables'] = vege_list
        return ret

