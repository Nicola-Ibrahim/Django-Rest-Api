import enum

from apps.core.base_api.responses import BaseResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class OperationCode(enum.Enum):
    Listing = _("listing")
    Created = _("created")
    Detail = _("detail")
    Updated = _("updated")
    Deleted = _("deleted")


class UserListResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Listing.value,
        "detail": _("No users found"),
        "data": [],
    }

    status_ = status.HTTP_200_OK

    def with_data(self, users_data: list):
        if users_data:
            self.data_["detail"] = _(f"{len(users_data)} users have been found")
            self.data_["data"] = users_data

        return super().with_data()


class UserCreateResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Created.value,
        "detail": _("The user has been created"),
    }

    status_ = status.HTTP_201_CREATED

    def with_data(self, user_data: dict):
        if user_data:
            self.data_["data"] = user_data

        return super().with_data()


class UserUpdateResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Created.value,
        "detail": _("The user has been updated"),
    }

    status_ = status.HTTP_200_OK

    def with_data(self, user_data: dict):
        if user_data:
            self.data_["data"] = user_data

        return super().with_data()


class UserDetailsResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Detail.value,
        "detail": _("No users found"),
        "data": {},
    }

    status_ = status.HTTP_200_OK

    def with_data(self, user_data: dict):
        if user_data:
            self.data_["detail"] = f"The info of {user_data['first_name']}"
            self.data_["data"] = user_data

        return super().with_data()


class UserDestroyResponse(BaseResponse):
    data_ = {
        "code": OperationCode.Deleted.value,
        "detail": _("The user has been deleted"),
    }

    status_ = status.HTTP_204_NO_CONTENT
