from rest_framework import serializers

from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Sandwich
from ..serializers import MainIngredientSerializer, CategorySerializer


class SandwichSerializer(serializers.ModelSerializer):
    main_ingredient = MainIngredientSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Sandwich
        fields = (
            'id',
            'name',
            'image_left',
            'image3x_left',
            'image_right',
            'image3x_right',
            'main_ingredient',
            'category',
            'ordering_num',
        )

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     main_ingredient_list = ret.get('main_ingredient')
    #     for main_ingredient in main_ingredient_list:
    #         ...
    #     ret['main_ingredient'] = ...
    #     return ret


class SandwichRelatedField(serializers.RelatedField):
    queryset = Sandwich.objects.all()

    def to_representation(self, value):
        serializer = SandwichSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        sandwich_name = data.get('name')
        sandwich = get_object_or_404_customed(Sandwich, name=sandwich_name)
        return sandwich

