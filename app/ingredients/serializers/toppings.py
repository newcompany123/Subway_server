from rest_framework import serializers

from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Toppings


class ToppingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toppings
        fields = '__all__'


class ToppingsRelatedField(serializers.RelatedField):
    queryset = Toppings.objects.all()

    def to_representation(self, value):
        serializer = ToppingsSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        topping_name = data.get('name')
        topping = get_object_or_404_customed(Toppings, name=topping_name)
        return topping
