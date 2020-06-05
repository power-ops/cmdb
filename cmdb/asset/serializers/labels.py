from rest_framework import serializers
from asset.models import Label
from utils import admin
from rest_framework.response import Response
from rest_framework import status
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
            if uuid:
                snippet = self.model.objects.get_by_id(uuid)
                serializer = self.serializer_class(snippet)
            else:
                queryset = self.model.objects.all()
                serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in getSelfAssets(request):
                queryset += list(res.Labels.all())
            queryset = list(set(queryset))
            if uuid:
                aim = self.model.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = self.model.objects.get_by_id(uuid)
                    serializer = self.serializer_class(snippet)
                else:
                    serializer = self.serializer_class(None, many=True)
            else:
                serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
