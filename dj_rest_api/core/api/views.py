from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from . import exceptions


class BaseGenericAPIView(GenericAPIView):
    """Base extended class for GenericAPIView, implement custom behaviors"""

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticatedAPIException()
        raise exceptions.PermissionDeniedAPIException(detail=message, code=code)


class BaseAPIView(APIView):
    """Base extended class for BaseAPIView, implement custom behaviors"""

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticatedAPIException()
        raise exceptions.PermissionDeniedAPIException(detail=message, code=code)
