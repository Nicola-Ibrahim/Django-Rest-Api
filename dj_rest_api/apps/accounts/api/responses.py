from typing import Any

from django.utils.translation import gettext_lazy as _
from lib.api.responses import BaseAPIResponse, OperationCode
from rest_framework import status as rest_status


class UserListResponse(BaseAPIResponse):
    default_status = rest_status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": OperationCode.Listing.value,
                "detail": _(f"{len(data)} users have been found"),
                "data": data,
            }
        return super().format_response()


class UserCreatedAPIResponse(BaseAPIResponse):
    default_status = rest_status.HTTP_201_CREATED

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": OperationCode.Created.value,
                "detail": _("The user has been created"),
            }

        return super().format_response()


class UserUpdateAPIResponse(BaseAPIResponse):
    default_status = rest_status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": OperationCode.Created.value,
                "detail": _("The user has been updated"),
            }

        return super().format_response()


class UserDetailsAPIResponse(BaseAPIResponse):
    default_status = rest_status.HTTP_200_OK

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": OperationCode.Detail.value,
                "detail": _("The info of {user_data['first_name']"),
                "data": data,
            }

        return super().format_response()


class UserDestroyAPIResponse(BaseAPIResponse):
    default_status = rest_status.HTTP_204_NO_CONTENT

    def format_response(self, data: Any) -> dict | list:
        if data:
            return {
                "code": OperationCode.Deleted.value,
                "detail": _("The user has been deleted"),
            }

        return super().format_response()
