import logging

from django.conf import settings
from django.core.cache import cache

import requests

from integeration import constants

logger = logging.getLogger(__name__)


class TokenKeycloakHandler:
    """
        i will use it for getting token for User.
        keycloak configuration is to save token for one day so i will cache token for one day.
    """

    def __init__(self, *args, **kwargs):
        self.url = settings.KEYCLOAK_ADMIN_TOKEN_API


class AdminTokenKeycloakHandler(TokenKeycloakHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = kwargs.get('username')

        self.access_token_attribute = {
            'client_id': settings.KEYCLOAK_CLIENT_ID,
            'grant_type': settings.KEYCLOAK_GRANT_TYPE,
            'client_secret': settings.KEYCLOAK_CLIENT_SECRECT
        }

    def get_token(self):
        """
            to getting token
        """
        try:
            response = requests.post(url=self.url, data=self.access_token_attribute)
        except Exception as e:
            logger.exception(f'<Token> error while getting token: {e}')
            raise Exception(f'cant get token for data: {self.access_token_attribute}')

        if response.status_code == 200:
            response_data = response.json()
            cache.set(
                constants.access_token_cache_str.format(self.username),
                response_data,
                constants.one_day_cache_period)
            return response_data

        logger.error(f'<Token> error happened: {response.text}')
        return response.text


class UserTokenKeycloakHandler(TokenKeycloakHandler):
    """
        i will use it for getting token for User.
        keycloak configuration is to save token for one day so i will cache token for one day.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = settings.KEYCLOAK_USER_TOKEN_API
        self.verify_token_url = settings.KEYCLOAK_USER_INFO_API
        self.kwargs = kwargs
        self.username = self.kwargs.get('username')

        self.access_token_attribute = {
            "username": self.username,
            "password": self.kwargs.get('password'),
            "client_id": settings.KEYCLOAK_CLIENT_ID,
            "client_secret": settings.KEYCLOAK_CLIENT_SECRECT,
            "scope": 'openid',
            "grant_type": 'password'
        }

    def verify(self, token):
        """
            to verify token
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.post(url=self.verify_token_url, headers=headers)
        except Exception as e:
            logger.exception(f'<Introspect> error while getting token: {e}')
            raise Exception(f'Token Error: {e}')

        logger.info(f"code: {response.status_code}")
        if response.status_code == 200:
            response_data = response.json()
            return response_data

        logger.error(f'<Introspect> error happened: {response.text}')
        return None

    def get_token(self):
        """
            to getting token
        """
        access_token_or_none = cache.get(constants.access_token_cache_str.format(self.username))
        if access_token_or_none:
            return access_token_or_none

        try:
            response = requests.post(url=self.url, data=self.access_token_attribute)
        except Exception as e:
            logger.exception(f'<Token> error while getting token: {e}')
            raise Exception(f'cant get token for data: ={e}')

        if response.status_code == 200:
            response_data = response.json()
            cache.set(
                constants.access_token_cache_str.format(self.username),
                response_data,
                constants.one_day_cache_period)
            return response_data

        logger.error(f'<Token> error happened: {response.text}')
        return response.text
