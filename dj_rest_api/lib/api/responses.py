import enum

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
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        status = status or rest_status.HTTP_200_OK

        super().__init__(data, status, template_name, headers, exception, content_type)

    def format_data(self, **kwargs) -> None:
        """Update the data in The Response"""


class LanguagesListResponse(BaseAPIResponse):
    data_ = {
        "code": OperationCode.Listing.value,
        "detail": _("retrieving the list of supported languages"),
        "data": {},
    }
    status_ = rest_status.HTTP_200_OK

    def __init__(
        self,
        languages: list,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        self.format_data(languages=languages)
        super().__init__(data, status, template_name, headers, exception, content_type)

    def format_data(self, languages: list) -> None:
        self.data_["data"]["languages"] = [{"code": code, "name": _(name)} for code, name in languages]
