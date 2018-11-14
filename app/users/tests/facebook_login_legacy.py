import ast

import requests
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# from config.settings import FACEBOOK_APP_ID, FACEBOOK_SECRET_CODE, FACEBOOK_HOST
from utils.exceptions import CustomAPIException

print('facebook_login.py --> start')


class FacebookLoginTest(APITestCase):
    URL = reverse('config:users:facebook-login')

    # 1. access_code를 받아와야함
    # 2. 그 access_code안의 data를 이용해서
    # 3. 우리 App에 있는 user와 비교를 하고
    # 4. user가 있으면 그 유저를 login 시키고
    # 5. 아니라면 user를 생성하고 login을 시킨다.

    # test용 DB data 초기화 메소드

    @classmethod
    def setUpTestData(cls):
        cls.app_id = settings.FACEBOOK_APP_ID
        cls.secret_code = settings.FACEBOOK_SECRET_CODE
        # cls.host = settings.FACEBOOK_HOST
        cls.host = 'https://graph.facebook.com/v2.12'
        # cls.app_id = FACEBOOK_APP_ID
        # cls.secret_code = FACEBOOK_SECRET_CODE
        # cls.host = FACEBOOK_HOST

    def get_app_access_token_from_facebook(self):
        url = self.host + "/oauth/access_token"

        params = {'client_id': self.app_id,
                  'client_secret': self.secret_code,
                  'grant_type': 'client_credentials'}
        response = requests.get(url, params=params)
        # Parse response and find token.
        for response_param in response.text.split('&'):
            # print(response_param)
            name, value = response_param.partition(',')[::2]
            token = name + '}'
            # print(token)
            D = ast.literal_eval(token)
            app_access_token = D['access_token']
            return app_access_token
        raise CustomAPIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not determine application access token from response: %r." % response.text,
        )

        # value에는 access_token이 들어있음

    def _get_json(self, response):
        try:
            response_dict = response.json()
        #
        except ValueError:
            raise CustomAPIException("Unexpected response. No JSON object could be decoded.")
        if 'error' in response_dict:
            raise CustomAPIException("Error in response: %r" % response_dict['error'])
        return response_dict

    def get_short_term_access_token_from_facebook(self):
        app_access_token = self.get_app_access_token_from_facebook()

        url = self.host + "/%s/accounts/test-users" % self.app_id
        params = {'access_token': app_access_token}
        response = requests.get(url, params=params)
        access_token_list = []
        for i in self._get_json(response).get('data'):
            # print(i)
            access_token_list.append(i)
            # break
        i = access_token_list[0]
        print(i)
        # print(self._get_json(response).get('data'))
        if i.get('id'):
            access_token = i.get('access_token')
            if not access_token:
                raise CustomAPIException("User %s located, but does not have access_token." % self.id)
            return access_token
        raise CustomAPIException("Unable to find user from response.")

    # def test_get_app_access_token_from_facebook(self):
    #     app_access_token = self.get_app_access_token_from_facebook()
    #     # print(app_access_token)

    def test_get_short_term_access_token_from_facebook(self):
        access_token = self.get_short_term_access_token_from_facebook()
        print(access_token)
