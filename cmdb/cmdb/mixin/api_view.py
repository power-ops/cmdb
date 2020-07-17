from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from cmdb.utils import admin
from django.http import Http404
from django.shortcuts import redirect


class MixinAPIView(APIView):
    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        if 'post' not in self.http_method_names and request.user.has_perm(
                self._class_name + '.add_' + self._class_name):
            self.http_method_names.append("post")
        if 'delete' not in self.http_method_names and request.user.has_perm(
                self._class_name + '.delete_' + self._class_name):
            self.http_method_names.append("delete")

    @property
    def _class_name(self):
        return str(self.__class__).split('.')[-2]

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
    def get(self, request, pk=None, format=None):
        return Response(self.get_serialiser_data_by_pk(pk))

    @admin.api_permission('add')
    def post(self, request, pk=None, format=None):
        if pk:
            snippet = self.get_object(pk)
            serializer = self.serializer_class(snippet, data=request.data)
        else:
            serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @admin.api_permission('delete')
    def delete(self, request, pk=None, format=None):
        if pk:
            snippet = self.get_object(pk)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def get_serialiser_data_by_pk(self, pk=None, queryset=None):
        if queryset != None:
            if pk:
                aim = self.get_object(pk)
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
                return self.get_serialiser_data_by_pk(pk, all)
            else:
                return self.serializer_class(None, many=True).data


class MixinSearchView(GenericAPIView):
    filter_backends = [SearchFilter]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        if request.GET.get('search'):
            return self.list(request, *args, **kwargs)
        return redirect(request.build_absolute_uri('?') + '/')

    @property
    def _class_name(self):
        return str(self.__class__).split('.')[-2]
