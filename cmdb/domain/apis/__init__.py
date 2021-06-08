from django.urls import include, path
from domain import serializers

urlpatterns = [
    path('v1/', include('domain.apis.v1')),
]