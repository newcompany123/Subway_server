from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Recipe, RecipeBookmark


class RecipeBookmarkListCreateView(APIView):

    def post(self, request, pk):
        user = request.user
        recipe = get_object_or_404_customed(Recipe, pk=pk)
        instance, created = RecipeBookmark.objects.get_or_create(
            bookmarker=user,
            recipe=recipe,
        )

        if not created:
            instance.delete()
            return Response(
                f'User(id:{user.pk})가 recipe(id:{recipe.pk})의 저장을 취소했습니다.',
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                f'User(id:{user.pk})가 recipe(id:{recipe.pk})를 저장했습니다.',
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk):
        recipe = get_object_or_404_customed(Recipe, pk=pk)
        bookmarkers = recipe.bookmarker.all()
        serializer = UserSerializer(bookmarkers, many=True)
        return Response(serializer.data)
