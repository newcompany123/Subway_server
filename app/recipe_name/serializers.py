from rest_framework import serializers

from .models import RecipeName
from users.serializers import UserSerializer


class RecipeNameSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = RecipeName
        fields = (
            'id',
            'name',
            'user',
            'created_date',
            'modified_date',
        )
