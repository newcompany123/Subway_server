from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.recipe import BookmarkedRecipeSerializer
from recipes.models import BookmarkedRecipe
from utils.exceptions.get_object_or_404 import get_object_or_404_customed


User = get_user_model()


class BookmarkListCreateAPIView(APIView):

    def post(self, request, pk):
        pass

    def get(self, request, pk):
        user = get_object_or_404_customed(User, pk=pk)
        bookmarkedrecipes = BookmarkedRecipe.objects.all().filter(user=user)
        serailizer = BookmarkedRecipeSerializer(bookmarkedrecipes, many=True)
        return Response(serailizer.data)
