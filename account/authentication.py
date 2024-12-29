from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .models import BlacklistedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.types import OpenApiTypes
from rest_framework import exceptions


class TokenBlacklistAuthentication(BaseAuthentication):
    def authenticate(self, request):

        access_token = request.headers.get("Authorization", None)
        refresh_token = request.headers.get("Refresh", None)

        if access_token:
            parts = access_token.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
                if BlacklistedToken.objects.filter(token=token).exists():
                    raise AuthenticationFailed("This access token has been blacklisted.")
                try:
                    AccessToken(token)
                except Exception:
                    raise AuthenticationFailed("Invalid or expired access token.")
            else:
                raise AuthenticationFailed("Invalid access token format.")

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.check_blacklist()
            except TokenError:
                raise AuthenticationFailed("This refresh token has been blacklisted.")
            except InvalidToken:
                raise AuthenticationFailed("Invalid or expired refresh token.")

        return None



class TokenBlacklistAuthenticationExtension(OpenApiAuthenticationExtension):

    target_class = 'account.authentication.TokenBlacklistAuthentication'
    name = 'BearerAuth'  

    def get_security_definition(self, auto_schema):
        return {
            'BearerAuth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'The Bearer token used to authenticate and authorize requests.'
            },
        }

    