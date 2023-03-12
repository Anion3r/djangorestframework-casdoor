from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from .settings import api_settings


class CasdoorBackend(BaseBackend):
    def authenticate(self, request, access_token=None, **kwargs):
        if access_token is None:
            access_token = kwargs.pop('access_token', None)
        if access_token is None:
            return None

        try:
            token = api_settings.sdk.parse_jwt_token(access_token)
        except Exception as e:
            return None
        user_model = get_user_model()
        try:
            query = {
                user_model.USERNAME_FIELD: token.get('name', '')
            }
            user = user_model.objects.get(**query)
        except user_model.DoesNotExist:
            if not api_settings.AUTO_CREATE_USER:
                return None
            query = {}
            fields = [field.name for field in user_model._meta.get_fields()]
            for k, v in token.items():
                if k in api_settings.CASDOOR_TO_AUTH_MODEL.keys() and api_settings.CASDOOR_TO_AUTH_MODEL[k] in fields:
                    query[api_settings.CASDOOR_TO_AUTH_MODEL[k]] = v
            user = user_model.objects.create_user(**query)
        return user

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
