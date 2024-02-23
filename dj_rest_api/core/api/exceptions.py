import enum
from typing import T

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class ErrorCode(enum.Enum):
    Field_Error = _("field_error")
    Permission_Denied = _("permission_denied")
    Not_Authenticated = _("not_authenticated")


class BaseAPIException(APIException):
    """
    Base class for custom API exceptions in the application.

    Attributes:
        default_detail (str): Default detail message for the exception.
        status_code (int): HTTP status code associated with the exception.

    Usage Example:
        This class is intended to be subclassed for creating specific API exceptions.
    """

    default_detail = None

    status_code = status.HTTP_200_OK

    def __init__(self, detail=None, code=None, status_code=None) -> None:
        """
        Initializes the BaseAPIException instance.

        Args:
            detail: Custom error detail message or a list/tuple of error messages.
            code: Custom error code.
            status_code: Custom HTTP status code.

        Returns:
            None
        """
        detail = self.format_default_detail(detail) or self.default_detail
        code = code or self.status_code
        status_code = status_code or self.status_code

        # For  failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)

    def format_default_detail(self, detail: T | None = None) -> T | None:
        """Updates the detail in the Exception."""
        return detail


class SerializerFieldsAPIException(BaseAPIException):
    default_detail = {
        "code": ErrorCode.Field_Error.value,
        "detail": [],
    }
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "invalid"

    def format_default_detail(self, detail: T | None = None) -> T | None:
        def _get_error_code(error):
            """Get the error code associated with the occurred error"""

            if hasattr(error, "code"):
                error_code = error.code
            else:
                error_code = self.default_code

            return error_code

        def _get_error_message(error: list):
            """Get the error message associated with the occurred error"""

            return error[0][0]

        def _create_error_list(errors: dict):
            # loop on all field that have wrong inputs
            for field, error in errors.items():
                if isinstance(error, list):
                    # self.default_detail["code"] = _get_error_code(error)
                    self.default_detail["detail"].append(f"Error in {field}: {_get_error_message(error)}")

                if isinstance(error, dict):
                    return _create_error_list(error)

        _create_error_list(errors=detail)


class PermissionDeniedAPIException(BaseAPIException):
    default_detail = {
        "code": ErrorCode.Permission_Denied.value,
        "detail": "You do not have permission to perform this action.",
    }
    status_code = status.HTTP_403_FORBIDDEN


class NotAuthenticatedAPIException(BaseAPIException):
    default_detail = {
        "code": ErrorCode.Not_Authenticated.value,
        "detail": "Authentication credentials were not provided.",
    }
    status_code = status.HTTP_401_UNAUTHORIZED
