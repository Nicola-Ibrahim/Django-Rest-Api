from apps.accounts.api.permissions.mixins import BasePermissionMixin
from apps.core.base_api.views import BaseAPIView, BaseGenericAPIView

from . import exceptions, responses, serializers


class LoginView(BaseGenericAPIView):
    """View for user logging"""

    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user")

        return responses.LoginResponse().with_data(user_details=user.get_user_details())


class LogoutView(BasePermissionMixin, BaseGenericAPIView):
    """View for user logout"""

    serializer_class = serializers.LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return responses.LogoutResponse()


class CheckJWTTokenView(BasePermissionMixin, BaseAPIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_password_changed:
            raise exceptions.FirstTimePasswordError().with_data(token=self.request.user.get_tokens()["access"])

        return responses.CheckJWTTokenResponse(user=request.user)
