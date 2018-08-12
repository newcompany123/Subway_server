from rest_framework import serializers

from bookmarkcollection.serializers.collection import BookmarkCollectionSerializer
from recipes.models import BookmarkedRecipe


class BookmarkedRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookmarkedRecipe
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        data = list(instance.bookmarkcollection_set.all())
        serializer = BookmarkCollectionSerializer(data, many=True)
        ret['collection'] = serializer.data
        return ret
