from rest_framework import serializers

from users.serializers import UserSerializer
from ..models import BookmarkCollection


class BookmarkCollectionSerializer(serializers.ModelSerializer):

    # bookmarked_recipe = BookmarkedRecipeSerializer(many=True, required=False)
    # Circling Import Issue -> model에서 'blank=True' 설정하고
    #   별도의 Nested Serializer를 위처럼 정의하지 않음으로 자동으로
    #   required=False가 설정되도록 함.

    user = UserSerializer(read_only=True)

    class Meta:
        model = BookmarkCollection
        fields = '__all__'
