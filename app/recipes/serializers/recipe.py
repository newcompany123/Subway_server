from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
from django.forms import model_to_dict

from rest_framework import serializers, status

from ingredients.models import Toppings, Vegetables, Sauces
from ingredients.serializers import SandwichRelatedField, BreadRelatedField, CheeseRelatedField, \
    ToastingRelatedField, ToppingsRelatedField, VegetablesRelatedField, SaucesRelatedField
from recipe_name.models import RecipeName
from recipe_name.serializers import RecipeNameSerializer
from users.serializers import UserSerializer
from utils.exceptions.custom_exception import CustomException
from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Recipe


User = get_user_model()

__all__ = (
    'RecipeSerializer',
)


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

    # 2) cheese,toasting 무조건 입력
    cheese = CheeseRelatedField()
    toasting = ToastingRelatedField()
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
            'toppings',
            'cheese',
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

        # 1) recipe name's uniqueness validation

        # O(log n)
        if Recipe.objects.filter(name=attrs.get('name')):
            raise CustomException(
                detail='Same sandwich name already exists!',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # [shoveling log]
        # O(n)
        # for recipe in Recipe.objects.all():
        #
        #     # 1) recipe name's uniqueness validation
        #     name = attrs.get('name')
        #     if recipe.name == name:
        #         raise CustomException(
        #             detail='Same sandwich name already exists!',
        #             status_code=status.HTTP_400_BAD_REQUEST
        #         )

        # 2) recipe ingredients' uniqueness validation

        # O(log n) - Time: 100~150ms
        recipe_filtered_list = Recipe.objects\
            .filter(sandwich=attrs.get('sandwich'))\
            .filter(bread=attrs.get('bread'))\
            .filter(cheese=attrs.get('cheese'))\
            .filter(toasting=attrs.get('toasting'))

        # toppings
        topping_pk_list = []
        for topping in attrs.get('toppings', []):
            topping_pk_list.append(topping.pk)

        if recipe_filtered_list:
            if attrs.get('toppings'):
                recipe_filtered_list = recipe_filtered_list\
                    .filter(toppings__in=attrs.get('toppings')).distinct()\
                    .annotate(num_toppings=Count('toppings', distinct=True))\
                    .filter(num_toppings=len(attrs.get('toppings')))\
                    .exclude(toppings__in=Toppings.objects.exclude(pk__in=topping_pk_list))
            else:
                recipe_filtered_list\
                    .filter(toppings__isnull=True)

        # vegetables
        vegetable_pk_list = []
        for vegetable in attrs.get('vegetables', []):
            vegetable_pk_list.append(vegetable.pk)

        if recipe_filtered_list:
            if attrs.get('vegetables'):
                recipe_filtered_list = recipe_filtered_list\
                    .filter(vegetables__in=attrs.get('vegetables')).distinct()\
                    .annotate(num_vegetables=Count('vegetables', distinct=True))\
                    .filter(num_vegetables=len(attrs.get('vegetables')))\
                    .exclude(vegetables__in=Vegetables.objects.exclude(pk__in=vegetable_pk_list))
            else:
                recipe_filtered_list\
                    .filter(vegetables__isnull=True)

        # sauces
        sauce_pk_list = []
        for sauce in attrs.get('sauces', []):
            sauce_pk_list.append(sauce.pk)

        if recipe_filtered_list:
            if attrs.get('sauces'):
                recipe_filtered_list = recipe_filtered_list\
                    .filter(sauces__in=attrs.get('sauces')).distinct()\
                    .annotate(num_sauces=Count('sauces', distinct=True))\
                    .filter(num_sauces=len(attrs.get('sauces')))\
                    .exclude(sauces__in=Sauces.objects.exclude(pk__in=sauce_pk_list))
            else:
                recipe_filtered_list\
                    .filter(sauces__isnull=True)

        print(recipe_filtered_list)
        for recipe in recipe_filtered_list:
            print(model_to_dict(recipe))

        if recipe_filtered_list:
            # pk = recipe_filtered_list.values('pk')[0]['pk']
            pk = recipe_filtered_list.values_list('pk', flat=True)[0]
            raise CustomException(
                detail=f'Same sandwich recipe (pk:{pk}) already exists!',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        # [shoveling log]
        # O(n) - Time: 150~200ms
        # for recipe in Recipe.objects.all():
        #
        #     sandwich = attrs.get('sandwich')
        #     if recipe.sandwich == sandwich:
        #
        #         bread = attrs.get('bread')
        #         # print(f'{recipe.bread} {bread_obj}')
        #         if recipe.bread == bread:
        #
        #             cheese = attrs.get('cheese')
        #             if recipe.cheese == cheese:
        #
        #                 toasting = attrs.get('toasting', False)
        #                 if recipe.toasting == toasting:
        #
        #                     topping_list = attrs.get('toppings')
        #                     # print(f'{list(recipe.toppings.all())} {topping_list}')
        #                     if set(recipe.toppings.all()) == (set(topping_list) if topping_list is not None else set()):
        #
        #                         vegetable_list = attrs.get('vegetables')
        #                         # print(f'{list(recipe.vegetables.all())} {vegetable_list}')
        #                         if set(recipe.vegetables.all()) == (set(vegetable_list) if vegetable_list is not None else set()):
        #
        #                             sauce_list = attrs.get('sauces')
        #                             if set(recipe.sauces.all()) == (set(sauce_list) if sauce_list is not None else set()):
        #
        #                                 raise CustomException(
        #                                     detail='Same sandwich recipe already exists!',
        #                                     status_code=status.HTTP_400_BAD_REQUEST
        #                                 )

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
        if self.context:
            user = self.context['request'].user
            if type(user) is AnonymousUser:
                return 'None'
            if obj in user.liked_recipe.all():
                return 'True'
            else:
                return 'False'
        else:
            pass

    def get_auth_user_bookmark_state(self, obj):
        if self.context:
            user = self.context['request'].user
            if type(user) is AnonymousUser:
                return 'None'
            if obj in user.bookmarked_recipe.all():
                return 'True'
            else:
                return 'False'
        else:
            pass

    def to_representation(self, obj):
        ret = super().to_representation(obj)
        del ret['inventor']['email']
        del ret['inventor']['token']
        return ret
