from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404

from ..models import Product, Bread, Vegetables, ProductName, MainIngredient

User = get_user_model()

__all__ = (
    'ProductSerializer',
)


class ProductNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductName
        fields = '__all__'


class MainIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainIngredient
        fields = '__all__'


class VegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetables
        fields = '__all__'


class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    # name = ProductNameSerializer(read_only=True)
    # bread = BreadSerializer(read_only=True)
    # vegetables = VegetableSerializer(read_only=True, many=True)
    product_like_state = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'product_maker',
            'main_ingredient',
            'bread',
            'vegetables',
            'img_profile',
            'img_profile_thumbnail',
            'product_like_state',
        )

    def validate(self, attrs):

        # [ Shoveling log ]

        # 과정1) self.initial_data에서 입력된 bread의 pk 데이터를 꺼내 attrs에 직접 할당
        # if self.initial_data.get('bread'):
        #     bread_pk = self.initial_data.get('bread')
        #     bread_obj = get_object_or_404(Bread, pk=bread_pk)
        #     attrs['bread'] = bread_obj
        # else:
        #     raise APIException("'bread' field is required.")

        # 과정2) self.initial_data에서 입력된 vetables의 pk 데이터를 꺼내 attrs에 직접 할당
        # if self.initial_data.get('vegetables'):
        #     veg_list = []
        #     veg_pk_list = self.initial_data.getlist('vegetables')
        #
        #     # 과정3_2) 하단의 uniqueness 검증을 위한 sort 과정 추
        #     veg_pk_list = sorted(veg_pk_list)
        #     for veg_pk in veg_pk_list:
        #         # veg_obj = get_object_or_404(Vegetables, pk=veg_pk)
        #         try:
        #             veg_obj = Vegetables.objects.get(pk=veg_pk)
        #         except Exception:
        #             raise APIException("Input non-existing 'vegetables' object.")
        #
        #         veg_list.append(veg_obj)
        #     attrs['vegetables'] = veg_list
        #     print(veg_list)
        # else:
        #     raise APIException("'vegetables' field is required.")

        # 과정3) product의 name 설정
        # if self.initial_data.get('name'):
        #     product_name_pk = self.initial_data.get('name')
        #     product_name_obj = get_object_or_404(ProductName, pk=product_name_pk)
        #     attrs['name'] = product_name_obj
        # else:
        #     raise APIException("'name' field(product name) is required.")

        # product's uniqueness validation
        for product in Product.objects.all():
            main_ingredient_obj = attrs.get('main_ingredient')
            if product.main_ingredient == main_ingredient_obj:

                bread_obj = attrs.get('bread')
                # print(f'{product.bread} {bread_obj}')
                if product.bread == bread_obj:

                    veg_list = attrs.get('vegetables')
                    # print(f'{list(product.vegetables.all())} {veg_list}')
                    if list(product.vegetables.all()) == veg_list:
                        raise APIException("Same product already exists")

        # attrs을 return하여 validate 과정 종료
        return attrs

    def create(self, validated_data):
        result = super().create(validated_data)
        return result

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # Response에서 main_ingredient의 형태를 기존의 pk에서 [{"id": 1, "name": "Italian B.M.T"} 형태로 변환
        main_ingredient_pk = ret.get('main_ingredient')
        main_ingredient_obj = MainIngredient.objects.get(pk=main_ingredient_pk)
        serializer = MainIngredientSerializer(main_ingredient_obj)
        ret['main_ingredient'] = serializer.data

        # Response에서 bread의 형태를 기존의 pk에서 {"id": 1, "name": "Wheat"} 형태로 변환
        bread_pk = ret.get('bread')
        bread_obj = get_object_or_404(Bread, pk=bread_pk)
        serializer = BreadSerializer(bread_obj)
        ret['bread'] = serializer.data

        # Response에서 vegetables의 형태를 기존의 pk에서 [{"id": 1: "name": "Lettuce"} 형태로 변환
        vege_pk_list = ret.get('vegetables')
        vege_list = []
        for vege_pk in vege_pk_list:
            vege_obj = Vegetables.objects.get(pk=vege_pk)
            serializer = VegetableSerializer(vege_obj)
            vege_list.append(serializer.data)
        ret['vegetables'] = vege_list

        # Response에서 name의 형태를 기존의 pk에서 [{"id": 1, "name": "넘맛있는BLT"} 형태로 변환
        name_pk = ret.get('name')
        name_obj = ProductName.objects.get(pk=name_pk)
        serializer = ProductNameSerializer(name_obj)
        ret['name'] = serializer.data

        return ret

    def get_product_like_state(self, obj):
        user = self._kwargs['context']['request'].user

        if type(user) is AnonymousUser:
            return 'None'
        if obj in user.liked_product.all():
            return 'True'
        else:
            return 'False'
