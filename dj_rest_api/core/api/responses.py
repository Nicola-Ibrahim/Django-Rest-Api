import enum
from typing import Any, T

from django.utils.translation import gettext_lazy as _
from rest_framework import status as rest_status
from rest_framework.response import Response


class OperationCode(enum.Enum):
    date_time = _("date_time")
    Listing = _("listing")
    Created = _("created")
    Detail = _("detail")
    Updated = _("updated")
    Deleted = _("deleted")


class BaseAPIResponse(Response):
    default_status = rest_status.HTTP_200_OK

    def __init__(
        self,
        data: Any = None,
        status: int = None,
        template_name: str = None,
        headers: dict = None,
        exception: bool = False,
        content_type: str = None,
    ):
        status = status or self.default_status

        data = self.format_data(data)

        super().__init__(data, status, template_name, headers, exception, content_type)

    def format_data(self, data: dict | None = None) -> T:
        """Update the data in The Response"""
        return data
