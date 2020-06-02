from rest_framework import serializers
from asset.models import Asset
from utils import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from asset.views import getSelfAssets
from rest_framework.request import Request


class AssetSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'


class AssetViewSet(APIView):
    serializer_class = AssetSerializer
    http_method_names = ['options', 'head', 'get']

    def get_object(self, pk):
        try:
            return Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        if 'post' not in self.http_method_names and request.user.has_perm('asset.add_asset'):
            self.http_method_names.append("post")
        if 'put' not in self.http_method_names and request.user.has_perm('asset.change_asset'):
            self.http_method_names.append("put")
        if 'delete' not in self.http_method_names and request.user.has_perm('asset.delete_asset'):
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

    @admin.api_permission('asset.view_self_assets', 'asset.view_asset')
    def get(self, request, format=None):
        if request.user.has_perm('asset.view_assets'):
            queryset = Asset.objects.all()
            serializer = AssetSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = getSelfAssets(request)
            serializer = AssetSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('asset.add_asset')
    def post(self, request, format=None):
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('asset.change_asset')
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AssetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('asset.delete_asset')
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
