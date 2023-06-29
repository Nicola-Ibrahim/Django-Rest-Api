from src.apps.accounts.api.permissions.mixins import BasePermissionMixin
from src.apps.core.base_api.views import BaseAPIView, BaseGenericAPIView

from ...core import mailers
from . import exceptions as authentication_exceptions
from . import responses as authentication_responses
from .serializers.serializers import (
    ChangePasswordSerializer,
    FirstTimePasswordSerializer,
    ForgetPasswordRequestSerializer,
    ForgetPasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    VerifyOTPNumberSerializer,
)


class LoginView(BaseGenericAPIView):
    """View for user logging"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user")

        return authentication_responses.LoginResponse(user=user)


class LogoutView(BasePermissionMixin, BaseGenericAPIView):
    """View for user logout"""

    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return authentication_responses.LogoutResponse()


class ForgetPasswordRequestView(BaseGenericAPIView):
    """View for sending an OTP number to the user's email for changing the password"""

    serializer_class = ForgetPasswordRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        # Validate user's email and check existence
        serializer.is_valid(raise_exception=True)

        # Create OTP number for the user
        serializer.save()

        # Send reset password message with OTP to user's email
        mailers.OTPMailer(
            to_email=serializer.validated_data.get("email"),
            otp_number=serializer.validated_data.get("otp"),
        ).send_email()

        user = serializer.validated_data.get("user")
        return authentication_responses.ForgetPasswordRequestResponse(user=user)


class VerifyOTPNumberView(BasePermissionMixin, BaseGenericAPIView):
    """View for verifying the generated OTP number for the user who wants to change password."""

    serializer_class = VerifyOTPNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return authentication_responses.VerifyOTPResponse()


class BaseResetPasswordView(BasePermissionMixin, BaseGenericAPIView):
    """
    Abstract base view for setting new password
    This model implements patch method, so the
    concrete ResetPassword class only have to set serializer_class attribute.
    """

    class Meta:
        abstract = True

    def patch(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return authentication_responses.ResetPasswordResponse()


class ForgetPasswordView(BaseResetPasswordView):
    """View for resetting the forgotten password"""

    serializer_class = ForgetPasswordSerializer


class ChangePasswordView(BaseResetPasswordView):
    """View for changing password"""

    serializer_class = ChangePasswordSerializer


class FirstTimePasswordView(BaseResetPasswordView):
    """View for setting the first time password"""

    serializer_class = FirstTimePasswordSerializer


class CheckJWTTokenView(BasePermissionMixin, BaseAPIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_password_changed:
            raise authentication_exceptions.FirstTimePasswordError(user=request.user)

        return authentication_responses.CheckJWTTokenResponse(user=request.user)
