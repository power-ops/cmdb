from rest_framework import serializers
from asset.models import SystemUser
from management.utils import admin
from rest_framework.response import Response
from django.db.models import Q
from asset.models import Permission
from django.core.cache import cache
from management.mixins import MixinAPIView, MixinSearchView


class SystemUserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.DateTimeField(read_only=True)
    # bug: when makemigratoins django.db.utils.OperationalError: no such table: asset_protocol
    # Protocol = serializers.ChoiceField(choices=Protocol.objects.values_list('Protocol', 'Protocol').distinct(),
    #                                    label=_("Protocol"))

    class Meta:
        model = SystemUser
        fields = '__all__'


def get_queryset(user):
    queryset = []
    if cache.get('SystemUserViewSet.get.' + user.username):
        queryset = cache.get('SystemUserViewSet.get.' + user.username)
    else:
        for res in Permission.objects.filter(Q(UserGroup__in=[g.id for g in user.groups.all()]) | Q(
                User=user.id)):
            queryset += list(res.SystemUser.all())
        queryset = list(set(queryset))
        cache.set('SystemUserViewSet.get.' + user.username, queryset)
    return queryset


class SystemUserViewSet(MixinAPIView):
    serializer_class = SystemUserSerializer
    model = SystemUser

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, pk=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_pk(pk))
        elif request.user.has_perm('asset.view_self_assets'):
            return Response(self.get_serialiser_data_by_pk(pk, get_queryset(request)))


class SystemUserSearchView(MixinSearchView):
    serializer_class = SystemUserSerializer
    search_fields = ['Username']

    def get_queryset(self):
        if self.request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return SystemUser.objects.all()
        elif self.request.user.has_perm('asset.view_self_assets'):
            return get_queryset(self.request.user)
