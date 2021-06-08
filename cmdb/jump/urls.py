from django.urls import path, include

urlpatterns = [
    path('api/', include('jump.apis')),
    path('', include('jump.serializers'))
]
