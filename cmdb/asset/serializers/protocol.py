from rest_framework import serializers
from asset.models import Protocol
from cmdb.utils import admin
from rest_framework.response import Response
from asset.views import getSelfAssets
from cmdb.mixin import MixinAPIView


class ProtocolSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Protocol
        fields = '__all__'


class ProtocolViewSet(MixinAPIView):
    serializer_class = ProtocolSerializer
    model = Protocol

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_uuid(uuid))
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in getSelfAssets(request):
                queryset += list(res.Protocols.all())
            return Response(self.get_serialiser_data_by_uuid(uuid, list(set(queryset))))
