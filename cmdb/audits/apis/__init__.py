from django.urls import include, path
from audits import serializers

urlpatterns = [
    path('api/audits/', include(serializers.urlpatterns)),
    # path('v1/', include('audits.apis.v1')),
]
