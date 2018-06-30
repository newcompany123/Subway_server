from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Recipe, RecipeLike


class RecipeLikeListCreateView(APIView):

    def post(self, request, pk):
        user = request.user
        recipe = get_object_or_404_customed(Recipe, pk=pk)
        instance, created = RecipeLike.objects.get_or_create(
            liker=user,
            recipe=recipe,
        )

        if not created:
            instance.delete()
            return Response(
                f'User(id:{user.pk})가 recipe(id:{recipe.pk})에 대한 좋아요를 취소하였습니다.',
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                f'User(id:{user.pk})가 recipe(id:{recipe.pk})를 좋아합니다.',
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk):
        # recipe = Recipe.objects.get(pk=pk)
        recipe = get_object_or_404_customed(Recipe, pk=pk)
        likers = recipe.liker.all()
        serializer = UserSerializer(likers, many=True)
        return Response(serializer.data)
