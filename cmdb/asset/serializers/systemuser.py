from rest_framework import serializers
from asset.models import SystemUser
from cmdb.utils import admin
from rest_framework.response import Response
from django.db.models import Q
from asset.models import Permission
from django.core.cache import cache
from cmdb.mixin import MixinAPIView


class SystemUserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = SystemUser
        fields = '__all__'


class SystemUserViewSet(MixinAPIView):
    serializer_class = SystemUserSerializer
    model = SystemUser

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        print("ssss",self.model.objects.all())
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_uuid(uuid))
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
            return Response(self.get_serialiser_data_by_uuid(uuid, queryset))
