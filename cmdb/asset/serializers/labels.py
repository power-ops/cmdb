from rest_framework import serializers
from asset.models import Label
from cmdb.utils import admin
from rest_framework.response import Response
from asset.utils import get_self_assets
from cmdb.mixin import MixinAPIView, MixinSearchView


class LabelSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Label
        fields = '__all__'


class LabelViewSet(MixinAPIView):
    serializer_class = LabelSerializer
    model = Label

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, pk=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_pk(pk))
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in get_self_assets(request):
                queryset += list(res.Labels.all())
            return Response(self.get_serialiser_data_by_pk(pk, list(set(queryset))))


class LabelSearchView(MixinSearchView):
    serializer_class = LabelSerializer
    search_fields = ['Name']

    def get_queryset(self):
        if self.request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Label.objects.all()
        elif self.request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in get_self_assets(self.request):
                queryset += list(res.Labels.all())
            return list(set(queryset))
