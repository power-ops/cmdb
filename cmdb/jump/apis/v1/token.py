from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from management.mixins import MixinViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from management.utils import aksk, csrf


class TokenSerializer(serializers.Serializer):
    data = serializers.JSONField(required=True, allow_null=False,
                                 label='data *')

    class Meta:
        fields = '__all__'


class TokenCreateView(MixinViewSet):
    serializer_class = TokenSerializer
    http_method_names = ['post']
    authentication_classes = (csrf.ExemptSessionAuthentication,)

    @swagger_auto_schema(
        operation_description='Token New API',
        tags=['Token'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'data': openapi.Schema(type=openapi.TYPE_OBJECT),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                '{"ak": "xxxx", "sk":"xxx", "success": True}'),
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
            ak, sk = aksk.New(serializer.data.get('data'))
            reply = {"ak": ak, "sk": sk, "success": True}
            return Response(reply, status=status.HTTP_200_OK)
        if serializer.error_messages:
            reply['message'] = serializer.error_messages
        return Response(reply, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TokenView(MixinViewSet):
    serializer_class = TokenSerializer
    http_method_names = ['get']
    authentication_classes = (csrf.ExemptSessionAuthentication,)

    @swagger_auto_schema(
        operation_description='Token API',
        tags=['Token'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                '{"data": jsonObject, "success": True}'),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                '{"message": "NOT FOUND", "success": False}'),
        },
    )
    def get(self, request, pk=None, format=None):
        reply = {
            'success': False,
            'message': "unknown error"
        }
        if pk:
            data = aksk.Get(pk)
            reply['data'] = data.get('data')
            reply['sk'] = data.get('sk')
            reply['message'] = "success"
            data.delete()
            return Response(reply, status=status.HTTP_200_OK)
        else:
            reply['message'] = "NOT FOUND"
        return Response(reply, status=status.HTTP_404_NOT_FOUND)
