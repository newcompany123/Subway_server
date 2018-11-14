from rest_framework import serializers, status

from recipes.models import Bookmark
from users.serializers import UserSerializer
from utils.exceptions import CustomAPIException


class BookmarkSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = '__all__'

    def validate_collection(self, collection):

        user = self.context['request'].user

        if not user.bookmarkcollection_set.filter(id=collection.pk):
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='collection does not belong to request user',
                collectio=collection.pk
            )
        return collection

    # 특정 유저가 북마크 하는 모든 recipe를 조회하는 화면이므로 collection을 보여줄
    # 이유가 없음.
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #
    #     data = instance.bookmarkcollection_set.all()
    #     serializer = BookmarkCollectionSerializer(data, many=True)
    #     ret['collection'] = serializer.data
    #     return ret
