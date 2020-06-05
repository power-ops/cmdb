from rest_framework import serializers
from asset.models import AssetGroup
from utils import admin
from rest_framework.response import Response
from django.db.models import Q
from asset.models import Permission
from django.core.cache import cache
from utils.mixin import MixinAPIView


class AssetGroupSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = AssetGroup
        fields = '__all__'


class AssetGroupViewSet(MixinAPIView):
    serializer_class = AssetGroupSerializer
    model = AssetGroup

    @admin.api_permission('view', 'asset.view_self_asset')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            if uuid:
                snippet = self.get_object(uuid)
                serializer = self.serializer_class(snippet)
            else:
                queryset = self.model.objects.all()
                serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            if cache.get('AssetGroupViewSet.get.' + request.user.username):
                queryset = cache.get('AssetGroupViewSet.get.' + request.user.username)
            else:
                for res in Permission.objects.filter(Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(
                        User=request.user.id)):
                    queryset += list(res.AssetGroup.all())
                queryset = list(set(queryset))
                cache.set('AssetGroupViewSet.get.' + request.user.username, queryset)
            if uuid:
                aim = self.model.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = self.get_object(uuid)
                    serializer = self.serializer_class(snippet)
                else:
                    serializer = self.serializer_class(None, many=True)
            else:
                serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
