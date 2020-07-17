from django.urls import path
from .asset import AssetViewSet, AssetSearchView
from .asset_group import AssetGroupViewSet, AssetGroupSearchView
from .labels import LabelViewSet, LabelSearchView
from .systemuser import SystemUserViewSet, SystemUserSearchView
from .protocol import ProtocolViewSet, ProtocolSearchView
from .permission import PermissionViewSet

urlpatterns = [
    path('asset', AssetSearchView.as_view()),
    path('asset/', AssetViewSet.as_view()),
    path('asset/<uuid:pk>/', AssetViewSet.as_view()),
    path('asset_group', AssetGroupSearchView.as_view()),
    path('asset_group/', AssetGroupViewSet.as_view()),
    path('asset_group/<uuid:pk>/', AssetGroupViewSet.as_view()),
    path('label', LabelSearchView.as_view()),
    path('label/', LabelViewSet.as_view()),
    path('label/<uuid:pk>/', LabelViewSet.as_view()),
    path('protocol', ProtocolSearchView.as_view()),
    path('protocol/', ProtocolViewSet.as_view()),
    path('protocol/<uuid:pk>/', ProtocolViewSet.as_view()),
    path('permission/', PermissionViewSet.as_view()),
    path('permission/<uuid:pk>/', PermissionViewSet.as_view()),
    path('systemuser', SystemUserSearchView.as_view()),
    path('systemuser/', SystemUserViewSet.as_view()),
    path('systemuser/<uuid:pk>/', SystemUserViewSet.as_view()),
]
