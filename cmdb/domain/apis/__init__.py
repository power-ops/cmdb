from django.urls import include, path
from domain import serializers

urlpatterns = [
    path('api/domain/', include(serializers.urlpatterns)),
    path('api/domain/v1/', include('domain.apis.v1')),
]