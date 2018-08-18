from rest_framework import generics

from sandwichingredients.serializers import ToastingSerializer
from ..models import Toasting


class ToastingListCreateView(generics.ListCreateAPIView):
    queryset = Toasting.objects.all()
    serializer_class = ToastingSerializer
