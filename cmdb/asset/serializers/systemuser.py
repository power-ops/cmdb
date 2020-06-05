from rest_framework import serializers
from asset.models import SystemUser
from utils import admin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from asset.models import Permission
from django.core.cache import cache
from utils.mixin import MixinAPIView


class SystemUserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = SystemUser
        fields = '__all__'


class SystemUserViewSet(MixinAPIView):
    serializer_class = SystemUserSerializer

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('asset.view_self_assets'):
            if uuid:
                snippet = SystemUser.objects.get_by_id(uuid)
                serializer = SystemUserSerializer(snippet)
            else:
                queryset = SystemUser.objects.all()
                serializer = SystemUserSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            if cache.get('SystemUserViewSet.get.' + request.user.username):
                queryset = cache.get('SystemUserViewSet.get.' + request.user.username)
            else:
                for res in Permission.objects.filter(Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(
                        User=request.user.id)):
                    queryset += list(res.SystemUser.all())
                queryset = list(set(queryset))
                cache.set('SystemUserViewSet.get.' + request.user.username, queryset)
            if uuid:
                aim = SystemUser.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = SystemUser.objects.get_by_id(uuid)
                    serializer = SystemUserSerializer(snippet)
                else:
                    serializer = SystemUserSerializer(None, many=True)
            else:
                serializer = SystemUserSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('add')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = SystemUser.objects.get_by_id(uuid)
            serializer = SystemUserSerializer(snippet, data=request.data)
        else:
            serializer = SystemUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('delete')
    def delete(self, request, uuid, format=None):
        snippet = SystemUser.objects.get_by_id(uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
