from django.db import models

from .usermanager import KeycloakUserManager


class KeycloakUser(models.Model):
    objects = KeycloakUserManager()
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    roles = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True)

    def is_authenticated(self):
        return True


