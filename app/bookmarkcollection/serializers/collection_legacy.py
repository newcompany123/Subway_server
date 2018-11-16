from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from users.serializers import UserSerializer
from ..models import Collection


class BookmarkCollectionSerializer(serializers.ModelSerializer):

    # bookmarked_recipe = BookmarkSerializer(many=True, required=False)
    # Circling Import Issue -> model에서 'blank=True' 설정하고
    #   별도의 Nested Serializer를 위처럼 정의하지 않음으로 자동으로
    #   required=False가 설정되도록 함.

    user = UserSerializer(read_only=True)
    # bookmarked_recipe = BookmarkSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # bookmarked_recipe_list = []
        # for i in ret['bookmarked_recipe']:
        #     # nested 구조로 serializer가 데이터를 받지 않아서 아래 주석처리
        #     # object = Recipe.objects.get(pk=i['recipe'])
        #     object = Recipe.objects.get(pk=i)
        #     bookmarked_recipe_list.append(object)

        # 위 4줄 -> 1줄 축약
        bookmarked_recipe_list = Recipe.objects.filter(pk__in=ret['bookmarked_recipe'])

        # 방법 1) informal way
        # serializer = RecipeSerializer(bookmarked_recipe_list, many=True)
        # serializer._context = self.context

        # 아래코드로는 AttributeError: can't set attribute 발생
        # _context, context 차이?
        # serializer.context = self.context

        # 방법 2) formal way
        # context = self.context
        # serializer = RecipeSerializer(bookmarked_recipe_list, many=True, context=context)

        # 변경 3)
        # iOS 요청으로 일단 auth_user_like_state, auth_user_bookmark_state를
        # null로 표시되도록 임시 변경
        serializer = RecipeSerializer(bookmarked_recipe_list, many=True)

        del ret['bookmarked_recipe']
        ret['bookmarked_recipe'] = serializer.data
        return ret

    # bookmarkcollection.models.BookmarkCollection에서
    # ManyToManyField (bookmarked_recipe)를 삭제하기 전의
    # legacy 코드

    # (특히 Serializer에 context data를 넣는 방법을 찾는 과정이
    #  의미있었기에 남겨둠.)
