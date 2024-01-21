import enum

from apps.api.base.exceptions import BaseAPIException
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class ErrorCode(enum.Enum):
    Credential_Error = _("credential_error")
    Not_Exists = _("not_exists")
    OTP_Wrong = _("OTP_Wrong")
    OTP_Expired = _("OTP_expired")
    OTP_Not_Verified = _("OTP_not_verified")
    User_Not_Active = _("user_not_active")
    Not_Similar_Passwords = "not_similar_passwords"
    Wrong_Password = _("wrong_password")
    First_Time_Password = _("first_time_password")
    Not_Valid = _("not_valid")


class UserNotActiveAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.User_Not_Active.value,
        "detail": _("Account is inactive, please contact the admin"),
    }
    status_code = status.HTTP_403_FORBIDDEN


class NotSimilarPasswordsAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Not_Similar_Passwords.value,
        "detail": _("The two password fields didn't match."),
    }
    status_code = status.HTTP_400_BAD_REQUEST


class WrongPasswordAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Wrong_Password.value,
        "detail": _("The old password is wrong."),
    }
    status_code = status.HTTP_400_BAD_REQUEST


class WrongOTPAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.OTP_Wrong.value,
        "detail": _("The OTP number is wrong"),
    }
    status_code = status.HTTP_404_NOT_FOUND


class ExpiredOTPAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.OTP_Expired.value,
        "detail": _("The OTP number has been expired, please resubmit your credential again."),
    }
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class OTPNotVerifiedAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.OTP_Not_Verified.value,
        "detail": _("The OTP number must be verified, please verify it first."),
    }
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class FirstTimePasswordAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.First_Time_Password.value,
        "detail": _("Please change your default generated password"),
        "data": [],
    }
    status_code = status.HTTP_200_OK

    def format_response(self, access_token: str):
        self.detail_["data"]["access_token"] = access_token
        return super().format_response()


class CredentialsNotValidAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Credential_Error.value,
        "detail": _("Unable to log in with provided credentials."),
    }
    status_code = status.HTTP_401_UNAUTHORIZED
