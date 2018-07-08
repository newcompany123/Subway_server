from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework import serializers, status

from users.serializers import UserSerializer
from utils.exceptions.custom_exception import CustomException
from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Recipe, Bread, Vegetables, RecipeName, Sandwich, Cheese, Toppings, Sauces, MainIngredient, Category

User = get_user_model()

__all__ = (
    'RecipeSerializer',
)


class RecipeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeName
        fields = '__all__'


class MainIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainIngredient
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
        )


class SandwichSerializer(serializers.ModelSerializer):
    main_ingredient = MainIngredientSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Sandwich
        fields = (
            'id',
            'name',
            'image_left',
            'image3x_left',
            'image_right',
            'image3x_right',
            'main_ingredient',
            'category',
        )

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     main_ingredient_list = ret.get('main_ingredient')
    #     for main_ingredient in main_ingredient_list:
    #         ...
    #     ret['main_ingredient'] = ...
    #     return ret


class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'


class CheeseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'


class ToppingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toppings
        fields = '__all__'


class VegetablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetables
        fields = '__all__'


class SaucesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sauces
        fields = '__all__'


class RecipeNameRelatedField(serializers.RelatedField):
    queryset = RecipeName.objects.all()

    def to_representation(self, value):
        serializer = RecipeNameSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        recipe_name_name = data.get('name')
        recipe_name = get_object_or_404_customed(RecipeName, name=recipe_name_name)

        # serializer = RecipeNameSerializer(data=data)
        # serializer.is_valid()
        # obj = serializer.save
        # return obj

        return recipe_name


class SandwichRelatedField(serializers.RelatedField):
    queryset = Sandwich.objects.all()

    def to_representation(self, value):
        serializer = SandwichSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        sandwich_name = data.get('name')
        sandwich = get_object_or_404_customed(Sandwich, name=sandwich_name)
        return sandwich


class BreadRelatedField(serializers.RelatedField):
    queryset = Bread.objects.all()

    def to_representation(self, value):
        serializer = BreadSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        bread_name = data.get('name')
        bread = get_object_or_404_customed(Bread, name=bread_name)
        return bread


class CheeseRelatedField(serializers.RelatedField):
    queryset = Bread.objects.all()

    def to_representation(self, value):
        serializer = CheeseSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        cheese_name = data.get('name')
        cheese = get_object_or_404_customed(Cheese, name=cheese_name)
        return cheese


class ToppingsRelatedField(serializers.RelatedField):
    queryset = Toppings.objects.all()

    def to_representation(self, value):
        serializer = ToppingsSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        topping_name = data.get('name')
        topping = get_object_or_404_customed(Toppings, name=topping_name)
        return topping


class VegetablesRelatedField(serializers.RelatedField):
    queryset = Vegetables.objects.all()

    def to_representation(self, value):
        serializer = VegetablesSerializer(value)
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


class SaucesRelatedField(serializers.RelatedField):
    queryset = Sauces.objects.all()

    def to_representation(self, value):
        serializer = SaucesSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        sauce_name = data.get('name')
        sauce = get_object_or_404_customed(Sauces, name=sauce_name)
        return sauce


