"""
This script defines custom formatted exceptions for handling errors in the system.
"""

import enum

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from src.apps.core.base_api.exceptions import BaseException


class ErrorCode(enum.Enum):
    Not_Exists = _("not_exists")
    OTP_Wrong = _("OTP_Wrong")
    OTP_Expired = _("OTP_expired")
    OTP_Not_Verified = _("OTP_not_verified")
    User_Not_Active = _("user_not_active")
    Not_Similar_Passwords = "not_similar_passwords"
    Wrong_Password = _("wrong_password")
    First_Time_Password = _("first_time_password")
    Not_Valid = _("not_valid")


class UserNotExists(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Exists.value,
        "detail": _("The user does not exists."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class UserNotActive(BaseException):
    detail_ = {
        "code": ErrorCode.User_Not_Active.value,
        "detail": _("Account is inactive, please contact the admin"),
    }
    status_code = status.HTTP_403_FORBIDDEN


class NotSimilarPasswords(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Similar_Passwords.value,
        "detail": _("The two password fields didn't match."),
    }
    status_code = status.HTTP_400_BAD_REQUEST


class WrongPassword(BaseException):
    detail_ = {
        "code": ErrorCode.Wrong_Password.value,
        "detail": _("The old password is wrong."),
    }
    status_code = status.HTTP_400_BAD_REQUEST


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


class UserSerializerNotFound(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Exists.value,
        "detail": _("The type of the user serializer is not found"),
    }
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordNotValid(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Valid.value,
        "detail": _("The password is not valid"),
        "data": {},
    }
    status_code = status.HTTP_400_BAD_REQUEST

    def with_data(self, errors):
        self.detail_["data"] = errors
        return super().with_data()
