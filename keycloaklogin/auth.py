from django.contrib.auth.backends import BaseBackend
from .models import KeycloakUser


class KeycloakAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user) -> KeycloakUser:
        existing_user = KeycloakUser.objects.filter(username=user['username'])
        if len(existing_user) == 0:
            print('User not found, adding to system')
            new_user = KeycloakUser.objects.create_new_keycloak_user(user)
            print(new_user)
            return new_user
        else:
            KeycloakUser.objects.update_keycloak_user(user, existing_user)
        return existing_user

    def get_user(self, user_id):
        try:
            return KeycloakUser.objects.get(pk=user_id)
        except KeycloakUser.DoesNotExist:
            return None

