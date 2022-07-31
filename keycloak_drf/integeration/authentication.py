from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from integeration.keycloak import user as user_handler, token as token_handler


User = get_user_model()


class KeycloakAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', b'')
        if not token:
            msg = 'Token string should contain characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            keycloak_token_handler = token_handler.UserTokenKeycloakHandler()
            verification_response = keycloak_token_handler.verify(key)
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {e}')

        if not verification_response:
            raise exceptions.AuthenticationFailed('Invalid token.: Empty')

        username = verification_response.get('preferred_username')

        keycloak_user_handler = user_handler.UserKeycloakHandler(username)
        role = keycloak_user_handler.get_user_role()

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
