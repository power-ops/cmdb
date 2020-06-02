from django.urls import path
from .asset import AssetViewSet
from .asset_group import AssetGroupViewSet
from .labels import LabelViewSet

urlpatterns = [
    path('asset/', AssetViewSet.as_view()),
    path('asset_group/', AssetGroupViewSet.as_view()),
    path('label/', LabelViewSet.as_view()),
]
