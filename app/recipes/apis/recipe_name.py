from rest_framework import generics, permissions

from utils.permission.custom_permission import IsSuperUserOrReadOnly
from ..serializers.recipe import RecipeNameSerializer
from ..models import RecipeName


class RecipeNameListCreateView(generics.ListCreateAPIView):
    queryset = RecipeName.objects.all()
    serializer_class = RecipeNameSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnly,
    )
