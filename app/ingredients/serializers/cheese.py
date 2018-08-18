from rest_framework import serializers

from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Cheese


class CheeseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheese
        fields = '__all__'


class CheeseRelatedField(serializers.RelatedField):
    queryset = Cheese.objects.all()

    def to_representation(self, value):
        serializer = CheeseSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        cheese_name = data.get('name')
        cheese = get_object_or_404_customed(Cheese, name=cheese_name)
        return cheese
