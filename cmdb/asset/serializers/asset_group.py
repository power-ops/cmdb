from rest_framework import serializers
from asset.models import AssetGroup
from utils import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.db.models import Q
from asset.models import Permission


class AssetGroupSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = AssetGroup
        fields = '__all__'


class AssetGroupViewSet(APIView):
    # queryset = Asset.objects.all()
    serializer_class = AssetGroupSerializer

    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    # http_method_names = ['options', 'head', 'get']

    def get_object(self, pk):
        try:
            return AssetGroup.objects.get(pk=pk)
        except AssetGroup.DoesNotExist:
            raise Http404

    @admin.api_permission('assetgroup.view_assetgroup', 'asset.view_self_assets')
    def get(self, request, format=None):
        if request.user.has_perm('assetgroup.view_assetgroup'):
            queryset = AssetGroup.objects.all()
            serializer = AssetGroupSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in Permission.objects.filter(Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(
                User=request.user.id)):
                queryset += list(res.AssetGroup.all())
            queryset = list(set(queryset))
            serializer = AssetGroupSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('assetgroup.add_assetgroup')
    def post(self, request, format=None):
        serializer = AssetGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('assetgroup.change_assetgroup')
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AssetGroupSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('assetgroup.delete_assetgroup')
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)