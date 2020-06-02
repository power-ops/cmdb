from django.urls import path
from .asset import AssetViewSet
from .asset_group import AssetGroupViewSet
from .labels import LabelViewSet
from .systemuser import SystemUserViewSet
from .protocol import ProtocolViewSet
from .permission import PermissionViewSet

urlpatterns = [
    path('asset/', AssetViewSet.as_view()),
    path('asset_group/', AssetGroupViewSet.as_view()),
    path('label/', LabelViewSet.as_view()),
    path('protocol/', ProtocolViewSet.as_view()),
    path('permission/', PermissionViewSet.as_view()),
    path('systemuser/', SystemUserViewSet.as_view()),
]
