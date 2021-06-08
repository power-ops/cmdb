from django.urls import path, include

urlpatterns = [
    path('api/', include('domain.apis')),
    path('', include('domain.serializers'))
]
