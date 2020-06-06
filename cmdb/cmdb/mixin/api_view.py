from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from cmdb.utils import admin
from django.http import Http404


class MixinAPIView(APIView):
    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        self._class_name = str(self.__class__).split('.')[-2]
        if 'post' not in self.http_method_names and request.user.has_perm(
            self._class_name + '.add_' + self._class_name):
            self.http_method_names.append("post")
        if 'delete' not in self.http_method_names and request.user.has_perm(
            self._class_name + '.delete_' + self._class_name):
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

    @admin.api_permission('view')
    def get(self, request, uuid=None, format=None):
        return Response(self.get_serialiser_data_by_uuid(uuid))

    @admin.api_permission('add')
    def post(self, request, uuid=None, format=None):
        if uuid:
            snippet = self.get_object(uuid)
            serializer = self.serializer_class(snippet, data=request.data)
        else:
            serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('delete')
    def delete(self, request, uuid, format=None):
        snippet = self.get_object(uuid)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serialiser_data_by_uuid(self, uuid=None, queryset=None):
        if queryset:
            if uuid:
                aim = self.get_object(uuid)
                if aim in queryset:
                    serializer = self.serializer_class(aim)
                else:
                    serializer = self.serializer_class(None, many=True)
            else:
                serializer = self.serializer_class(queryset, many=True)
            return serializer.data
        else:
            all = self.model.objects.all()
            if all:
                return self.get_serialiser_data_by_uuid(uuid, all)
            else:
                return self.serializer_class(None, many=True).data