class RecipeSerializer(serializers.ModelSerializer):

    # NestedSerializer로 사용하면 해당 Serializer에서 전달된 json 객체를
    #  생성하려 들기 때문에 문제가 됨.
    # name = RecipeNameSerializer()
    # sandwich = SandwichSerializer()
    # bread = BreadSerializer()
    # vegetables = VegetablesSerializer(many=True)

    name = RecipeNameRelatedField()
    sandwich = SandwichRelatedField()
    bread = BreadRelatedField()

    # 1) serializer default 설정할 경우
    # CHEESE_DEFAULT = Cheese.objects.get(name='no_cheese')
    # cheese = CheeseRelatedField(default=CHEESE_DEFAULT)

    # 2) cheese 무조건 입력
    cheese = CheeseRelatedField()
    toppings = ToppingsRelatedField(many=True, required=False)
    vegetables = VegetablesRelatedField(many=True, required=False)
    sauces = SaucesRelatedField(many=True, required=False)
    inventor = UserSerializer(read_only=True)

    auth_user_like_state = serializers.SerializerMethodField(read_only=True)
    auth_user_bookmark_state = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    bookmark_count = serializers.IntegerField(read_only=True)
    like_bookmark_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'sandwich',
            'bread',
            'cheese',
            'toppings',
            'toasting',
            'vegetables',
            'sauces',
            'inventor',

            'auth_user_like_state',
            'auth_user_bookmark_state',
            'like_count',
            'bookmark_count',
            'like_bookmark_count',
            'created_date',
        )

    def validate(self, attrs):

        # ------------------------------------------------------------
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
        #     product_name_obj = get_object_or_404(RecipeName, pk=product_name_pk)
        #     attrs['name'] = product_name_obj
        # else:
        #     raise APIException("'name' field(recipe name) is required.")
        # ------------------------------------------------------------

        for recipe in Recipe.objects.all():

            # 1) recipe name's uniqueness validation
            name = attrs.get('name')
            if recipe.name == name:
                raise CustomException(
                    detail='Same sandwich name already exists!',
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # 2) recipe's uniqueness validation
            sandwich = attrs.get('sandwich')
            if recipe.sandwich == sandwich:

                bread = attrs.get('bread')
                # print(f'{recipe.bread} {bread_obj}')
                if recipe.bread == bread:

                    cheese = attrs.get('cheese')
                    if recipe.cheese == cheese:

                        toasting = attrs.get('toasting', False)
                        if recipe.toasting == toasting:

                            topping_list = attrs.get('toppings')
                            # print(f'{list(recipe.toppings.all())} {topping_list}')
                            if set(recipe.toppings.all()) == (set(topping_list) if topping_list is not None else set()):

                                vegetable_list = attrs.get('vegetables')
                                # print(f'{list(recipe.vegetables.all())} {vegetable_list}')
                                if set(recipe.vegetables.all()) == (set(vegetable_list) if vegetable_list is not None else set()):

                                    sauce_list = attrs.get('sauces')
                                    if set(recipe.sauces.all()) == (set(sauce_list) if sauce_list is not None else set()):

                                        raise CustomException(
                                            detail='Same sandwich recipe already exists!',
                                            status_code=status.HTTP_400_BAD_REQUEST
                                        )

        # attrs을 return하여 validate 과정 종료
        return attrs

    def create(self, validated_data):
        recipe = super().create(validated_data)
        return recipe

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #
    #     # Response에서 main_ingredient의 형태를 기존의 pk에서 [{"id": 1, "name": "Italian B.M.T"} 형태로 변환
    #     main_ingredient_pk = ret.get('sandwich')
    #     main_ingredient_obj = Sandwich.objects.get(pk=main_ingredient_pk)
    #     serializer = SandwichSerializer(main_ingredient_obj)
    #     ret['sandwich'] = serializer.data
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
    #         serializer = VegetablesSerializer(vege_obj)
    #         vege_list.append(serializer.data)
    #     ret['vegetables'] = vege_list
    #
    #     # Response에서 name의 형태를 기존의 pk에서 [{"id": 1, "name": "넘맛있는BLT"} 형태로 변환
    #     name_pk = ret.get('name')
    #     name_obj = RecipeName.objects.get(pk=name_pk)
    #     serializer = RecipeNameSerializer(name_obj)
    #     ret['name'] = serializer.data
    #     return ret

    def get_auth_user_like_state(self, obj):
        user = self._kwargs['context']['request'].user

        if type(user) is AnonymousUser:
            return 'None'
        if obj in user.liked_recipe.all():
            return 'True'
        else:
            return 'False'

    def get_auth_user_bookmark_state(self, obj):
        user = self._kwargs['context']['request'].user

        if type(user) is AnonymousUser:
            return 'None'
        if obj in user.bookmarked_recipe.all():
            return 'True'
        else:
            return 'False'

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        del ret['inventor']['email']
        del ret['inventor']['token']
        return ret
