from rest_framework import serializers
from asset.models import SystemUser
from utils import admin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.db.models import Q
from asset.models import Permission
from rest_framework.request import Request


class SystemUserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = SystemUser
        fields = '__all__'


class SystemUserViewSet(APIView):
    serializer_class = SystemUserSerializer

    def get_object(self, pk):
        try:
            return SystemUser.objects.get(pk=pk)
        except SystemUser.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        self.http_method_names = ['options', 'head', 'get']
        if 'post' not in self.http_method_names and request.user.has_perm('systemuser.add_systemuser'):
            self.http_method_names.append("post")
        if 'delete' not in self.http_method_names and request.user.has_perm('systemuser.delete_systemuser'):
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

    @admin.api_permission('systemuser.view_systemuser', 'asset.view_self_assets')
    def get(self, request, uuid=None, format=None):
        if request.user.has_perm('systemuser.view_systemuser'):
            if uuid:
                snippet = self.get_object(uuid)
                serializer = SystemUserSerializer(snippet)
            else:
                queryset = SystemUser.objects.all()
                serializer = SystemUserSerializer(queryset, many=True)
            return Response(serializer.data)
        elif request.user.has_perm('asset.view_self_assets'):
            queryset = []
            for res in Permission.objects.filter(Q(UserGroup__in=[g.id for g in request.user.groups.all()]) | Q(
                    User=request.user.id)):
                queryset += list(res.SystemUser.all())
            queryset = list(set(queryset))
            if uuid:
                aim = SystemUser.objects.filter(uuid=uuid)
                if aim in queryset:
                    snippet = self.get_object(uuid)
                    serializer = SystemUserSerializer(snippet)
                else:
                    serializer = SystemUserSerializer(None, many=True)
            else:
                serializer = SystemUserSerializer(queryset, many=True)
            return Response(serializer.data)

    @admin.api_permission('asset.add_asset')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = self.get_object(uuid)
            serializer = SystemUserSerializer(snippet, data=request.data)
        else:
            serializer = SystemUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('asset.delete_asset')
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
