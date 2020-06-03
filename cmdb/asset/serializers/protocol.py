from rest_framework import serializers
from asset.models import Protocol
from utils import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from asset.views import getSelfAssets
from rest_framework.request import Request


class ProtocolSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Protocol
        fields = '__all__'


class ProtocolViewSet(APIView):
    serializer_class = ProtocolSerializer

    def get_object(self, pk):
        try:
            return Protocol.objects.get(pk=pk)
        except Protocol.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        self.http_method_names = ['options', 'head', 'get']
        if 'post' not in self.http_method_names and request.user.has_perm('protocol.add_protocol'):
            self.http_method_names.append("post")
        if 'delete' not in self.http_method_names and request.user.has_perm('protocol.delete_protocol'):
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

    @admin.api_permission('protocol.view_protocol', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('protocol.view_protocol'):
            if uuid:
                snippet = self.get_object(uuid)
                serializer = ProtocolSerializer(snippet)
            else:
                queryset = Protocol.objects.all()
                serializer = ProtocolSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in getSelfAssets(request):
                queryset += list(res.Protocols.all())
            queryset = list(set(queryset))
            if uuid:
                aim = Protocol.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = self.get_object(uuid)
                    serializer = ProtocolSerializer(snippet)
                else:
                    serializer = ProtocolSerializer(None, many=True)
            else:
                serializer = ProtocolSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('protocol.add_protocol')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = self.get_object(uuid)
            serializer = ProtocolSerializer(snippet, data=request.data)
        else:
            serializer = ProtocolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('protocol.delete_protocol')
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
