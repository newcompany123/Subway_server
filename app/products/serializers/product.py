from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers, status

from users.serializers import UserSerializer
from utils.exceptions.custom_exception import CustomException
from utils.exceptions.get_object_or_404 import get_object_or_404_customed
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


class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'


class VegetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetables
        fields = '__all__'


class ProductNameListingField(serializers.RelatedField):
    queryset = ProductName.objects.all()

    def to_representation(self, value):
        serializer = ProductNameSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        product_name_name = data.get('name')
        product_name = get_object_or_404_customed(ProductName, name=product_name_name)

        # serializer = ProductNameSerializer(data=data)
        # serializer.is_valid()
        # obj = serializer.save
        # return obj

        return product_name


class MainIngredientListingField(serializers.RelatedField):
    queryset = MainIngredient.objects.all()

    def to_representation(self, value):
        serializer = MainIngredientSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        main_ingredient_name = data.get('name')
        main_ingredient = get_object_or_404_customed(MainIngredient, name=main_ingredient_name)
        return main_ingredient


class BreadListingField(serializers.RelatedField):
    queryset = Bread.objects.all()

    def to_representation(self, value):
        serializer = BreadSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        bread_name = data.get('name')
        bread = get_object_or_404_customed(Bread, name=bread_name)
        return bread


class VegetableListingField(serializers.RelatedField):
    queryset = Vegetables.objects.all()

    def to_representation(self, value):
        serializer = VegetableSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        vegetable_name = data.get('name')
        vegetable = get_object_or_404_customed(Vegetables, name=vegetable_name)
        quantity_text = data.get('quantity')
        if not quantity_text in ['LE', 'NO', 'MO'] \
                or quantity_text is None:
            raise CustomException(
                detail='Input correct vegetable quantity option!',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        else:
            vegetable.quantity = quantity_text
            vegetable.save()
        return vegetable


class ProductMakerListingField(serializers.RelatedField):
    queryset = User.objects.all()

    def to_representation(self, value):
        serializer = UserSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        user_name = data.get('username')
        user = get_object_or_404_customed(User, username=user_name)
        # try:
        #     user = User.objects.get(username=user_name)
        # except User.DoesNotExist:
        #     raise CustomException(
        #         detail='User matching query does not exist.',
        #         status_code=status.HTTP_400_BAD_REQUEST
        #     )
        return user


class ProductSerializer(serializers.ModelSerializer):

    # NestedSerializer로 사용하면 해당 Serializer에서 전달된 json 객체를
    #  생성하려 들기 때문에 문제가 됨.
    # product_name = ProductNameSerializer()
    # main_ingredient = MainIngredientSerializer()
    # bread = BreadSerializer()
    # vegetables = VegetableSerializer(many=True)

    product_name = ProductNameListingField()
    main_ingredient = MainIngredientListingField()
    bread = BreadListingField()
    vegetables = VegetableListingField(many=True)
    product_maker = ProductMakerListingField()

    user_like_state = serializers.SerializerMethodField(read_only=True)
    user_save_state = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    save_count = serializers.IntegerField(read_only=True)
    like_save_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'product_name',
            'product_maker',
            'main_ingredient',
            'bread',
            'vegetables',
            'img_profile',
            'img_profile_thumbnail',
            'user_like_state',
            'user_save_state',

            'like_count',
            'save_count',
            'like_save_count',
        )

    def validate(self, attrs):

        # [ Shoveling log ]
        #   : hardcoding eradicated

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

        for product in Product.objects.all():

            # 1) product name's uniqueness validation
            product_name = attrs.get('product_name')
            if product.product_name == product_name:
                raise CustomException(
                    detail='Same sandwich name already exists!',
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # 2) product recipe's uniqueness validation
            main_ingredient_obj = attrs.get('main_ingredient')
            if product.main_ingredient == main_ingredient_obj:

                bread_obj = attrs.get('bread')
                # print(f'{product.bread} {bread_obj}')
                if product.bread == bread_obj:

                    veg_list = attrs.get('vegetables')
                    # print(f'{list(product.vegetables.all())} {veg_list}')
                    if list(product.vegetables.all()) == veg_list:
                        raise CustomException(
                            detail='Same sandwich recipe already exists!',
                            status_code=status.HTTP_400_BAD_REQUEST
                        )

        # attrs을 return하여 validate 과정 종료
        return attrs

    def create(self, validated_data):
        result = super().create(validated_data)
        return result

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #
    #     # Response에서 main_ingredient의 형태를 기존의 pk에서 [{"id": 1, "name": "Italian B.M.T"} 형태로 변환
    #     main_ingredient_pk = ret.get('main_ingredient')
    #     main_ingredient_obj = MainIngredient.objects.get(pk=main_ingredient_pk)
    #     serializer = MainIngredientSerializer(main_ingredient_obj)
    #     ret['main_ingredient'] = serializer.data
    #
    #     # Response에서 bread의 형태를 기존의 pk에서 {"id": 1, "name": "Wheat"} 형태로 변환
    #     bread_pk = ret.get('bread')
    #     bread_obj = Bread.objects.get(pk=bread_pk)
    #     serializer = BreadSerializer(bread_obj)
    #     ret['bread'] = serializer.data
    #
    #     # Response에서 vegetables의 형태를 기존의 pk에서 [{"id": 1: "name": "Lettuce"} 형태로 변환
    #     vege_pk_list = ret.get('vegetables')
    #     vege_list = []
    #     for vege_pk in vege_pk_list:
    #         vege_obj = Vegetables.objects.get(pk=vege_pk)
    #         serializer = VegetableSerializer(vege_obj)
    #         vege_list.append(serializer.data)
    #     ret['vegetables'] = vege_list
    #
    #     # Response에서 name의 형태를 기존의 pk에서 [{"id": 1, "name": "넘맛있는BLT"} 형태로 변환
    #     name_pk = ret.get('name')
    #     name_obj = ProductName.objects.get(pk=name_pk)
    #     serializer = ProductNameSerializer(name_obj)
    #     ret['name'] = serializer.data
    #     return ret

    def get_user_like_state(self, obj):
        user = self._kwargs['context']['request'].user

        if type(user) is AnonymousUser:
            return 'None'
        if obj in user.liked_product.all():
            return 'True'
        else:
            return 'False'

    def get_user_save_state(self, obj):
        user = self._kwargs['context']['request'].user

        if type(user) is AnonymousUser:
            return 'None'
        if obj in user.saved_product.all():
            return 'True'
        else:
            return 'False'
