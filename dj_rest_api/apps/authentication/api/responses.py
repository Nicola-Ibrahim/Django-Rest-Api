import enum

from django.utils.translation import gettext_lazy as _
from lib.api.responses import BaseAPIResponse
from rest_framework import status


class OperationCode(enum.Enum):
    Created = _("created")
    Updated = _("updated")
    Deleted = _("deleted")
    Login = _("login")
    Logout = _("logout")
    Verified_OTP = _("verified_OTP")
    Reset_Password = _("reset_password")
    Forget_Password = _("forget_password")
    First_Time_Password = _("first_time_password")
    JWT_Checked = _("JWT_checked")
    Activated_Account = _("activated_account")


class LoginResponse(BaseAPIResponse):
    data_ = {
        "code": OperationCode.Login.value,
        "detail": _("The user has been logged in"),
        "data": {},
    }
    status_ = status.HTTP_200_OK

    def format_data(self, user_details):
        self.data_["data"] = user_details
        return super().format_data()


class LogoutResponse(BaseAPIResponse):
    data_ = {
        "code": OperationCode.Logout.value,
        "detail": _("The user has been logout"),
    }
    status_ = status.HTTP_204_NO_CONTENT


class ActivatedAccount(BaseAPIResponse):
    data_ = {
        "code": OperationCode.Activated_Account.value,
        "detail": _("The account has been activated successfully."),
    }
    status_ = status.HTTP_200_OK


class VerifyOTPResponse(BaseAPIResponse):
    data_ = {
        "code": OperationCode.Verified_OTP.value,
        "detail": _("The OTP number has been verified"),
        "data": {},
    }

    status_ = status.HTTP_200_OK

    def format_data(self, access_token: str):
        if access_token:
            self.data_["data"]["access_token"] = access_token

        return super().format_data()


class ResetPasswordResponse(BaseAPIResponse):
    data_ = {
        "code": OperationCode.Reset_Password.value,
        "detail": _("The password reset successfully"),
    }
    status_ = status.HTTP_200_OK


class ForgetPasswordRequestResponse(BaseAPIResponse):
    data_ = {
        "code": OperationCode.Forget_Password.value,
        "detail": _("An OTP number has been sent to email."),
    }
    status_ = status.HTTP_200_OK
