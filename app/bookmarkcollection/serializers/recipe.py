from rest_framework import serializers

from ..serializers import BookmarkCollectionSerializer
from recipes.models import BookmarkedRecipe


class BookmarkedRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookmarkedRecipe
        fields = '__all__'

    # 특정 유저가 북마크 하는 모든 recipe를 조회하는 화면이므로 collection을 보여줄
    # 이유가 없음.
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #
    #     data = instance.bookmarkcollection_set.all()
    #     serializer = BookmarkCollectionSerializer(data, many=True)
    #     ret['collection'] = serializer.data
    #     return ret
