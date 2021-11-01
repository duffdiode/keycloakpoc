import copy

from django.http import HttpRequest
from django.shortcuts import redirect
import requests
from django.contrib.auth import authenticate, login, logout

from keycloaklogin.models import KeycloakUser
from keycloakpoc import settings


def keycloak_login(request: HttpRequest):
    params = copy.deepcopy(settings.OAUTH_PARAMS)
    if next:
        params['redirect_uri'] = f"{params['redirect_uri']}?next={request.GET.get('next')}"
    return redirect(build_url(settings.KEYCLOAK_AUTHORISATION_ENDPOINT, params))


def keycloak_redirect(request: HttpRequest):
    code = request.GET.get('code')
    next_url = request.GET.get('next')
    user = get_code(code, next_url=next_url)
    keycloak_user = authenticate(request, user=user)
    if type(keycloak_user) != KeycloakUser:
        keycloak_user = list(keycloak_user).pop()
    print(keycloak_user)
    login(request, keycloak_user)
    return redirect(next_url)


def get_code(code: str, next_url: str):
    redirect_uri = f"{settings.APP_BASE_URL}/login/redirect"
    if next_url:
        redirect_uri = f"{redirect_uri}?next={next_url}"
    data = {"client_id": settings.KEYCLOAK_CLIENT_ID,
            "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "scope": "identify"}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(settings.KEYCLOAK_TOKEN_ENDPOINT, data=data, headers=headers).json()
    access_token = response['access_token']
    response = requests.get(settings.KEYCLOAK_USERINFO_ENDPOINT, headers={'Authorization': 'Bearer {}'.format(access_token)})
    print(response)
    user = response.json()
    print(user)
    return user


def keycloak_logout(request):
    logout(request)
    return redirect(build_url(settings.KEYCLOAK_END_SESSION_ENDPOINT, {"redirect_uri": f"{settings.APP_BASE_URL}/"}))


def build_url(base_url, query_params):
    return "{}?{}".format(base_url, '&'.join(["{}={}".format(key, query_params[key]) for key in query_params]))

