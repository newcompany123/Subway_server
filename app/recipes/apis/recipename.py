from django.core.cache import cache
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsSuperUserOrReadOnly
from ..serializers.recipe import RecipeNameSerializer
from ..models import RecipeName


class RecipeNameListCreateView(generics.ListCreateAPIView):
    queryset = RecipeName.objects.all()
    serializer_class = RecipeNameSerializer

    # Data caching by Redis
    # queryset = cache.get_or_set('recipenames', RecipeName.objects.all().values(), 3600)

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsSuperUserOrReadOnly,
    )
