from rest_framework import serializers
from asset.models import AssetGroup
from cmdb.utils import admin
from rest_framework.response import Response
from django.db.models import Q
from asset.models import Permission
from django.core.cache import cache
from cmdb.mixin import MixinAPIView, MixinSearchView


class AssetGroupSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AssetGroup
        fields = '__all__'


def get_queryset(user):
    queryset = []
    if cache.get('AssetGroupViewSet.get.' + user.username):
        queryset = cache.get('AssetGroupViewSet.get.' + user.username)
    else:
        for res in Permission.objects.filter(Q(UserGroup__in=[g.id for g in user.groups.all()]) | Q(
                User=user.id)):
            queryset += list(res.AssetGroup.all())
        queryset = list(set(queryset))
        cache.set('AssetGroupViewSet.get.' + user.username, queryset)
    return queryset


class AssetGroupViewSet(MixinAPIView):
    serializer_class = AssetGroupSerializer
    model = AssetGroup

    @admin.api_permission('view', 'asset.view_self_asset')
    def get(self, request, pk=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_pk(pk))
        elif request.user.has_perm('asset.view_self_assets'):
            return Response(self.get_serialiser_data_by_pk(pk, get_queryset(request.user)))


class AssetGroupSearchView(MixinSearchView):
    serializer_class = AssetGroupSerializer
    search_fields = ['Name']

    def get_queryset(self):
        if self.request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return AssetGroup.objects.all()
        elif self.request.user.has_perm('asset.view_self_assets'):
            return get_queryset(self.request.user)
