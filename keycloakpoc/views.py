from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from keycloaklogin.decorators import role_required


def show_home_page(request):
    return render(request, "home.html")


@login_required(login_url="/login")
@role_required(allowed_role="Test")
def show_test_page(request: HttpRequest):
    print(request.session.get_expiry_date())
    return render(request, "test_page.html", context={"title": "Test Page"})


@login_required(login_url="/login")
@role_required(allowed_role="Security")
def show_security_page(request: HttpRequest):
    print(request.session.get_expiry_date())
    return render(request, "test_page.html", context={"title": "Security Page"})

