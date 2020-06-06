from django.urls import include, path
from certificate import serializers

urlpatterns = [
    path('', include(serializers.urlpatterns)),
]
