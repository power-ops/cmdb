from django.contrib import admin
from django.conf import settings
from django.http import HttpResponseForbidden
from audits.models import ApiLog

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
                    ApiLog.objects.create(Class=api.__class__.__name__,
                                          Function=func.__name__,
                                          User=request.user,
                                          SourceIP=request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
                                          if request.META.get('HTTP_X_FORWARDED_FOR') else request.META.get(
                                              'REMOTE_ADDR')).save()
                    return func(api, request, *args, **kwargs)
            return HttpResponseForbidden('You DO NOT have this api permission, Please contact your administrator')

        return wrapper

    return decorator
