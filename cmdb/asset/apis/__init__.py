from django.urls import include, path
from asset import serializers

urlpatterns = [
    path('v1/', include('asset.apis.v1')),
]
