import enum
import logging

from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


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

    def update_data(self, **kwargs):
        """Update the data dictionary in The Response"""
        pass
