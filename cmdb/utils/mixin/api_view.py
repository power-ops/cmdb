from rest_framework.views import APIView
from rest_framework.request import Request


class MixinAPIView(APIView):
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
