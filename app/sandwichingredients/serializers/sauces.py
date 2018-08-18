from rest_framework import serializers

from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Sauces


class SaucesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sauces
        fields = '__all__'


class SaucesRelatedField(serializers.RelatedField):
    queryset = Sauces.objects.all()

    def to_representation(self, value):
        serializer = SaucesSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        sauce_name = data.get('name')
        sauce = get_object_or_404_customed(Sauces, name=sauce_name)
        return sauce
