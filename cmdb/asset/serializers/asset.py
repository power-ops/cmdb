from rest_framework import serializers
from asset.models import Asset
from utils import admin
from rest_framework.response import Response
from rest_framework import status
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

    @admin.api_permission('view_self', 'view')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('asset.view_assets'):
            if uuid:
                snippet = Asset.objects.get_by_id(uuid)
                serializer = AssetSerializer(snippet)
            else:
                queryset = Asset.objects.all()
                serializer = AssetSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = getSelfAssets(request)
            if uuid:
                aim = Asset.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = Asset.objects.get_by_id(uuid)
                    serializer = AssetSerializer(snippet)
                else:
                    serializer = AssetSerializer(None, many=True)
            else:
                serializer = AssetSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('add')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = Asset.objects.get_by_id(uuid)
            serializer = AssetSerializer(snippet, data=request.data)
        else:
            serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('delete')
    def delete(self, request, uuid, format=None):
        snippet = Asset.objects.get_by_id(uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
