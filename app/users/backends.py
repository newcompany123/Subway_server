import requests
from django.contrib.auth import get_user_model
from rest_framework import status

from users.models import UserOAuthID

User = get_user_model()


class APIFacebookBackend:

    def authenticate(self, request, access_token):
        """
        Facebook access_token을 사용해서
        GraphAPI의 'User'항목을 리턴
        (엔드포인트 'me'를 사용해서 access_token에 해당하는 사용자의 정보를 가져옴)
        :param access_token: 정보를 가져올 Facebook User access token
        :return: User정보 (dict)
        """
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'email',
                'picture.width(512)',
            ])
        }
        response = requests.get('https://graph.facebook.com/v2.12/me', params)
        # 요청에 성공했을 때 (정상 응답)만 진행, 아닐경우 None반환

        if response.status_code == status.HTTP_200_OK:
            response_dict = response.json()

            # print('response.content: ')
            # print(response.content)
            #
            # print('response_dict: ')
            # print(response_dict)

            facebook_id = response_dict['id']
            img_profile_url = response_dict['picture']['data']['url']
            # email은 기본공개정보가 아니기 때문에 유저마다 존재유무가 다름
            email = response_dict.get('email')

            try:
                user = User.objects.get(oauthid__facebook_id=facebook_id)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=facebook_id,
                    email=email,
                )
                obj = UserOAuthID.objects.create(user=user)
                obj.facebook_id = facebook_id
                obj.save()
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None