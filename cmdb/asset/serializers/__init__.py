from django.urls import path
from .asset import AssetViewSet

urlpatterns = [
    path('asset/', AssetViewSet.as_view()),
]
