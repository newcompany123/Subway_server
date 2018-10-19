from django.core.cache import cache
from rest_framework import generics, permissions

from utils.permission.custom_permission import IsRecipeNameMakerOrReadOnly
from ..serializers import RecipeNameSerializer
from ..models import RecipeName


class RecipeNameListCreateView(generics.ListCreateAPIView):
    queryset = RecipeName.objects.all()
    serializer_class = RecipeNameSerializer

    # Data caching by Redis
    # queryset = cache.get_or_set('recipenames', RecipeName.objects.all().values(), 3600)

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # IsSuperUserOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeNameRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeName.objects.all()
    serializer_class = RecipeNameSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsRecipeNameMakerOrReadOnly,
    )
