from rest_framework import serializers
from asset.models import Label
from utils import admin
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
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

    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

    @admin.api_permission('view', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('label.view_label'):
            if uuid:
                snippet = self.get_object(uuid)
                serializer = LabelSerializer(snippet)
            else:
                queryset = Label.objects.all()
                serializer = LabelSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in getSelfAssets(request):
                queryset += list(res.Labels.all())
            queryset = list(set(queryset))
            if uuid:
                aim = Label.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = self.get_object(uuid)
                    serializer = LabelSerializer(snippet)
                else:
                    serializer = LabelSerializer(None, many=True)
            else:
                serializer = LabelSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('add')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = self.get_object(uuid)
            serializer = LabelSerializer(snippet, data=request.data)
        else:
            serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('delete')
    def delete(self, request, uuid, format=None):
        snippet = self.get_object(uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
