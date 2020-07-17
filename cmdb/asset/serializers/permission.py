from rest_framework import serializers
from asset.models import Permission
from cmdb.mixin import MixinAPIView, MixinSearchView


class PermissionSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'


class PermissionViewSet(MixinAPIView):
    serializer_class = PermissionSerializer
    model = Permission


class SystemUserSearchView(MixinSearchView):
    serializer_class = PermissionSerializer
    search_fields = ['Name']

    def get_queryset(self):
        if self.request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Permission.objects.all()
