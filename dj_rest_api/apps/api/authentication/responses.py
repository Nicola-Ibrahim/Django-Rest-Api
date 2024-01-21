import enum
from typing import Any

from apps.api.base.responses import BaseAPIResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class OperationCode(enum.Enum):
    Login = _("login")
    Logout = _("logout")
    Verified_OTP = _("verified_OTP")
    Reset_Password = _("reset_password")
    Forget_Password = _("forget_password")
    First_Time_Password = _("first_time_password")
    JWT_Checked = _("JWT_checked")
    Activated_Account = _("activated_account")


class LoginAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": OperationCode.Login.value,
                "detail": _("The user has been logged in"),
                "data": data,
            }

        return super().format_response()


class LogoutResponse(BaseAPIResponse):
    default_status = status.HTTP_204_NO_CONTENT

    def format_response(self) -> dict:
        return {
            "code": OperationCode.Logout.value,
            "detail": _("The user has been logout"),
        }


class VerifyOTPAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": OperationCode.Verified_OTP.value,
                "detail": _("The OTP number has been verified"),
                "data": data,
            }

        return super().format_response()


class ResetPasswordAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_response(self) -> dict:
        return {
            "code": OperationCode.Reset_Password.value,
            "detail": _("The password reset successfully"),
        }


class ForgetPasswordRequestAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_response(self, data) -> dict:
        return {
            "code": OperationCode.Forget_Password.value,
            "detail": _("An OTP number has been sent to email."),
        }
