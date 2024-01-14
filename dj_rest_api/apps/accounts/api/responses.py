from typing import Any

from django.utils.translation import gettext_lazy as _
from lib.api.responses import BaseAPIResponse, OperationCode
from rest_framework import status as rest_status


class UserListResponse(BaseAPIResponse):
    def __init__(
        self,
        data=None,
        status=rest_status.HTTP_200_OK,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        formatted_data = self.format_data(data)

        super().__init__(formatted_data, status, template_name, headers, exception, content_type)

    def format_data(self, data: Any) -> dict:
        if data:
            return {
                "code": OperationCode.Listing.value,
                "detail": _(f"{len(data)} users have been found"),
                "data": data,
            }
        return {}


class UserCreatedAPIResponse(BaseAPIResponse):
    def __init__(
        self,
        data=None,
        status=rest_status.HTTP_201_CREATED,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        formatted_data = self.format_data(data)

        super().__init__(formatted_data, status, template_name, headers, exception, content_type)

    def format_data(self, data: Any):
        if data:
            return {
                "code": OperationCode.Created.value,
                "detail": _("The user has been created"),
            }

        return {}


class UserUpdateAPIResponse(BaseAPIResponse):
    def __init__(
        self,
        data=None,
        status=rest_status.HTTP_200_OK,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        formatted_data = self.format_data(data)

        super().__init__(formatted_data, status, template_name, headers, exception, content_type)

    def format_data(self, data: Any):
        if data:
            return {
                "code": OperationCode.Created.value,
                "detail": _("The user has been updated"),
            }

        return {}


class UserDetailsAPIResponse(BaseAPIResponse):
    def __init__(
        self,
        data=None,
        status=rest_status.HTTP_200_OK,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        formatted_data = self.format_data(data)

        super().__init__(formatted_data, status, template_name, headers, exception, content_type)

    def format_data(self, data: Any):
        if data:
            return {
                "code": OperationCode.Detail.value,
                "detail": _("The info of {user_data['first_name']"),
                "data": data,
            }

        return {}


class UserDestroyAPIResponse(BaseAPIResponse):
    def __init__(
        self,
        data=None,
        status=rest_status.HTTP_204_NO_CONTENT,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        formatted_data = self.format_data(data)

        super().__init__(formatted_data, status, template_name, headers, exception, content_type)

    def format_data(self, data: Any):
        if data:
            return {
                "code": OperationCode.Deleted.value,
                "detail": _("The user has been deleted"),
            }

        return {}
