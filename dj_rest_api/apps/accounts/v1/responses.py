import enum
from typing import T

from core.api.responses import BaseAPIResponse
from core.api.responses import OperationCode as BaseOperationCode
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class OperationCode(enum.Enum):
    Activated_Account = _("activated_account")


class UserListAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_data(self, data: dict | None = None) -> T:
        if data:
            return {
                "code": BaseOperationCode.Listing.value,
                "detail": _(f"{len(data)} users have been found"),
                "data": data,
            }

        return super().format_data(data)


class UserCreatedAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_201_CREATED

    def format_data(self, data: dict | None = None) -> T:
        return {
            "code": BaseOperationCode.Created.value,
            "detail": _("The user has been created"),
        }


class UserUpdateAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_data(self, data: dict | None = None) -> T:
        return {
            "code": BaseOperationCode.Created.value,
            "detail": _("The user has been updated"),
        }


class UserDetailsAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_data(self, data: dict | None = None) -> T:
        return {
            "code": BaseOperationCode.Detail.value,
            "detail": _("The info of {user_data['first_name']"),
            "data": data,
        }


class UserDestroyAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_204_NO_CONTENT

    def format_data(self, data: dict | None = None) -> T:
        return {
            "code": BaseOperationCode.Deleted.value,
            "detail": _("The user has been deleted"),
        }


class ActivatedAccountAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_data(self, data: dict | None = None) -> T:
        return {
            "code": OperationCode.Activated_Account.value,
            "detail": _("The account has been activated successfully."),
        }
