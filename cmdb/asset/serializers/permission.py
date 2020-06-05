from rest_framework import serializers
from asset.models import Permission
from utils.mixin import MixinAPIView


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'


class PermissionViewSet(MixinAPIView):
    serializer_class = PermissionSerializer
    model = Permission
