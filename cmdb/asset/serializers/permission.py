from rest_framework import serializers
from asset.models import Permission
from utils import admin
from rest_framework.response import Response
from utils.mixin import MixinAPIView


class PermissionSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'


class PermissionViewSet(MixinAPIView):
    serializer_class = PermissionSerializer
    model = Permission

    @admin.api_permission('view')
    def get(self, request, uuid=None, format=None):
        return Response(self.get_serialiser_data_by_uuid(uuid))
