from rest_framework import serializers
from domain.models import Domain
from cmdb.mixin import MixinAPIView


class DomainSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Domain
        fields = '__all__'


class DomainViewSet(MixinAPIView):
    serializer_class = DomainSerializer
    model = Domain
