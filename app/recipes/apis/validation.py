from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.serializers import RecipeSerializer


class RecipeValidationAPIView(APIView):

    def post(self, request):

        # 1)
        # validate function에 전달되는 attrs와 달리 request 내부의
        # data는 serializing이 되지 않은 raw data이기 때문에
        # 직접 serializing을 해준다.
        # serializer = RecipeSerializer(data=request.data)

        # result = recipe_uniqueness_validator(serializer.validated_data)
        # if type(result) is int:
        #     raise CustomAPIException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=f'Same sandwich recipe (pk:{result}) already exists!',
        #         pk=result,
        #     )
        # return Response({'result': True})

        # 2)
        # API view와 같이 위 처럼 처리하려고 했으나 request.data에 있는
        # raw data들을 변환시키는 과정에서 is_validate를 호출해야하고
        # 이 과정에 있는 vaidate function에서 recipe_uniqueness_validator을
        # 호출함으로써 결과적으로 별도로 위 함수를 호출할 필요가 없어졌다..
        # 그리고 이 is_valid에서 return 되는 값은 True인데 공교롭게도 위에서
        # return Response({'result': True})에서 처럼 True를 반환받는다.

        serializer = RecipeSerializer(data=request.data)
        result = serializer.is_valid(raise_exception=True)
        return Response({'detail': result})
