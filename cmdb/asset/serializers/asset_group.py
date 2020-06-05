from rest_framework import serializers
from asset.models import AssetGroup
from utils import admin
from rest_framework.response import Response
from rest_framework import status
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

    @admin.api_permission('view', 'asset.view_self_asset')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('asset.view_self_asset'):
            if uuid:
                snippet = AssetGroup.objects.get_by_id(uuid)
                serializer = AssetGroupSerializer(snippet)
            else:
                queryset = AssetGroup.objects.all()
                serializer = AssetGroupSerializer(queryset, many=True)
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
                aim = AssetGroup.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = AssetGroup.objects.get_by_id(uuid)
                    serializer = AssetGroupSerializer(snippet)
                else:
                    serializer = AssetGroupSerializer(None, many=True)
            else:
                serializer = AssetGroupSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('add')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = AssetGroup.objects.get_by_id(uuid)
            serializer = AssetGroupSerializer(snippet, data=request.data)
        else:
            serializer = AssetGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('delete')
    def delete(self, request, uuid, format=None):
        snippet = AssetGroup.objects.get_by_id(uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
