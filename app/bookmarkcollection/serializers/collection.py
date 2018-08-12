from rest_framework import serializers

from ..models import BookmarkCollection


class BookmarkCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookmarkCollection
        fields = '__all__'
