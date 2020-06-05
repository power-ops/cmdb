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

    @admin.api_permission('view_self', 'view')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('asset.view_assets'):
            if uuid:
                snippet = self.model.objects.get_by_id(uuid)
                serializer = self.serializer_class(snippet)
            else:
                queryset = self.model.objects.all()
                serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = getSelfAssets(request)
            if uuid:
                aim = self.model.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = self.model.objects.get_by_id(uuid)
                    serializer = self.serializer_class(snippet)
                else:
                    serializer = self.serializer_class(None, many=True)
            else:
                serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
