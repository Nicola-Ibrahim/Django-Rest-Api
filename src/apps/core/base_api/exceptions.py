import enum

from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class ErrorCode(enum.Enum):
    Not_Authenticated = "not_authenticated"
    Permission_Denied = "permission_denied"
    Field_Error = "field_error"


class BaseException(APIException):
    """
    Base class for exceptions.
    Subclasses should provide `.detail_` and `.status_code` properties.
    """

    detail_ = None

    status_code = status.HTTP_200_OK

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code

        if detail is None:
            detail = self.detail_

        if code is None:
            code = self.status_code

        # For  failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)

    def with_data(self, **kwargs):
        """Update the data dictionary in The Response"""
        return self


class NotAuthenticated(BaseException):
    detail_ = {
        "code": ErrorCode.Not_Authenticated.value,
        "detail": "Authentication credentials were not provided.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED


class PermissionDenied(BaseException):
    detail_ = {
        "code": ErrorCode.Permission_Denied.value,
        "detail": "You do not have permission to perform this action.",
    }
    status_code = status.HTTP_403_FORBIDDEN


class SerializerFieldsError(BaseException):
    detail_ = {
        "code": ErrorCode.Field_Error.value,
        "detail": [],
    }
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "invalid"

    def with_data(self, errors: dict):
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

        _create_error_list(errors=errors)

        return super().with_data()
