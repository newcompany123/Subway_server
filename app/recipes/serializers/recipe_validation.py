from django.contrib.auth import get_user_model

from rest_framework import serializers, status

from ingredients.serializers import SandwichRelatedField, BreadRelatedField, CheeseRelatedField, \
    ToastingRelatedField, ToppingsRelatedField, VegetablesRelatedField, SaucesRelatedField
from users.serializers import UserSerializer
from utils.exceptions import CustomAPIException
from utils.recipe_uniqueness_validator import recipe_uniqueness_validator
from ..models import Recipe


User = get_user_model()

__all__ = (
    'RecipeValidationSerializer',
)


# Serializer for RecipeValidation added
#  because exisitng serializer requires name field in its validation process
class RecipeValidationSerializer(serializers.ModelSerializer):

    # name = serializers.CharField()
    sandwich = SandwichRelatedField()
    bread = BreadRelatedField()
    cheese = CheeseRelatedField()
    toasting = ToastingRelatedField()
    toppings = ToppingsRelatedField(many=True, required=False)
    vegetables = VegetablesRelatedField(many=True, required=False)
    sauces = SaucesRelatedField(many=True, required=False)
    calories = serializers.IntegerField(read_only=True)
    inventor = UserSerializer(read_only=True)

    # auth_user_like_state = serializers.SerializerMethodField(read_only=True)
    # auth_user_bookmark_state = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    bookmark_count = serializers.IntegerField(read_only=True)
    like_bookmark_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            # 'name',
            'sandwich',
            'bread',
            'toppings',
            'cheese',
            'toasting',
            'vegetables',
            'sauces',
            'calories',

            'inventor',
            # 'auth_user_like_state',
            # 'auth_user_bookmark_state',
            'like_count',
            'bookmark_count',
            'like_bookmark_count',
            'created_date',
        )

    def validate(self, attrs):

        """
        181029
        [Error found]
        When request data are overlapped,
        (user input two same data)
        those data are just passed to 'recipe_uniqueness_validator
        And every logic of recipe_uniqueness_validator will be broken.

        """

        result = recipe_uniqueness_validator(attrs, path=self.context)
        if type(result) is int:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Same sandwich recipe (pk:{result}) already exists!',
                duplicate_recipe_pk=result,
            )
        return attrs
