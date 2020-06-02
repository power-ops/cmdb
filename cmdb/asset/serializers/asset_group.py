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


class AssetGroupSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = AssetGroup
        fields = '__all__'


class AssetGroupViewSet(APIView):
    serializer_class = AssetGroupSerializer
    http_method_names = ['options', 'head', 'get']

    def get_object(self, pk):
        try:
            return AssetGroup.objects.get(pk=pk)
        except AssetGroup.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        if 'post' not in self.http_method_names and request.user.has_perm('assetgroup.add_assetgroup'):
            self.http_method_names.append("post")
        if 'put' not in self.http_method_names and request.user.has_perm('assetgroup.change_assetgroup'):
            self.http_method_names.append("put")
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
