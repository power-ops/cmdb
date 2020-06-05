from rest_framework import serializers
from asset.models import Permission
from utils import admin
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from utils.mixin import MixinAPIView


class PermissionSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'


class PermissionViewSet(MixinAPIView):
    serializer_class = PermissionSerializer

    def get_object(self, pk):
        try:
            return Permission.objects.get(pk=pk)
        except Permission.DoesNotExist:
            raise Http404

    @admin.api_permission('view')
    def get(self, request, uuid=None, format=None):
        if uuid:
            snippet = self.get_object(uuid)
            serializer = PermissionSerializer(snippet)
        else:
            queryset = Permission.objects.all()
            serializer = PermissionSerializer(queryset, many=True)
        return Response(serializer.data)

    @admin.api_permission('add')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = self.get_object(uuid)
            serializer = PermissionSerializer(snippet, data=request.data)
        else:
            serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('delete')
    def delete(self, request, uuid, format=None):
        snippet = self.get_object(uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
