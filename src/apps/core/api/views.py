from rest_framework.generics import GenericAPIView

from . import exceptions


class CustomGenericAPIView(GenericAPIView):
    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated()
        raise exceptions.PermissionDenied(detail=message, code=code)
