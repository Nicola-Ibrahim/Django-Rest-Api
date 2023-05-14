from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details


class BaseExceptions(APIException):
    """
    Base class for exceptions.
    Subclasses should provide `.detail_` and `.status_code` properties.
    """

    detail_ = None

    status_code = status.HTTP_200_OK

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code

        if detail is None:
            detail = self.detail_

        if code is None:
            code = self.status_code

        # For  failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if isinstance(detail, tuple):
            detail = list(detail)
        elif not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)

    def update_data(self, **kwargs):
        """Update the data dictionary in The Response"""
        pass
