from django.urls import path, include

urlpatterns = [
    path('api/', include('asset.apis')),
    path('', include('asset.serializers'))
]
