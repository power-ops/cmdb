from rest_framework import serializers
from asset.models import Label
from utils import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from asset.views import getSelfAssets


class LabelSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Label
        fields = '__all__'


class LabelViewSet(APIView):
    # queryset = Asset.objects.all()
    serializer_class = LabelSerializer
    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    http_method_names = ['options', 'head', 'get']

    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        if 'post' not in self.http_method_names and request.user.has_perm('label.add_label'):
            self.http_method_names.append("post")
        if 'put' not in self.http_method_names and request.user.has_perm('label.change_label'):
            self.http_method_names.append("put")
        if 'delete' not in self.http_method_names and request.user.has_perm('label.delete_label'):
            self.http_method_names.append("delete")

    @admin.api_permission('label.view_label', 'asset.view_self_assets')
    def get(self, request, format=None):
        self.http_methods(request)
        if request.user.has_perm('assetgroup.view_assetgroup'):
            queryset = Label.objects.all()
            serializer = LabelSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in getSelfAssets(request):
                queryset.append(res.Labels.all())
                queryset = list(set(queryset))
            serializer = LabelSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('asset.add_asset')
    def post(self, request, format=None):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('asset.change_asset')
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = LabelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('asset.delete_asset')
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
