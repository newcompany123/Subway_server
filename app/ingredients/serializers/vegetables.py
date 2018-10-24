from rest_framework import serializers, status

from utils.exceptions import CustomAPIException
from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Vegetables


class VegetablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vegetables
        fields = '__all__'


class VegetablesRelatedField(serializers.RelatedField):
    queryset = Vegetables.objects.all()

    def to_representation(self, value):
        serializer = VegetablesSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        vegetable_name = data.get('name')
        vegetable = get_object_or_404_customed(Vegetables, name=vegetable_name)
        quantity_text = data.get('quantity')
        if quantity_text not in ['조금', '보통', '많이'] \
                or quantity_text is None:
            raise CustomAPIException(
                detail='Input correct vegetable quantity option!',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        else:
            vegetable.quantity = quantity_text
            vegetable.save()
        return vegetable
