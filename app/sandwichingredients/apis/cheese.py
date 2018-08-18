from rest_framework import generics

from sandwichingredients.serializers import CheeseSerializer
from ..models import Cheese


class CheeseListCreateView(generics.ListCreateAPIView):
    queryset = Cheese.objects.all()
    serializer_class = CheeseSerializer
