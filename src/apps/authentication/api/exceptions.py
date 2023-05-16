"""
This script defines custom formatted exceptions for handling errors in the system.
"""

import enum

from rest_framework import status

from apps.core.api.exceptions import BaseExceptions


class ErrorCode(enum.Enum):
    Not_Exists = "not_exists"
    Not_Found = "not_found"
    Not_Allowed = "not_allowed"
    Expired_OTP = "expired_OTP"
    Not_Authenticated = "not_authenticated"
    Permission_Denied = "permission_denied"
    Credential_Error = "credential_error"
    User_Not_Active = "user_not_active"
    Verified_OTP = "verified_OTP"
    Not_Similar_Passwords = "not_similar_passwords"
    Wrong_Password = "wrong_password"
    Field_Error = "field_error"
    JWT_No_Type = "JWT_no_type"
    JWT_No_Id = "JWT_no_id"
    JWT_Wrong_Type = "JWT_wrong_type"
    JWT_token_not_valid = "token_not_valid"
    Bad_Authorization_Header = "bad_authorization_header"


class UserNotExists(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Exists.value,
        "detail": "The user does not exists.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class WrongCredentials(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Credential_Error.value,
        "detail": "Unable to log in with provided credentials.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class UserNotActive(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.User_Not_Active.value,
        "detail": "Account is inactive, please contact the admin",
    }
    status_code = status.HTTP_403_FORBIDDEN


class JWTAccessTokenNotExists(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Exists.value,
        "detail": "The access token does not exists in the header.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasNoType(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_No_Type.value,
        "detail": "The access token has no type.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasWrongType(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_Wrong_Type.value,
        "detail": "The access token has wrong type.",
    }
    status_code = status.HTTP_400_BAD_REQUEST


class JWTAccessTokenHasNoId(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_No_Id.value,
        "detail": "The access token has no id.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTRefreshTokenHasNoType(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_No_Type.value,
        "detail": "The refresh token has no type.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTRefreshTokenHasWrongType(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_Wrong_Type.value,
        "detail": "The refresh token has wrong type.",
    }
    status_code = status.HTTP_400_BAD_REQUEST


class JWTRefreshTokenHasNoId(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_No_Id.value,
        "detail": "The refresh token has no id.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenNotValid(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.JWT_token_not_valid.value,
        "detail": "Given access token not valid for any token type or expired.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class JWTAuthenticationFailed(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Bad_Authorization_Header.value,
        "detail": "Authorization header must contain two space-delimited values.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class OTPNotExists(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Exists.value,
        "detail": "The OTP number does not exists.",
    }
    status_code = status.HTTP_404_NOT_FOUND


class OTPExpired(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Expired_OTP.value,
        "detail": "The OTP number has been expired, please resubmit your credential again.",
    }
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class OTPNotVerified(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Verified_OTP.value,
        "detail": "The OTP number must be verified, please verify it first.",
    }
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class NotSimilarPasswords(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Similar_Passwords.value,
        "detail": "The two password fields didn't match.",
    }
    status_code = status.HTTP_400_BAD_REQUEST


class WrongPassword(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Wrong_Password.value,
        "detail": "The current password is wrong.",
    }
    status_code = status.HTTP_400_BAD_REQUEST


class SerializerFieldsError(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Field_Error.value,
        "detail": "An error occurred in the fields",
        "data": {},
    }
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, errors, detail=None, code=None, status_code=None):
        self.update_data(errors=errors)
        super().__init__(detail, code, status_code)

    def update_data(self, **kwargs):
        errors = kwargs.get("errors")

        if errors:
            self.detail_["data"]["errors"] = errors
        return super().update_data(**kwargs)


class UserSerializerNotFound(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Found.value,
        "detail": "The user serializer not found",
        "data": {},
    }
    status_code = status.HTTP_404_NOT_FOUND


class UserFilterNotFound(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Found.value,
        "detail": "The user filter class not found",
        "data": {},
    }
    status_code = status.HTTP_404_NOT_FOUND


class UserModelNotFound(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Found.value,
        "detail": "The user model class not found",
        "data": {},
    }
    status_code = status.HTTP_404_NOT_FOUND


class DeleteMultipleUsers(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Allowed.value,
        "detail": "delete multiple user not allowed for non admin user",
        "data": {},
    }
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED


class UpdateMultipleUsers(BaseExceptions):
    detail_ = {
        "error": True,
        "error_code": ErrorCode.Not_Allowed.value,
        "detail": "update multiple user not allowed for non admin user",
        "data": {},
    }
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
