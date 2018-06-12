from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from utils.exceptions.get_object_or_404 import get_object_or_404_customed
from ..models import Product, ProductLike


class ProductLikeListCreateView(APIView):

    def post(self, request, pk):
        user = request.user
        product = get_object_or_404_customed(Product, pk=pk)
        instance, created = ProductLike.objects.get_or_create(
            liker=user,
            product=product,
        )

        if not created:
            instance.delete()
            return Response(
                f'User(id:{user.pk})가 product(id:{product.pk})에 대한 좋아요를 취소하였습니다.',
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                f'User(id:{user.pk})가 product(id:{product.pk})를 좋아합니다.',
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk):
        # product = Product.objects.get(pk=pk)
        product = get_object_or_404_customed(Product, pk=pk)
        product_likers = product.product_liker.all()
        serializer = UserSerializer(product_likers, many=True)
        return Response(serializer.data)
