from rest_framework import serializers
from asset.models import Asset
from utils import admin
from rest_framework.response import Response
from asset.views import getSelfAssets
from utils.mixin import MixinAPIView


class AssetSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'


class AssetViewSet(MixinAPIView):
    serializer_class = AssetSerializer
    model = Asset

    @admin.api_permission('asset.view_self_asset', 'view')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_uuid(uuid))
        elif request.user.has_perm('asset.view_self_assets'):
            return Response(self.get_serialiser_data_by_uuid(uuid, getSelfAssets(request)))
