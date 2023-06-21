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

    def update_data(self, **kwargs):
        """Update the data dictionary in The Response"""
        pass


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
        "detail": "An error occurred in the fields",
        "data": {},
    }
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, errors, detail=None, code=None, status_code=None):
        self.update_data(errors=errors)
        super().__init__(detail, code, status_code)

    def update_data(self, **kwargs):
        field = list(kwargs.get("errors").keys())[0]
        error_detail = list(kwargs.get("errors").values())[0][0]

        if hasattr(error_detail, "code"):
            self.detail_["code"] = error_detail.code
        else:
            self.detail_["code"] = self.default_code

        if isinstance(error_detail, (list, tuple)):
            error_detail = error_detail[0]

        self.detail_["detail"] = "Error in " + field + " : " + error_detail.replace('"', "")
