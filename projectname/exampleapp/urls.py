from django.urls import path, include

urlpatterns = [
    path('api/', include('exampleapp.apis')),
    path('',include('exampleapp.serializers'))
]
