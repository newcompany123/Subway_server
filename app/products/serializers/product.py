from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404

from ..models import Product, Bread, Vegetables

User = get_user_model()

__all__ = (
    'ProductSerializer',
)


class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'


class VegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetables
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    bread = BreadSerializer(read_only=True)
    vegetables = VegetableSerializer(read_only=True, many=True)

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

    def validate(self, attrs):
        # 과정1) self.initial_data에서 입력된 bread의 pk 데이터를 꺼내 attrs에 직접 할당
        if self.initial_data.get('bread'):
            bread_pk = self.initial_data.get('bread')
            bread_obj = get_object_or_404(Bread, pk=bread_pk)
            attrs['bread'] = bread_obj
        else:
            raise APIException("'bread' field is required.")

        # 과정2) self.initial_data에서 입력된 vetables의 pk 데이터를 꺼내 attrs에 직접 할당
        if self.initial_data.get('vegetables'):
            veg_list = []
            veg_pk_list = self.initial_data.getlist('vegetables')

            # 과정3_2) 하단의 uniqueness 검증을 위한 sort 과정 추
            veg_pk_list = sorted(veg_pk_list)
            for veg_pk in veg_pk_list:
                # veg_obj = get_object_or_404(Vegetables, pk=veg_pk)
                try:
                    veg_obj = Vegetables.objects.get(pk=veg_pk)
                except Exception:
                    raise APIException("Input non-existing 'vegetables' object.")

                veg_list.append(veg_obj)
            attrs['vegetables'] = veg_list
            print(veg_list)
        else:
            raise APIException("'vegetables' field is required.")

        # 과정3) product의 uniqueness 확인
        for product in Product.objects.all():
            print(f'{product.bread} {bread_obj}')
            if product.bread == bread_obj:

                print(f'{list(product.vegetables.all())} {veg_list}')
                if list(product.vegetables.all()) == veg_list:
                    raise APIException("Same product already exists")

        # attrs을 return하여 validate 과정 종료
        return attrs

    def create(self, validated_data):
        result = super().create(validated_data)
        return result

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     print(ret)
    #
    #     # Response에서 bread의 형태를 기존의 pk에서 {"1": "Lettuce"} 형태로 변환
    #     bread_obj = get_object_or_404(Bread, pk=ret['bread'])
    #     ret['bread'] = {bread_obj.pk: bread_obj.name}
    #
    #     # Response에서 vegetables의 형태를 기존의 pk에서 [{"1": "Lettuce"} 형태로 변환
    #     vege_pk_list = ret['vegetables']
    #     vege_list = []
    #     for vege_pk in vege_pk_list:
    #         vege_obj = Vegetables.objects.get(pk=vege_pk)
    #         vege_list.append({vege_pk: vege_obj.name})
    #     ret['vegetables'] = vege_list
    #     return ret
