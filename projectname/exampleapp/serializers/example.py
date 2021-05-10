from rest_framework import serializers
from exampleapp.models import ExampleModel
from rest_framework.response import Response
from management.mixins import MixinAPIView, MixinSearchView


class ExampleSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ExampleModel
        fields = '__all__'


class ExampleViewSet(MixinAPIView):
    serializer_class = ExampleSerializer
    model = ExampleModel

    def get(self, request, pk=None, format=None):
        return Response(self.get_serialiser_data_by_pk(pk))


class ExampleSearchView(MixinSearchView):
    serializer_class = ExampleSerializer
    search_fields = ['uuid']

    def get_queryset(self):
        return ExampleModel.objects.all()
