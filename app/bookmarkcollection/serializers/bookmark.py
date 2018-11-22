from rest_framework import serializers, status

from recipes.models import Bookmark
from recipes.serializers import RecipeSerializer
from utils.exceptions import CustomAPIException

__all__ = (
    'BookmarkSerializer',
)


class BookmarkSerializer(serializers.ModelSerializer):

    # 2018.11.16
    # Remove 'user' field from the Bookmark API response.
    # user = UserSerializer(read_only=True)

    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = (
            'id',
            'recipe',
            'collection',
            'created_date',
        )

    def validate_collection(self, collection):

        user = self.context['request'].user

        if not user.collection_set.filter(id=collection.pk):
            raise CustomAPIException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='collection does not belong to request user',
                collection_pk=collection.pk
            )
        return collection

    # 특정 유저가 북마크 하는 모든 recipe를 조회하는 화면이므로 collection을 보여줄
    # 이유가 없음.
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #
    #     data = instance.collection_set.all()
    #     serializer = CollectionSerializer(data, many=True)
    #     ret['collection'] = serializer.data
    #     return ret
