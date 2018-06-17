from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Product, ProductSave


class ProductSaveListCreateView(APIView):

    def post(self, request, pk):
        user = request.user
        product = get_object_or_404_customed(Product, pk=pk)
        instance, created = ProductSave.objects.get_or_create(
            saver=user,
            product=product,
        )

        if not created:
            instance.delete()
            return Response(
                f'User(id:{user.pk})가 product(id:{product.pk})의 저장을 취소했습니다.',
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                f'User(id:{user.pk})가 product(id:{product.pk})를 저장했습니다.',
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk):
        product = get_object_or_404_customed(Product, pk=pk)
        product_savers = product.product_saver.all()
        serializer = UserSerializer(product_savers, many=True)
        return Response(serializer.data)
