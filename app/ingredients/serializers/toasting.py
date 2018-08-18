from rest_framework import serializers

from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Toasting


class ToastingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toasting
        fields = '__all__'


class ToastingRelatedField(serializers.RelatedField):
    queryset = Toasting.objects.all()

    def to_representation(self, value):
        serializer = ToastingSerializer(value)
        return serializer.data

    def to_internal_value(self, data):
        toasting_name = data.get('name')
        toasting = get_object_or_404_customed(Toasting, name=toasting_name)
        return toasting
