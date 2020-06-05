from rest_framework import serializers
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.request import Request
from domain.models import Domain


class DomainSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    CreateDate = serializers.CharField(read_only=True)

    class Meta:
        model = Domain
        fields = '__all__'


class DomainViewSet(APIView):
    serializer_class = DomainSerializer

    def get_object(self, pk):
        try:
            return Domain.objects.get(pk=pk)
        except Domain.DoesNotExist:
            raise Http404

    def http_methods(self, request):
        if 'post' not in self.http_method_names and request.user.has_perm('domain.add_domain'):
            self.http_method_names.append("post")
        if 'delete' not in self.http_method_names and request.user.has_perm('domain.delete_domain'):
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
