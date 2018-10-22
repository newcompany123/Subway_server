from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.serializers import RecipeSerializer
from utils.exceptions import CustomAPIException
from utils.recipe_uniqueness_validator import recipe_uniqueness_validator


class RecipeValidationAPIView(APIView):

    def post(self, request):
        # validate function에 전달되는 attrs와 달리 request 내부의
        # data는 serializing이 되지 않은 raw data이기 때문에
        # 직접 serializing을 해준다.
        serializer = RecipeSerializer(data=request.data)

        result = recipe_uniqueness_validator(serializer.validated_data)
        if type(result) is int:
            raise CustomAPIException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Same sandwich recipe (pk:{result}) already exists!',
                pk=result,
            )
        return Response({'result': True})
