from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, JSONParser
from rest_framework.views import APIView

from .exceptions import NotAuthenticated, PermissionDenied
from .parsers import PlainTextParser
from .responses import LanguagesListResponse


class BaseGenericApiView(GenericAPIView):
    parser_classes = [JSONParser, PlainTextParser, FormParser]

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated()
        raise PermissionDenied(detail=message, code=code)


class BaseApiView(APIView):
    parser_classes = [JSONParser, PlainTextParser, FormParser]

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise NotAuthenticated()
        raise PermissionDenied(detail=message, code=code)


class LanguagesListView(BaseApiView):
    def get(self, request, *args, **kwargs):
        # Get the list of available supported languages.
        languages = settings.LANGUAGES

        return LanguagesListResponse(languages=languages)
