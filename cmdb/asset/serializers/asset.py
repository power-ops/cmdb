from rest_framework import serializers
from asset.models import Asset, Permission
from management.utils import admin
from rest_framework.response import Response
from management.mixins import MixinAPIView, MixinSearchView


class AssetSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'


class AssetViewSet(MixinAPIView):
    serializer_class = AssetSerializer
    model = Asset

    @admin.api_permission('asset.view_self_asset', 'view')
    def get(self, request, pk=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_pk(pk))
        elif request.user.has_perm('asset.view_self_assets'):
            return Response(self.get_serialiser_data_by_pk(pk, Permission.objects.UserAssets(request.user)))


class AssetSearchView(MixinSearchView):
    serializer_class = AssetSerializer
    search_fields = ['Hostname', 'IP']

    def get_queryset(self):
        if self.request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Asset.objects.all()
        elif self.request.user.has_perm('asset.view_self_assets'):
            return Permission.objects.UserAssets(self.request.user)
