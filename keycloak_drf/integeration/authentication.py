import logging

from django.contrib.auth import get_user_model

from rest_framework import authentication, exceptions

from integeration.keycloak import token as token_handler
from integeration.keycloak import user as user_handler

logger=logging.getLogger(__name__)

User = get_user_model()


class KeycloakAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', b'')
        if not token:
            msg = 'Token string should contain characters.'
            raise exceptions.AuthenticationFailed(msg)

        token = self.get_raw_token(token)

        return self.authenticate_credentials(token)

    def get_raw_token(self, header):
        """
            Extracts an unvalidated JSON web token from the given "Authorization"
            header value.
        """
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in self.keyword:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise exceptions.AuthenticationFailed(
                "Authorization header must contain two space-delimited values",
                code="bad_authorization_header",
            )

        return parts[1]

    def authenticate_credentials(self, key):
        try:
            keycloak_token_handler = token_handler.UserTokenKeycloakHandler()
            verification_response = keycloak_token_handler.verify(key)
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {e}')

        if not verification_response:
            raise exceptions.AuthenticationFailed('Invalid token.: Empty')

        username = verification_response.get('preferred_username')

        keycloak_token_handler = token_handler.AdminTokenKeycloakHandler(username=username)
        admin_token_response = keycloak_token_handler.get_token()
        admin_token = admin_token_response.get('access_token')

        keycloak_user_handler = user_handler.UserKeycloakHandler(username=username, access_token=admin_token)
        role = keycloak_user_handler.get_user_role()

        if not isinstance(role, str):
            raise exceptions.AuthenticationFailed('Invalid token: Role')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        else:
            user.first_name = verification_response.get('given_name')
            user.last_name = verification_response.get('family_name')
            user.role = role
            user.save()

        return (user, key)
