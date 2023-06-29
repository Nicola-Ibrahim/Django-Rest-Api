"""
This script defines custom formatted responses for the api views.
"""
import enum

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from src.apps.core.base_api.responses import BaseResponse


class OperationCode(enum.Enum):
    Created = _("created")
    Updated = _("updated")
    Deleted = _("deleted")
    Login = _("login")
    Logout = _("logout")
    Reset_Password = _("reset_password")
    Forget_Password = _("forget_password")
    Verified_OTP = _("verified_OTP")
    JWT_Checked = _("JWT_checked")
    Activated_Account = _("activated_account")
    First_Time_Password = _("first_time_password")


class LoginResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Login.value,
        "detail": _("The user has been logged in"),
        "data": {},
    }
    status_ = status.HTTP_200_OK

    def __init__(
        self,
        user,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        self.update_data(user=user)
        super().__init__(data, status, template_name, headers, exception, content_type)

    def update_data(self, **kwargs):
        user = kwargs.get("user", None)
        if user:
            self.data_["data"] = user.get_user_details()


class LogoutResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Logout.value,
        "detail": _("The user has been logout"),
    }
    status_ = status.HTTP_204_NO_CONTENT


class ForgetPasswordRequestResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Forget_Password.value,
        "detail": _("An OTP number has been sent to email."),
        "data": {},
    }
    status_ = status.HTTP_200_OK

    def __init__(
        self,
        user,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        self.update_data(user=user)
        super().__init__(data, status, template_name, headers, exception, content_type)

    def update_data(self, **kwargs):
        user = kwargs.get("user", None)
        # Add access token to the data
        if user:
            self.data_["data"]["access_token"] = user.get_tokens()["access"]


class VerifyOTPResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Verified_OTP.value,
        "detail": _("The OTP number has been verified"),
    }

    status_ = status.HTTP_200_OK


class ResetPasswordResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Reset_Password.value,
        "detail": _("The password reset successfully"),
    }
    status_ = status.HTTP_200_OK


class ActivatedAccount(BaseResponse):
    data_ = {
        "code": OperationCode.Activated_Account.value,
        "detail": _("The account has been activated successfully."),
    }
    status_ = status.HTTP_200_OK
