from rest_framework import serializers
from asset.models import Protocol, Permission
from management.utils import admin
from rest_framework.response import Response
from management.mixins import MixinAPIView, MixinSearchView


class ProtocolSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Protocol
        fields = '__all__'


class ProtocolViewSet(MixinAPIView):
    serializer_class = ProtocolSerializer
    model = Protocol

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, pk=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_pk(pk))
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in Permission.objects.UserAssets(request.user):
                queryset += list(res.Protocols.all())
            return Response(self.get_serialiser_data_by_pk(pk, list(set(queryset))))


class ProtocolSearchView(MixinSearchView):
    serializer_class = ProtocolSerializer
    search_fields = ['Username']

    def get_queryset(self):
        if self.request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Protocol.objects.all()
        elif self.request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in Permission.objects.UserAssets(self.request.user):
                queryset += list(res.Protocols.all())
            return list(set(queryset))
