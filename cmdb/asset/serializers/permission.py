from rest_framework import serializers
from asset.models import Permission
from utils import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.request import Request


class PermissionSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'


class PermissionViewSet(APIView):
    serializer_class = PermissionSerializer
    http_method_names = ['options', 'head', 'get']

    def get_object(self, pk):
        try:
            return Permission.objects.get(pk=pk)
        except Permission.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        self.http_method_names = ['options', 'head', 'get']
        if 'post' not in self.http_method_names and request.user.has_perm('permission.add_permission'):
            self.http_method_names.append("post")
        if 'put' not in self.http_method_names and request.user.has_perm('permission.change_permission'):
            self.http_method_names.append("put")
        if 'delete' not in self.http_method_names and request.user.has_perm('permission.delete_permission'):
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

    @admin.api_permission('premission.view_premission')
    def get(self, request, format=None):
        queryset = Permission.objects.all()
        serializer = PermissionSerializer(queryset, many=True)
        return Response(serializer.data)

    @admin.api_permission('premission.add_premission')
    def post(self, request, format=None):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('premission.change_premission')
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PermissionSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('premission.delete_premission')
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
