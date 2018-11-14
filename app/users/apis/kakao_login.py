from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserSerializer, KakaoAccessTokenSerializer

__all__ = (
    'UserKakaoAccessTokenView',
)


class UserKakaoAccessTokenView(APIView):
    def post(self, request):
        serializer = KakaoAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer = UserSerializer(user, context=self.request)
        return Response(serializer.data)
