from rest_framework import serializers
from asset.models import Protocol
from utils import admin
from rest_framework.response import Response
from rest_framework import status
from asset.views import getSelfAssets
from utils.mixin import MixinAPIView


class ProtocolSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Protocol
        fields = '__all__'


class ProtocolViewSet(MixinAPIView):
    serializer_class = ProtocolSerializer

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('asset.view_self_assets'):
            if uuid:
                snippet = Protocol.objects.get_by_id(uuid)
                serializer = ProtocolSerializer(snippet)
            else:
                queryset = Protocol.objects.all()
                serializer = ProtocolSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in getSelfAssets(request):
                queryset += list(res.Protocols.all())
            queryset = list(set(queryset))
            if uuid:
                aim = Protocol.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = Protocol.objects.get_by_id(uuid)
                    serializer = ProtocolSerializer(snippet)
                else:
                    serializer = ProtocolSerializer(None, many=True)
            else:
                serializer = ProtocolSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('add')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = Protocol.objects.get_by_id(uuid)
            serializer = ProtocolSerializer(snippet, data=request.data)
        else:
            serializer = ProtocolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('delete')
    def delete(self, request, uuid, format=None):
        snippet = Protocol.objects.get_by_id(uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
