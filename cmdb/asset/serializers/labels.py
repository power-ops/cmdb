from rest_framework import serializers
from asset.models import Label
from utils import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from asset.views import getSelfAssets
from rest_framework.request import Request


class LabelSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Label
        fields = '__all__'


class LabelViewSet(APIView):
    serializer_class = LabelSerializer
    # http_method_names = ['options', 'head', 'get']

    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        self.http_method_names = ['options', 'head', 'get']
        if 'post' not in self.http_method_names and request.user.has_perm('label.add_label'):
            self.http_method_names.append("post")
        if 'put' not in self.http_method_names and request.user.has_perm('label.change_label'):
            self.http_method_names.append("put")
        if 'delete' not in self.http_method_names and request.user.has_perm('label.delete_label'):
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

    @admin.api_permission('label.view_label', 'asset.view_self_assets')
    def get(self, request, format=None):
        if request.user.has_perm('label.view_label'):
            queryset = Label.objects.all()
            serializer = LabelSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in getSelfAssets(request):
                queryset += list(res.Labels.all())
            queryset = list(set(queryset))
            serializer = LabelSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('label.add_label')
    def post(self, request, format=None):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('label.change_label')
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = LabelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('label.delete_label')
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
