import enum

from django.utils.translation import gettext_lazy as _
from lib.api.exceptions import BaseAPIException
from rest_framework import status


class ErrorCode(enum.Enum):
    Not_Exists = _("not_exists")
    Not_Valid = _("not_valid")
    Failed = _("failed")


class PasswordNotValid(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Not_Valid.value,
        "detail": _("The password is not valid"),
        "data": {},
    }
    status_code = status.HTTP_400_BAD_REQUEST

    def format_response(self, errors):
        self.detail_["data"] = errors
        return super().format_response()


class UserNotCreatedAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Failed.value,
        "detail": _("The user has not been created. please try again!"),
    }

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class UserNotFoundAPIException(BaseAPIException):
    detail_ = {
        "code": ErrorCode.Not_Exists.value,
        "detail": _("The user does not exist"),
    }

    status_code = status.HTTP_404_NOT_FOUND
