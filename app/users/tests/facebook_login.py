import json

import os
import requests
from django.conf import settings
from rest_framework import status

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from utils.exceptions import CustomAPIException


class FacebookLoginTest(APITestCase):

    # Facebook OAuth Test Login Process
    # 1) Get Facebook Access-Token
    # 2) Signup or login by sending Access-Token

    # URL_HOST for local / staging test
    SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')
    if SETTINGS_MODULE == 'config.settings.prod':
        from config.settings import prod
        URL_HOST = prod.URL_HOST
    else:
        from config.settings import local
        URL_HOST = local.URL_HOST

    URL_FACEBOOK_LOGIN = URL_HOST + reverse('user:facebook-login')
    URL_ACCESS_TOKEN = 'https://graph.facebook.com/v2.12/oauth/access_token'

    def _get_json(self, response):
        try:
            response_dict = response.json()
        except ValueError:
            raise CustomAPIException("Unexpected response. No JSON object could be decoded.")
        if 'error' in response_dict:
            raise CustomAPIException("Error in response: %r" % response_dict['error'])
        return response_dict

    def get_app_access_token_from_facebook(self):

        # Facebook client_credentials access
        params = {'client_id': settings.FACEBOOK_APP_ID,
                  'client_secret': settings.FACEBOOK_SECRET_CODE,
                  'grant_type': 'client_credentials'}
        response = requests.get(self.URL_ACCESS_TOKEN, params=params)

        # [ast.literal_eval() - turn string to dict]
        # dict1 = ast.literal_eval(response.text)
        # access_token = dict1['access_token']

        response_dict = self._get_json(response)
        access_token = response_dict['access_token']

        return access_token

    def get_short_term_access_token_from_facebook(self, app_access_token):

        # Facebook app access token access
        url = f'https://graph.facebook.com/v2.12/{settings.FACEBOOK_APP_ID}/accounts/test-users'
        params = {'access_token': app_access_token}
        response = requests.get(url, params=params)

        response_dict = self._get_json(response)
        response_data = response_dict.get('data')[0]
        if response_data.get('id'):
            access_token = response_data.get('access_token')
            if not access_token:
                raise CustomAPIException("User %s located, but does not have access_token." % self.id)
            return access_token
        raise CustomAPIException("Unable to find user from response.")

    def test_facebook_login(self):

        # Facebook-login POST request
        app_access_token = self.get_app_access_token_from_facebook()
        access_token = self.get_short_term_access_token_from_facebook(app_access_token)

        # Facebook Login API Test
        post_data = {
            'access_token': access_token
        }
        response = requests.post(self.URL_FACEBOOK_LOGIN, post_data)

        # response_data = json.loads(response.content)
        response_data = self._get_json(response)
        print(response_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['username'], 'Open')
        self.assertEqual(response_data['email'], '')

        # Delete User from the service
        headers = {
            'Authorization': 'Token ' + response_data['token']
        }
        # URL_DELETE_ACCOUNT = self.URL_HOST + '/user/' + str(response_data['id'])
        URL_DELETE_ACCOUNT = self.URL_HOST + reverse('user:user-detail', kwargs={'pk': response_data['id']})
        response = requests.delete(URL_DELETE_ACCOUNT, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # # Check the deletion of user data even in Facebook thoroughly
        # post_data = {
        #     'access_token': access_token
        # }
        # response = requests.post(self.URL_FACEBOOK_LOGIN, post_data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #
        # headers = {
        #     'Authorization': 'Token ' + response_data['token']
        # }
        # URL_DELETE_ACCOUNT = self.URL_HOST + '/user/' + str(response_data['id'])
        # response = requests.delete(URL_DELETE_ACCOUNT, headers=headers)
        # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
