# Django-REST-Framework-Casdoor
`djangorestframework-casdoor` is a Django REST framework authentication plugin for Casdoor.
## Features
- [x] Login with Casdoor
- [x] Verify Casdoor token
- [x] Built-in login view and callback view
- [x] Compatible with `rest_framework`
- [x] Compatible with `django.contrib.auth`
## Install
```shell
pip install Django djangorestframework casdoor djangorestframework-casdoor
```
## Configuration
### Configure `INSTALLED_APPS`
```python
INSTALLED_APPS = [
    ...,
    'rest_framework_casdoor'
]
```
### Configure `AUTHENTICATION_BACKENDS`
```python
AUTHENTICATION_BACKENDS = [
    ...,
    'rest_framework_casdoor.backends.CasdoorBackend'
]
```
### Configure `REST_FRAMEWORK`
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_casdoor.authentication.CasdoorAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ]
}
```
### Configure `rest_framework_casdoor`
```python
REST_CASDOOR = {
    'CASDOOR_CERT': '''''',
    'CASDOOR_APP_NAME': '',
    'CASDOOR_ENDPOINT': '',
    'CASDOOR_CLIENT_ID': '',
    'CASDOOR_CLIENT_SECRET': '',
    'CASDOOR_ORG_NAME': '',
    'CASDOOR_FRONT_ENDPOINT': '',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_TYPE_NAME': ('Bearer', 'JWT'),
    'AUTH_USER_ID_FIELD': 'id',
    'AUTO_CREATE_USER': True,
}
```
> More configuration of `rest_framework_casdoor` please see below
## Usage
### Login
you can use `rest_framework_casdoor` built-in view to login, and get the token.
```python
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('rest_framework_casdoor.urls', namespace='rest_framework_casdoor'))
]
```
Or you can write your own login view to get token and authenticate user.
### Use with `rest_framework`
You can easily write a `rest_framework`'s API views to verify current user's permission.

For `CBV`:
```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_casdoor.authentication import CasdoorAuthentication


class ExampleView(APIView):
    authentication_classes = [CasdoorAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)

```
For `FBV`:
```python
@api_view(['GET'])
@authentication_classes([CasdoorAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # token
    }
    return Response(content)

```
## Configuration of `rest_framework_casdoor`
```python
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
```
### Required configuration
`CASDOOR_CERT`: Casdoor public key，to verify casdoor token.

`CASDOOR_APP_NAME`: Casdoor app name that you use.

`CASDOOR_ENDPOINT`: Casdoor endpoint.

`CASDOOR_CLIENT_ID`: Casdoor client id.

`CASDOOR_CLIENT_SECRET`: Casdoor client secret.

`CASDOOR_ORG_NAME`: Casdoor organization name.

`CASDOOR_FRONT_ENDPOINT`: Casdoor front endpoint, could be same as `CASDOOR_ENDPOINT`
### Optional configuration
`AUTH_HEADER_NAME`: The header name that contains the token.

`AUTH_TYPE_NAME`: The type of the token.

`AUTO_CREATE_USER`: Whether to automatically create a user that does not exist in the database(if set this `True`, you need to configure `CASDOOR_TO_AUTH_MODEL` with your `auth` user model).

`CASDOOR_TO_AUTH_MODEL`: Casdoor field name corresponding to Django User model field name, used to pass parameters when creating users.

## TODO
- [ ] Get user info from Casdoor
- [ ] Update user info in Django
- [ ] Permission control