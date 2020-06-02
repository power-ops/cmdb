from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import admin


def has_view_permission(admin: admin.ModelAdmin):
    def decorator(func):
        def wrapper(request):
            if admin.has_view_permission(request):
                return func(request)
            else:
                return HttpResponseForbidden

        return wrapper

    return decorator


def has_add_permission(admin: admin.ModelAdmin):
    def decorator(func):
        def wrapper(request):
            if admin.has_add_permission(request):
                return func(request)
            else:
                return HttpResponseForbidden

        return wrapper

    return decorator


def has_change_permission(admin: admin.ModelAdmin):
    def decorator(func):
        def wrapper(request):
            if admin.has_change_permission(request):
                return func(request)
            else:
                return HttpResponseForbidden

        return wrapper

    return decorator


def has_delete_permission(admin: admin.ModelAdmin):
    def decorator(func):
        def wrapper(request):
            if admin.has_delete_permission(request):
                return func(request)
            else:
                return HttpResponseForbidden

        return wrapper

    return decorator


def has_module_permission(admin: admin.ModelAdmin):
    def decorator(func):
        def wrapper(request):
            if admin.has_module_permission(request):
                return func(request)
            else:
                return HttpResponseForbidden

        return wrapper

    return decorator


def has_view_or_change_permission(admin: admin.ModelAdmin):
    def decorator(func):
        def wrapper(request):
            if admin.has_view_or_change_permission(request):
                return func(request)
            else:
                return HttpResponseForbidden

        return wrapper

    return decorator


def check_admin_permission(admin: admin.ModelAdmin, use_cache=False):
    def decorator(func):
        def wrapper(request):
            if request.user.is_anonymous:
                if use_cache:
                    # print(request.get_full_path())
                    # print(request.META['PATH_INFO'])
                    # Todo: 引入 cache 机制，防 DDoS

                    return func(request)
                else:
                    return JsonResponse({'code': 109, 'errMsg': 'Login required'}, status=403)
            admin.has_view_permission(request)
            return func(request)

        return wrapper

    return decorator
