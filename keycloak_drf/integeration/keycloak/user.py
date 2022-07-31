import logging
from django.conf import settings
import requests
from .token import UserTokenKeycloakHandler, AdminTokenKeycloakHandler

logger = logging.getLogger(__name__)


class UserKeycloakHandler:

    def __init__(self, *args, **kwargs):
        # here i will take url from setting as env var because if we need change our host
        self.create_user_url = settings.KEYCLOAK_CREATE_RETRIEVE_USER_API
        self.user_info_url = settings.KEYCLOAK_USER_INFO_API

        self.username = kwargs.get('username')
        self.enabled = True
        self.emailVerified = True
        self.firstName = kwargs.get('first_name')
        self.lastName = kwargs.get('last_name')
        self.user_password = kwargs.get('user_password')
        self.requiredActions = []
        self.role = kwargs.get('role')
        self.attributes = {'role': self.role}
        self.credentials = [{'type': 'password',
                             'value': self.user_password,
                             'temporary': False}]

        access_token_client = UserTokenKeycloakHandler()
        self.access_token = access_token_client.get_token()

        self.data = {
            'username': self.username,
            'enabled': True,
            'emailVerified': True,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'requiredActions': [],
            'attributes': {'role': self.role},
            'credentials': [{'type': 'password',
                             'value': self.user_password,
                             'temporary': False}]}

    def create_user(self):
        """
            creating user with speciefied data.
        """
        # here are are sure the password will be in kwrga for class
        headers = {
            'Content-Type': 'application/json',
            # access token obtained from token api
            'Authorization': f'Bearer {self.access_token}'
        }
        try:
            # here can cuase many exception like json-decode-error, connection-error like 500
            # all info you may need here https://www.keycloak.org/docs-api/17.0/rest-api/#_users_resource
            response = requests.post(url=self.create_user_url, json=self.data, headers=headers)
        except Exception as e:
            logger.exception(f'<User> error while creatung user in Keycloak: {e}')
            raise Exception(f'Error happend while createing User data: {self.data}')

        if response.status_code == 201:
            return True

        logger.info(f'<User> user creation error response: {response.text}')
        return response.text

    def get_user_role(self):
        """
            here i will add param called `username` to filter user by username.
            * please make sure token is in cache => OR IT WILL NOT WORK.
        """
        # using get_token from admin class because there are alot of cases we will not have used password
        access_token_client = AdminTokenKeycloakHandler()
        self.access_token = access_token_client.get_token()

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
