from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404


class MixinViewSet(APIView):
    serializer_class = None
    model = None

    def get(self, request, pk=None, format=None):
        return Response(self.get_serialiser_data_by_pk(pk))

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

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def get_serialiser_data_by_pk(self, pk=None, queryset=None):
        if queryset:
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
