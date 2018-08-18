from rest_framework import serializers

from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Bread


class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'


class BreadRelatedField(serializers.RelatedField):
    queryset = Bread.objects.all()

    def to_representation(self, value):
        serializer = BreadSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        bread_name = data.get('name')
        bread = get_object_or_404_customed(Bread, name=bread_name)
        return bread
