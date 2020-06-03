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

    def get_object(self, pk):
        try:
            return Label.objects.get(pk=pk)
        except Label.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        self.http_method_names = ['options', 'head', 'get']
        if 'post' not in self.http_method_names and request.user.has_perm('label.add_label'):
            self.http_method_names.append("post")
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

    @admin.api_permission('label.add_label')
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

    @admin.api_permission('label.delete_label')
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
