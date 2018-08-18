from rest_framework import generics

from sandwichingredients.serializers import SaucesSerializer
from ..models import Sauces


class SaucesListCreateView(generics.ListCreateAPIView):
    queryset = Sauces.objects.all()
    serializer_class = SaucesSerializer
