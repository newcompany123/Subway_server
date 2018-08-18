from rest_framework import serializers

from ..models import MainIngredient


class MainIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainIngredient
        fields = '__all__'

