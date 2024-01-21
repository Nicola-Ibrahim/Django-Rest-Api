import enum
from typing import Any

from apps.api.base.responses import BaseAPIResponse
from apps.api.base.responses import OperationCode as BaseOperationCode
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class OperationCode(enum.Enum):
    Activated_Account = _("activated_account")


class UserListAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": BaseOperationCode.Listing.value,
                "detail": _(f"{len(data)} users have been found"),
                "data": data,
            }
        return super().format_response()


class UserCreatedAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_201_CREATED

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": BaseOperationCode.Created.value,
                "detail": _("The user has been created"),
            }

        return super().format_response()


class UserUpdateAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": BaseOperationCode.Created.value,
                "detail": _("The user has been updated"),
            }

        return super().format_response()


class UserDetailsAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": BaseOperationCode.Detail.value,
                "detail": _("The info of {user_data['first_name']"),
                "data": data,
            }

        return super().format_response()


class UserDestroyAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_204_NO_CONTENT

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": BaseOperationCode.Deleted.value,
                "detail": _("The user has been deleted"),
            }

        return super().format_response()


class ActivatedAccountAPIResponse(BaseAPIResponse):
    default_status = status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": OperationCode.Activated_Account.value,
                "detail": _("The account has been activated successfully."),
            }

        return super().format_response()
