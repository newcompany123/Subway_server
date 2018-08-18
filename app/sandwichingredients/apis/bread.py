from rest_framework import generics

from sandwichingredients.serializers import BreadSerializer
from ..models import Bread


class BreadListCreateView(generics.ListCreateAPIView):
    queryset = Bread.objects.all()
    serializer_class = BreadSerializer
