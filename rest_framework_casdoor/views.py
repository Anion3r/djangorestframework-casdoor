from django.contrib.auth import authenticate
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from .settings import api_settings


def login(request):
    link = api_settings.sdk.get_auth_link(
        redirect_uri=f'{request.build_absolute_uri(reverse("rest_framework_casdoor:callback"))}',
        scope='openid profile email phone username',
    )
    return redirect(link)


def callback(request):
    code = request.GET.get('code', None)
    if not code:
        return Http404()

    response = api_settings.sdk.oauth_token_request(code).json()
    if 'error' in response.keys():
        return JsonResponse({'error': response.get('error_description', None)})
    user = authenticate(request, access_token=response.get('access_token', None))
    if user:
        response.pop('scope')
        response.pop('id_token')
        return JsonResponse(response)
    return JsonResponse("Login failed", safe=False)
