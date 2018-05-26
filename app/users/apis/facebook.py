from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserSerializer, FacebookAccessTokenSerializer

__all__ = (
    'UserFacebookAccessTokenView',
)


class UserFacebookAccessTokenView(APIView):
    def post(self, request):
        serializer = FacebookAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data
        }
        return Response(data)
