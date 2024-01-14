import enum

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class ErrorCode(enum.Enum):
    Not_Exists = _("not_exists")
    Not_Authenticated = "not_authenticated"
    JWT_No_Type = _("JWT_no_type")
    JWT_No_Id = _("JWT_no_id")
    JWT_Wrong_Type = _("JWT_wrong_type")
    JWT_token_not_valid = _("token_not_valid")
    Bad_Authorization_Header = _("bad_authorization_header")
    Permission_Denied = _("permission_denied")
    Field_Error = "field_error"


class BaseAPIException(APIException):
    """
    Base class for exceptions.
    Subclasses should provide `.detail_` and `.status_code` properties.
    """

    detail_ = None

    status_code = status.HTTP_200_OK

    def __init__(self, detail=None, code=None, status_code=None):
        detail = detail or self.detail_
        code = code or self.status_code
        status_code = status_code or self.status_code

        # For  failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)

    def format_response(self, **kwargs):
        """Update the data dictionary in The Response"""


class NotAuthenticated(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Not_Authenticated.value,
        "detail": "Authentication credentials were not provided.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class JWTAccessTokenNotValid(BaseAPIException):
    detail_ = {
        "code": ErrorCode.JWT_token_not_valid.value,
        "detail": _("Given access token not valid for any token type or expired."),
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class JWTAccessTokenNotExists(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Not_Exists.value,
        "detail": _("The access token does not exists in the header."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasNoType(BaseAPIException):
    detail_ = {
        "code": ErrorCode.JWT_No_Type.value,
        "detail": _("The access token has no type."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAccessTokenHasWrongType(BaseAPIException):
    detail_ = {
        "code": ErrorCode.JWT_Wrong_Type.value,
        "detail": _("The access token has wrong type."),
    }
    status_code = status.HTTP_400_BAD_REQUEST


class JWTAccessTokenHasNoId(BaseAPIException):
    detail_ = {
        "code": ErrorCode.JWT_No_Id.value,
        "detail": _("The access token has no id."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTRefreshTokenHasNoType(BaseAPIException):
    detail_ = {
        "code": ErrorCode.JWT_No_Type.value,
        "detail": _("The refresh token has no type."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTRefreshTokenHasWrongType(BaseAPIException):
    detail_ = {
        "code": ErrorCode.JWT_Wrong_Type.value,
        "detail": _("The refresh token has wrong type."),
    }
    status_code = status.HTTP_400_BAD_REQUEST


class JWTRefreshTokenHasNoId(BaseAPIException):
    detail_ = {
        "code": ErrorCode.JWT_No_Id.value,
        "detail": _("The refresh token has no id."),
    }
    status_code = status.HTTP_404_NOT_FOUND


class JWTAuthenticationFailed(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Bad_Authorization_Header.value,
        "detail": _("Authorization header must contain two space-delimited values."),
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDenied(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Permission_Denied.value,
        "detail": "You do not have permission to perform this action.",
    }
    status_code = status.HTTP_403_FORBIDDEN


class SerializerFieldsError(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Field_Error.value,
        "detail": [],
    }
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "invalid"

    def __init__(self, errors: dict, detail=None, code=None, status_code=None):
        self.format_response(errors=errors)
        super().__init__(detail, code, status_code)

    def format_response(self, errors: dict):
        def _get_error_code(error_detail):
            """Get the error code associated with the occurred error"""
            if hasattr(error_detail, "code"):
                error_code = error_detail.code
            else:
                error_code = self.default_code

            return error_code

        def _get_error_message(error_detail):
            """Get the error message associated with the occurred error"""

            return error_detail[0]

        def _create_error_list(errors: dict):
            # loop on all field that have wrong inputs
            for field, error in errors.items():
                if isinstance(error, list):
                    error_message = _get_error_message(error_detail=error)

                    self.detail_["code"] = _get_error_code(error_detail=error[0])
                    self.detail_["detail"].append(f"Error in {field} : {error_message}")

                if isinstance(error, dict):
                    return _create_error_list(error)

        # Reset detail befor appending new error messages
        self.detail_["detail"] = []

        _create_error_list(errors=errors)
