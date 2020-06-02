from asset import views
from django.urls import include, path

urlpatterns = [
    path('myassets', views.MyAssetsView, name='myassets'),
    path('v1/', include('asset.apis.v1'))
]
