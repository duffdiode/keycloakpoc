from django.contrib.auth import models

from keycloakpoc import settings


class KeycloakUserManager(models.UserManager):
    def create_new_keycloak_user(self, user):
        if "resource_access" in user:
            roles = user['resource_access'][settings.KEYCLOAK_CLIENT_ID]['roles']
        else:
            roles = []
        new_user = self.create(username=user['username'],
                               roles=roles)
        return new_user

    @staticmethod
    def update_keycloak_user(user, user_object):
        if "resource_access" in user:
            roles = user['resource_access'][settings.KEYCLOAK_CLIENT_ID]['roles']
        else:
            roles = []
        user_object.update(roles=roles)
        