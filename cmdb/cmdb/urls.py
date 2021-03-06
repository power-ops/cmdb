"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin'),
              ] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# + templates(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \

for app, uri in settings.URL_PATTERNS.items():
    urlpatterns += [
        path(uri, include(app)),
    ]

if settings.DEBUG:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="CMDB API",
            default_version='v1',
            description="CMDB",
            # terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="liuzheng712@gmail.com"),
            license=openapi.License(name="GPLv2.0 License"),
        ),
        public=False,
        permission_classes=(permissions.IsAuthenticated,),
    )
    urlpatterns += [url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                        name='schema-json'),
                    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                    ]
    # redoc 页面有bug，缺 position: fixed 等前端bug，暂时没有找到项目PR
