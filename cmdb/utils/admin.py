from django.contrib import admin
from django.conf import settings
from django.http import HttpResponseForbidden

admin.site.site_header = settings.DJANGO_TITLE


def has_permission(perm: str):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.has_perm(perm):
                return func(request, *args, **kwargs)
            return HttpResponseForbidden

        return wrapper

    return decorator


def api_permission(*perms: str):
    def decorator(func):
        def wrapper(api, request, *args, **kwargs):
            for perm in perms:
                if request.user.has_perm(perm):
                    return func(api, request, *args, **kwargs)
            return HttpResponseForbidden('You DO NOT have this api permission, Please contact your administrator')

        return wrapper

    return decorator
