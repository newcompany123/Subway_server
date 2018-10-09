from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from users.serializers import UserSerializer
from ..models import BookmarkCollection


class BookmarkCollectionSerializer(serializers.ModelSerializer):

    # bookmarked_recipe = BookmarkedRecipeSerializer(many=True, required=False)
    # Circling Import Issue -> model에서 'blank=True' 설정하고
    #   별도의 Nested Serializer를 위처럼 정의하지 않음으로 자동으로
    #   required=False가 설정되도록 함.

    user = UserSerializer(read_only=True)
    # bookmarked_recipe = BookmarkedRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = BookmarkCollection
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # bookmarked_recipe_list = []
        # for i in ret['bookmarked_recipe']:
        #     # nested 구조로 serializer가 데이터를 받지 않아서 아래 주석처리
        #     # object = Recipe.objects.get(pk=i['recipe'])
        #     object = Recipe.objects.get(pk=i)
        #     bookmarked_recipe_list.append(object)

        bookmarked_recipe_list = Recipe.objects.filter(pk__in=ret['bookmarked_recipe'])
        serializer = RecipeSerializer(bookmarked_recipe_list, many=True)

        del ret['bookmarked_recipe']
        ret['bookmarked_recipe'] = serializer.data
        return ret
