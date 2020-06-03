from rest_framework import serializers
from asset.models import AssetGroup
from utils import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.db.models import Q
from asset.models import Permission
from rest_framework.request import Request
from django.core.cache import cache


class AssetGroupSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = AssetGroup
        fields = '__all__'


class AssetGroupViewSet(APIView):
    serializer_class = AssetGroupSerializer

    def get_object(self, pk):
        try:
            return AssetGroup.objects.get(pk=pk)
        except AssetGroup.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        if 'post' not in self.http_method_names and request.user.has_perm('assetgroup.add_assetgroup'):
            self.http_method_names.append("post")
        if 'delete' not in self.http_method_names and request.user.has_perm('assetgroup.delete_assetgroup'):
            self.http_method_names.append("delete")

    def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        self.http_methods(request)
        parser_context = self.get_parser_context(request)
        return Request(
            request,
            parsers=self.get_parsers(),
            authenticators=self.get_authenticators(),
            negotiator=self.get_content_negotiator(),
            parser_context=parser_context
        )

    @admin.api_permission('assetgroup.view_assetgroup', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('assetgroup.view_assetgroup'):
            if uuid:
                snippet = self.get_object(uuid)
                serializer = AssetGroupSerializer(snippet)
            else:
                queryset = AssetGroup.objects.all()
                serializer = AssetGroupSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            if cache.get('AssetGroupViewSet_get_' + request.user.username):
                queryset = cache.get('AssetGroupViewSet_get_' + request.user.username)
            else:
                for res in Permission.objects.filter(Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(
                        User=request.user.id)):
                    queryset += list(res.AssetGroup.all())
                queryset = list(set(queryset))
                cache.set('AssetGroupViewSet_get_' + request.user.username, queryset)
            if uuid:
                aim = AssetGroup.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = self.get_object(uuid)
                    serializer = AssetGroupSerializer(snippet)
                else:
                    serializer = AssetGroupSerializer(None, many=True)
            else:
                serializer = AssetGroupSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('assetgroup.add_assetgroup')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = self.get_object(uuid)
            serializer = AssetGroupSerializer(snippet, data=request.data)
        else:
            serializer = AssetGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('assetgroup.delete_assetgroup')
    def delete(self, request, uuid, format=None):
        snippet = self.get_object(uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
