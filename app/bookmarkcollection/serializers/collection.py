from rest_framework import serializers

from ..models import BookmarkCollection


class BookmarkCollectionSerializer(serializers.ModelSerializer):

    # bookmarked_recipe = recipe.BookmarkedRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = BookmarkCollection
        fields = '__all__'
