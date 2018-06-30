from rest_framework import generics, permissions

from utils.permission.custom_permission import IsSuperUserOrReadOnly
from ..serializers.recipe import SandwichSerializer
from ..models import Sandwich


class SandwichListCreateView(generics.ListCreateAPIView):
    queryset = Sandwich.objects.all()
    serializer_class = SandwichSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnly,
    )
