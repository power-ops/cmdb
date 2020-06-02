from asset import views
from django.urls import include, path
from asset import serializers

urlpatterns = [
    path('myassets', views.MyAssetsView, name='myassets'),
    path('', include(serializers.urlpatterns)),
    path('v1/', include('asset.apis.v1')),
]
