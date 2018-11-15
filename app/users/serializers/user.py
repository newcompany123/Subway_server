import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

__all__ = (
    'UserSerializer',
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            # 'date_joined',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        # 2018.11.14
        # Code of showing token data Refactored
        # : show token data only when API request is related to user
        allowed_path = [
            '/user/',
            '/user/kakao-login/',
            '/user/facebook-login/',
        ]

        try:
            # normal USER related API
            if type(self.context) == dict and\
                    (self.context['request']._request.path in allowed_path
                     or re.search(r'/user/(\d)/$', self.context['request']._request.path)):
                token, _ = Token.objects.get_or_create(user=instance)
                ret['token'] = token.key

            # Facebook-login / Kaka-login API
            elif self.context._request.path in allowed_path:
                token, _ = Token.objects.get_or_create(user=instance)
                ret['token'] = token.key

        # Bookmark & Collection API raise an AttributeError at 'self.context._request.path'
        except AttributeError:
            # delete email address if request is not related to USER API
            del ret['email']

        return ret
