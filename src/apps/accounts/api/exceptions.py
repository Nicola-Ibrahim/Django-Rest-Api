"""
This script defines custom formatted exceptions for handling errors in the system.
"""

import enum

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from src.apps.core.api.exceptions import BaseException


class ErrorCode(enum.Enum):
    Not_Exists = _("not_exists")
    OTP_Expired = _("OTP_expired")
    OTP_Not_Verified = _("OTP_not_verified")
    OTP_Wrong = _("OTP_wrong")
    Not_Authenticated = _("not_authenticated")
    Permission_Denied = _("permission_denied")
    Credential_Error = _("credential_error")
    User_Not_Active = _("user_not_active")
    Not_Similar_Passwords = "not_similar_passwords"
    Wrong_Password = _("wrong_password")
    JWT_No_Type = _("JWT_no_type")
    JWT_No_Id = _("JWT_no_id")
    JWT_Wrong_Type = _("JWT_wrong_type")
    JWT_token_not_valid = _("token_not_valid")
    Bad_Authorization_Header = _("bad_authorization_header")


class UserNotExists(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Exists.value,
        "detail": _("The user does not exists."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class CredentialsNotValid(BaseException):
    detail_ = {
        "code": ErrorCode.Credential_Error.value,
        "detail": _("Unable to log in with provided credentials."),
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotActive(BaseException):
    detail_ = {
        "code": ErrorCode.User_Not_Active.value,
        "detail": _("Account is inactive, please contact the admin"),
    }
    status_code = status.HTTP_403_FORBIDDEN


class JWTAccessTokenNotExists(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Exists.value,
        "detail": _("The access token does not exists in the header."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasNoType(BaseException):
    detail_ = {
        "code": ErrorCode.JWT_No_Type.value,
        "detail": _("The access token has no type."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasWrongType(BaseException):
    detail_ = {
        "code": ErrorCode.JWT_Wrong_Type.value,
        "detail": _("The access token has wrong type."),
    }
    status_code = status.HTTP_400_BAD_REQUEST


class JWTAccessTokenHasNoId(BaseException):
    detail_ = {
        "code": ErrorCode.JWT_No_Id.value,
        "detail": _("The access token has no id."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTRefreshTokenHasNoType(BaseException):
    detail_ = {
        "code": ErrorCode.JWT_No_Type.value,
        "detail": _("The refresh token has no type."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTRefreshTokenHasWrongType(BaseException):
    detail_ = {
        "code": ErrorCode.JWT_Wrong_Type.value,
        "detail": _("The refresh token has wrong type."),
    }
    status_code = status.HTTP_400_BAD_REQUEST


class JWTRefreshTokenHasNoId(BaseException):
    detail_ = {
        "code": ErrorCode.JWT_No_Id.value,
        "detail": _("The refresh token has no id."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenNotValid(BaseException):
    detail_ = {
        "code": ErrorCode.JWT_token_not_valid.value,
        "detail": _("Given access token not valid for any token type or expired."),
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class JWTAuthenticationFailed(BaseException):
    detail_ = {
        "code": ErrorCode.Bad_Authorization_Header.value,
        "detail": _("Authorization header must contain two space-delimited values."),
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class NotAuthenticated(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Authenticated.value,
        "detail": _("Authentication credentials were not provided."),
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDenied(BaseException):
    detail_ = {
        "code": ErrorCode.Permission_Denied.value,
        "detail": _("You do not have permission to perform this action."),
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


class UserSerializerNotFound(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Exists.value,
        "detail": _("The type of the user serializer is not found"),
    }
    status_code = status.HTTP_400_BAD_REQUEST
