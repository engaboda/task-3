from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from .serializers import LoginSerializer
from integeration.keycloak.token import UserTokenKeycloakHandler
from .models import User


class KeycloakTokenObtainPairView(TokenObtainPairView):
    """
        Take a set of user credentials and returns an access and refresh JSON web
        token pair to prove the authentication of those credentials.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(username=username).first()

        if not user:
            raise InvalidToken('Token Error')

        token_handler = UserTokenKeycloakHandler(username=username, password=password)
        token_info = token_handler.get_token()

        if isinstance(token_info, str):
            return Response(token_info, status=status.HTTP_400_BAD_REQUEST)
        return Response(token_info, status=status.HTTP_200_OK)
