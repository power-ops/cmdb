from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import uuid
from management.mixins import MixinViewSet
from management.utils.csrf import CsrfExemptSessionAuthentication


class TokenSerializer(serializers.Serializer):
    aaa = serializers.CharField(max_length=40, required=True, allow_null=False,
                                label='aaa *')
    bbb = serializers.CharField(max_length=40, required=True, allow_null=False,
                                label='bbb *')

    class Meta:
        fields = '__all__'


class TokenView(MixinViewSet):
    serializer_class = TokenSerializer
    http_method_names = ['post']
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @swagger_auto_schema(
        operation_description='Token API',
        tags=['Example Token'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['aaa', 'bbb'],
            properties={
                'aaa': openapi.Schema(type=openapi.TYPE_STRING),
                'bbb': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                '{"token": "xxxx", success": True}'),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response('{"success": False, "message": "<error message>"}'),
        },
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        reply = {
            'success': False,
            'message': "unknown error"
        }
        if serializer.is_valid():
            reply = {"token": str(uuid.uuid4()), "success": True}
            return Response(reply, status=status.HTTP_200_OK)
        if serializer.errors:
            reply['message'] = serializer.errors
        return Response(reply, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
