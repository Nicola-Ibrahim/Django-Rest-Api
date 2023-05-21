"""
This script defines custom formatted responses for the api views.
"""
import enum
import logging

from rest_framework import status
from rest_framework.response import Response

from apps.core.api.responses import BaseResponse

logger = logging.getLogger(__name__)


class OperationCode(enum.Enum):
    Created = "created"
    Updated = "updated"
    Deleted = "deleted"
    Login = "login"
    Logout = "logout"
    First_Time_Password = "first_time_password"
    Reset_Password = "reset_password"
    Forget_Password = "forget_password"
    Verified_OTP = "verified_OTP"
    Activated_Account = "activated_account"


class LoginResponse(BaseResponse):
    data_ = {
        "error": False,
        "operation_code": OperationCode.Login.value,
        "data": {},
    }
    status_ = status.HTTP_200_OK

    def __init__(
        self,
        email: str,
        groups: list,
        tokens: dict,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        self.update_data(email=email, groups=groups, tokens=tokens)
        super().__init__(data, status, template_name, headers, exception, content_type)

    def update_data(self, **kwargs):
        self.data_["data"]["email"] = kwargs.get("email", None)
        self.data_["data"]["groups"] = kwargs.get("groups", None)
        self.data_["data"]["tokens"] = {
            "refresh": kwargs.get("tokens")["refresh"],
            "access": kwargs.get("tokens")["access"],
        }


class LogoutResponse(BaseResponse):
    data_ = {
        "error": False,
        "operation_code": OperationCode.Logout.value,
        "data": {
            "message": "The user has been logout",
        },
    }
    status_ = status.HTTP_204_NO_CONTENT


class FirstTimePasswordError(BaseResponse):
    data_ = {
        "error": False,
        "operation_code": OperationCode.First_Time_Password.value,
        "detail": "Password must be reset for the first logging.",
        "data": {
            "message": "Please change your default generated password.",
        },
    }
    status_ = status.HTTP_200_OK

    def __init__(
        self,
        access_token,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        self.update_data(access_token=access_token)
        super().__init__(data, status, template_name, headers, exception, content_type)

    def update_data(self, **kwargs):
        # Add access token to the data
        self.data_["data"]["access_token"] = kwargs.get("access_token", None)


class ForgetPasswordRequestResponse(BaseResponse):
    data_ = {
        "error": False,
        "operation_code": OperationCode.Forget_Password.value,
        "data": {
            "message": "We send you a number to email for resetting a new password.",
        },
    }
    status_ = status.HTTP_200_OK

    def __init__(
        self,
        access_token,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        self.update_data(access_token=access_token)
        super().__init__(data, status, template_name, headers, exception, content_type)

    def update_data(self, **kwargs):
        # Add access token to the data
        self.data_["data"]["access_token"] = kwargs.get("access_token", None)


class VerifyOTPResponse(BaseResponse):
    data_ = {
        "error": False,
        "operation_code": OperationCode.Verified_OTP.value,
        "data": {
            "message": "The OTP number has been verified",
        },
    }

    status_ = status.HTTP_200_OK


class ResetPasswordResponse(BaseResponse):
    data_ = {
        "error": False,
        "operation_code": OperationCode.Reset_Password.value,
        "data": {
            "message": "The password reset successfully",
        },
    }
    status_ = status.HTTP_200_OK


class ActivatedAccount(BaseResponse):
    data_ = {
        "error": False,
        "operation_code": OperationCode.Activated_Account.value,
        "data": {
            "message": "The account has been activated successfully.",
        },
    }
    status_ = status.HTTP_200_OK
