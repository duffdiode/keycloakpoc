from django.urls import path

from . import views

urlpatterns = [
    path('login/redirect', views.keycloak_redirect, name='keycloak_redirect'),
    path('login', views.keycloak_login, name='login'),
    path('logout', views.keycloak_logout, name='keycloak_logout'),
]
