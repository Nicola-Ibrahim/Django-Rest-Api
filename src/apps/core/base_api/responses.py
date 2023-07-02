import enum

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response


class OperationCode(enum.Enum):
    date_time = _("date_time")
    Listing = _("listing")


class BaseResponse(Response):
    data_ = None
    status_ = status.HTTP_200_OK

    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):
        if not data and self.data_:
            data = self.data_

        if not status and self.status_:
            status = self.status_

        super().__init__(data, status, template_name, headers, exception, content_type)

    def with_data(self, **kwargs):
        """Update the data dictionary in The Response"""
        return self


class LanguagesListResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Listing.value,
        "detail": _("retrieving the list of supported languages"),
        "data": {},
    }
    status_ = status.HTTP_200_OK

    def with_data(self, languages: list):
        self.data_["data"]["languages"] = [{"code": code, "name": _(name)} for code, name in languages]

        return super().with_data()
