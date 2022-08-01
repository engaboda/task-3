import logging

from django.conf import settings

import requests

logger = logging.getLogger(__name__)


class UserKeycloakHandler:

    def __init__(self, *args, **kwargs):
        # here i will take url from setting as env var because if we need change our host
        self.create_user_url = settings.KEYCLOAK_CREATE_RETRIEVE_USER_API
        self.user_info_url = settings.KEYCLOAK_USER_INFO_API

        self.access_token = kwargs.get('access_token')

        self.username = kwargs.get('username')
        self.enabled = True
        self.emailVerified = True
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.user_password = kwargs.get('user_password')
        self.role = kwargs.get('role')
        self.attributes = {'role': self.role}
        self.credentials = [{'type': 'password',
                             'value': self.user_password,
                             'temporary': False}]
        self.data = {
            'username': self.username,
            'enabled': True,
            'emailVerified': True,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'attributes': {'role': self.role},
            'credentials': [{'type': 'password',
                             'value': self.user_password,
                             'temporary': False}]}

    def get_user_role(self):
        """
            here i will add param called `username` to filter user by username.
            * please make sure token is in cache => OR IT WILL NOT WORK.
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        try:
            response = requests.get(url=self.create_user_url + f'?username={self.username}', headers=headers)
        except Exception as e:
            logger.exception(f'<Role> error while get role: {e}')
            raise Exception(f'Error happend while getting User Role: {self.username} role')

        if response.status_code == 200:
            response_data = response.json()
            user_info = response_data[0]
            user_attibute = user_info.get('attributes')
            user_role = user_attibute.get('role')[0]
            return user_role

        logger.info(f'<Role> error while getting user role: {response.text}')
        return response.text
