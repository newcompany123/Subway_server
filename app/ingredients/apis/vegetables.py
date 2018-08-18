from rest_framework import generics

from ..serializers import VegetablesSerializer
from ..models import Vegetables


class VegetablesListCreateView(generics.ListCreateAPIView):
    queryset = Vegetables.objects.all()
    serializer_class = VegetablesSerializer
