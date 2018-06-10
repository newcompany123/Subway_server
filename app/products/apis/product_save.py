from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from ..models import Product, ProductSave


class ProductSaveListCreateView(APIView):

    def post(self, request, pk):
        user = request.user
        product = Product.objects.get(pk=pk)
        instance, created = ProductSave.objects.get_or_create(
            saver=user,
            product=product,
        )

        if not created:
            instance.delete()
            return Response(
                f'User({user})가 product({product})의 저장을 취소했습니다.',
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                f'User({user})가 product({product})를 저장했습니다.',
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        product_saver = product.product_liker.all()
        serializer = UserSerializer(product_saver, many=True)
        return Response(serializer.data)
