from django.urls import include, path
from asset import views, serializers

urlpatterns = [
    path('myassets', views.MyAssetsView, name='myassets'),
    path('', include(serializers.urlpatterns)),
    path('v1/', include('asset.apis.v1')),
]
