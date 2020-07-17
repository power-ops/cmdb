from django.urls import include, path
from asset import serializers

urlpatterns = [
    path('asset/api/', include(serializers.urlpatterns)),
    path('asset/api/v1/', include('asset.apis.v1')),
]
