from rest_framework import generics

from ..serializers import ToppingsSerializer
from ..models import Toppings


class ToppingsListCreateView(generics.ListCreateAPIView):
    queryset = Toppings.objects.all()
    serializer_class = ToppingsSerializer
