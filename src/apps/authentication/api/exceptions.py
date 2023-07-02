"""
This script defines custom formatted exceptions for handling errors in the system.
"""

import enum

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from src.apps.core.base_api.exceptions import BaseException


class ErrorCode(enum.Enum):
    OTP_Expired = _("OTP_expired")
    OTP_Not_Verified = _("OTP_not_verified")
    OTP_Wrong = _("OTP_wrong")
    First_Time_Password = _("first_time_password")


class WrongOTP(BaseException):
    detail_ = {
        "code": ErrorCode.OTP_Wrong.value,
        "detail": _("The OTP number is wrong"),
    }
    status_code = status.HTTP_404_NOT_FOUND


class OTPExpired(BaseException):
    detail_ = {
        "code": ErrorCode.OTP_Expired.value,
        "detail": _("The OTP number has been expired, please resubmit your credential again."),
    }
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class OTPNotVerified(BaseException):
    detail_ = {
        "code": ErrorCode.OTP_Not_Verified.value,
        "detail": _("The OTP number must be verified, please verify it first."),
    }
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class FirstTimePasswordError(BaseException):
    detail_ = {
        "code": ErrorCode.First_Time_Password.value,
        "detail": _("Please change your default generated password"),
        "data": [],
    }
    status_code = status.HTTP_200_OK

    def with_data(self, access_token: str):
        self.detail_["data"]["access_token"] = access_token
        return super().with_data()
