from django.conf import settings
from django.test.signals import setting_changed
from casdoor import CasdoorSDK

DEFAULTS = {
    'CASDOOR_CERT': '',
    'CASDOOR_APP_NAME': '',
    'CASDOOR_ENDPOINT': '',
    'CASDOOR_CLIENT_ID': '',
    'CASDOOR_CLIENT_SECRET': '',
    'CASDOOR_ORG_NAME': '',
    'CASDOOR_FRONT_ENDPOINT': '',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_TYPE_NAME': ('Bearer',),
    'AUTO_CREATE_USER': False,
    'CASDOOR_TO_AUTH_MODEL': {
        'address': 'address',
        'affiliation': 'affiliation',
        'avatar': 'avatar',
        'bio': 'bio',
        'birthday': 'birthday',
        'createdIp': 'created_ip',
        'createdTime': 'created_time',
        'displayName': 'display_name',
        'education': 'education',
        'email': 'email',
        'emailVerified': 'email_verified',
        'firstName': 'first_name',
        'gender': 'gender',
        'homepage': 'homepage',
        'idCard': 'id_card',
        'idCardType': 'id_card_type',
        'isAdmin': 'is_staff',
        'isDeleted': 'is_deleted',
        'isGlobalAdmin': 'is_superuser',
        'isOnline': 'is_online',
        'language': 'language',
        'lastName': 'last_name',
        'lastSigninIp': 'last_signin_ip',
        'lastSigninTime': 'last_signin_time',
        'lastSigninWrongTime': 'last_signin_wrong_time',
        'location': 'location',
        'name': 'username',
        'owner': 'owner',
        'password': 'password',
        'passwordSalt': 'password_salt',
        'permanentAvatar': 'permanent_avatar',
        'phone': 'phone',
        'properties': 'properties',
        'ranking': 'ranking',
        'region': 'region',
        'scope': 'scope',
        'score': 'score',
        'signinWrongTimes': 'signin_wrong_times',
        'signupApplication': 'signup_application',
        'title': 'title',
        'updatedTime': 'updated_time'
    }
}


class APISettings:

    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()
        self._sdk = None

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'REST_CASDOOR', {})
        return self._user_settings

    @property
    def sdk(self):
        if not self._sdk:
            self._sdk = CasdoorSDK(
                endpoint=self.user_settings['CASDOOR_ENDPOINT'],
                client_id=self.user_settings['CASDOOR_CLIENT_ID'],
                client_secret=self.user_settings['CASDOOR_CLIENT_SECRET'],
                org_name=self.user_settings['CASDOOR_ORG_NAME'],
                certificate=self.user_settings['CASDOOR_CERT'],
                application_name=self.user_settings['CASDOOR_APP_NAME'],
                front_endpoint=self.user_settings['CASDOOR_FRONT_ENDPOINT'],
            )
        return self._sdk

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def __check_user_settings(self, user_settings):
        for k, v in user_settings.items():
            if k not in DEFAULTS:
                raise RuntimeError("Invalid REST_CASDOOR setting: '%s'" % k)
            if k.startswith('CASDOOR_') and not v:
                raise RuntimeError("REST_CASDOOR setting: '%s' is empty" % k)
        return user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


api_settings = APISettings(None, DEFAULTS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'REST_CASDOOR':
        api_settings.reload()


setting_changed.connect(reload_api_settings)
