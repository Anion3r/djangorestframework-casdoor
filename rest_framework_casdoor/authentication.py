from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework import exceptions
from .settings import api_settings


class CasdoorAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm = 'api'
    user_model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        return self.get_user(raw_token), raw_token

    @staticmethod
    def get_header(request):
        """
        Extracts the header containing the JSON web token from the given
        request.
        """
        return request.META.get(api_settings.AUTH_HEADER_NAME)

    @staticmethod
    def get_raw_token(header):
        """
        Extracts the raw token from the given header.
        """
        try:
            auth = header.split()
        except UnicodeError:
            raise exceptions.AuthenticationFailed()

        if not auth or auth[0] not in api_settings.AUTH_TYPE_NAME:
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed()
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed()

        try:
            raw_token = api_settings.sdk.parse_jwt_token(auth[1])
        except Exception as e:
            raise exceptions.AuthenticationFailed()
        return raw_token

    def get_user(self, raw_token):
        """
        Returns an active user that matches the payload's user id and email.
        """
        user = self.user_model.objects.get(username=raw_token.get('name', ''))
        if not user.is_active:
            raise exceptions.PermissionDenied()
        return user

    def authenticate_header(self, request):
        return '%s realm="%s"' % (api_settings.AUTH_TYPE_NAME[0], self.www_authenticate_realm)
