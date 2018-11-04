from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework import serializers, status

from ingredients.serializers import SandwichRelatedField, BreadRelatedField, CheeseRelatedField, \
    ToastingRelatedField, ToppingsRelatedField, VegetablesRelatedField, SaucesRelatedField
from users.serializers import UserSerializer
from utils.calories_counter import calories_counter
from utils.exceptions import CustomAPIException
from utils.recipe_uniqueness_validator import recipe_uniqueness_validator
from ..models import Recipe


User = get_user_model()

__all__ = (
    'RecipeSerializer',
)


# class RecipeNameRelatedField(serializers.RelatedField):
#     queryset = RecipeName.objects.all()
#
#     def to_representation(self, value):
#         serializer = RecipeNameSerializer(value)
#         return serializer.data
#
#     def to_internal_value(self, data):
#         recipe_name_name = data.get('name')
#         recipe_name = get_object_or_404_customed(RecipeName, name=recipe_name_name)
#
#         # serializer = RecipeNameSerializer(data=data)
#         # serializer.is_valid()
#         # obj = serializer.save
#         # return obj
#
#         return recipe_name


class RecipeSerializer(serializers.ModelSerializer):

    # NestedSerializer로 사용하면 해당 Serializer에서 전달된 json 객체를
    #  생성하려 들기 때문에 문제가 됨.
    # name = RecipeNameSerializer()
    # sandwich = SandwichSerializer()
    # bread = BreadSerializer()
    # vegetables = VegetablesSerializer(many=True)

    # 181028 'name' field modified : OneToOneField -> CharField
    # name = RecipeNameRelatedField()
    name = serializers.CharField()
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
    # calories = serializers.SerializerMethodField(read_only=True)
    calories = serializers.IntegerField(read_only=True)
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
            'calories',

            'inventor',
            'auth_user_like_state',
            'auth_user_bookmark_state',
            'like_count',
            'bookmark_count',
            'like_bookmark_count',
            'created_date',
        )

    def validate(self, attrs):

        result = recipe_uniqueness_validator(attrs)
        if type(result) is int:

            # 1) APIException
            # raise APIException(f'Same sandwich recipe (pk:{pk}) already exists!')

            # 2) CustomAPIException
            # raise CustomAPIException(
            #     status_code=status.HTTP_400_BAD_REQUEST,
            #     detail=f'Same sandwich recipe (pk:{pk}) already exists!',
            # )

            # 3) CustomAPIException + custom_exception_handler
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Same sandwich recipe (pk:{result}) already exists!',
                pk=result,
            )

        # attrs을 return하여 validate 과정 종료
        return attrs

    def create(self, validated_data):
        recipe = super().create(validated_data)

        # Counting calories of recipe
        recipe.calories = calories_counter(recipe)
        recipe.save()

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
                return None

            # if obj in user.liked_recipe.all():

            # Code Refactoring : queryset -> filtering
            if User.objects.filter(like__recipe__in=[obj]):
                return 'True'
            else:
                return 'False'
        else:
            pass

    def get_auth_user_bookmark_state(self, obj):
        if self.context:
            user = self.context['request'].user
            if type(user) is AnonymousUser:
                return None
            # if obj in user.bookmarked_recipe.all():
            if User.objects.filter(bookmark__recipe__in=[obj]):
                return 'True'
            else:
                return 'False'
        else:
            pass

    # def get_calories(self, obj):
    #
    #     # 1) validated_data 이용
    #     # calories = 0
    #     # calories += self.validated_data.get('sandwich').calories
    #     # calories += self.validated_data.get('bread').calories
    #     # calories += self.validated_data.get('cheese').calories
    #     # for i in self.validated_data.get('toppings'):
    #     #     if i.calories:
    #     #         calories += i.calories
    #     # for i in self.validated_data.get('vegetables'):
    #     #     if i.calories:
    #     #         calories += i.calories
    #     # for i in self.validated_data.get('sauces'):
    #     #     if i.calories:
    #     #         calories += i.calories
    #
    #     # self.validated_data는 serializing을 거친 값일 뿐
    #     # 정말 valid한 값이 아니기 때문에 calories를 계산하는 중요한
    #     # logic에서 이용할 경우 심각한 오류를 초래할 수 있음.
    #     #
    #     # eg. toppings에 동일한 값이 2번 이상 입력될 경우
    #     #     validated_data에 그대로 중복되어 있는 값을 2번 계산하게 된다.
    #     #
    #     #     >> print(obj.toppings.all())
    #     #     <QuerySet [<Toppings: 2_베이컨>, <Toppings: 5_에그마요>]>
    #     #
    #     #     >> print(self.validated_data.get('toppings'))
    #     #     [<Toppings: 2_베이컨>, <Toppings: 5_에그마요>, <Toppings: 5_에그마요>]
    #
    #     # 2) obj 이용
    #     calories = 0
    #     calories += obj.sandwich.calories - 200
    #     calories += obj.bread.calories
    #     calories += obj.cheese.calories
    #     for i in obj.toppings.all():
    #         if i.calories:
    #             calories += i.calories
    #     for i in obj.sauces.all():
    #         if i.calories:
    #             calories += i.calories
    #     for i in obj.vegetables.all():
    #         if i.calories:
    #             calories += i.calories
    #
    #     # double cheese process
    #     if obj.toppings.filter(name='더블 치즈'):
    #         calories += obj.cheese.calories
    #
    #     # double up process
    #     if obj.toppings.filter(name='더블업'):
    #         for i in obj.sandwich.main_ingredient.all():
    #             if i.calories:
    #                 calories += i.calories
    #
    #     # 3) 매번 GET 요청 때마다 위의 logic을 계산하는 것이 말이 안되서(너무 느려서)
    #     # create 오버라이딩 메서드에서 recipe object 생성 후 calories 값 계산
    #
    #     return calories

    def to_representation(self, obj):
        ret = super().to_representation(obj)

        # To protect private user information
        del ret['inventor']['email']
        del ret['inventor']['token']

        return ret
