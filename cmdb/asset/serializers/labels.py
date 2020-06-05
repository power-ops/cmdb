from rest_framework import serializers
from asset.models import Label
from utils import admin
from rest_framework.response import Response
from asset.views import getSelfAssets
from utils.mixin import MixinAPIView


class LabelSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Label
        fields = '__all__'


class LabelViewSet(MixinAPIView):
    serializer_class = LabelSerializer
    model = Label

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm(self._class_name + '.view_' + self._class_name):
            return Response(self.get_serialiser_data_by_uuid(uuid))
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in getSelfAssets(request):
                queryset += list(res.Labels.all())
            return Response(self.get_serialiser_data_by_uuid(uuid, list(set(queryset))))
