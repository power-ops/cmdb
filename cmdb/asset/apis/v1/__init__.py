from .myasset import MyAssets
from django.urls import path

urlpatterns = [
    path('myassets/', MyAssets),
]
