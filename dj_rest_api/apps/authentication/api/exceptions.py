"""
This script defines custom formatted exceptions for handling errors in the system.
"""

import enum

from django.utils.translation import gettext_lazy as _
from lib.api.exceptions import BaseException
from rest_framework import status


class ErrorCode(enum.Enum):
    Credential_Error = _("credential_error")


class CredentialsNotValid(BaseException):
    detail_ = {
        "code": ErrorCode.Credential_Error.value,
        "detail": _("Unable to log in with provided credentials."),
    }
    status_code = status.HTTP_401_UNAUTHORIZED
