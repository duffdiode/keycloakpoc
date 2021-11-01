from django.shortcuts import render


def role_required(allowed_role=""):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if allowed_role in request.user.roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "403.html", context={'role': allowed_role}, status=403)
        return wrap
    return decorator
