from rest_framework import serializers, status

from ..models import Vegetables

from utils.exceptions import CustomAPIException
from utils.exceptions.get_object_or_404 import get_object_or_404_customed


class VegetablesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vegetables
        fields = (
            'id',
            'name',
            'quantity',
            'calories',
            'image',
            'image3x',
        )


class VegetablesRelatedField(serializers.RelatedField):
    queryset = Vegetables.objects.all()

    def to_representation(self, value):
        serializer = VegetablesSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        vegetable_name = data.get('name')
        quantity_text = data.get('quantity')
        if quantity_text not in ['조금', '보통', '많이'] \
                or quantity_text is None:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Input correct vegetable quantity option!',
            )
        vegetable = get_object_or_404_customed(Vegetables, name=vegetable_name, quantity=quantity_text)
        return vegetable
