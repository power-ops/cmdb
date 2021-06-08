from django.urls import include, path
from jump import serializers

urlpatterns = [
    path('v1/', include('jump.apis.v1')),
]