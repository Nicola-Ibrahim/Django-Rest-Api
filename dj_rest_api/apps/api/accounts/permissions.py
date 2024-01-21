import enum

from apps.accounts.models import User
from apps.api.base.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class PermissionGroupsName(enum.Enum):
    TEACHER_GROUP = "warehouses_group"
    STUDENT_GROUP = "doctors_group"


class UserListPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET" and request.user and request.user.is_authenticated:
            return True

        return False


class UserCreatePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return False


class UserDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Override the has_object_permission for adding more constraints on users

        Args:
            request (_type_): _description_
            view (_type_): _description_
            obj (_type_): _description_

        Raises:
            Response: HTTP_403_FORBIDDEN
            Response: HTTP_403_FORBIDDEN
            DeleteMultipleUsers: Delete multiple user exception

        Returns:
            _type_: _description_
        """

        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user
        ids = request.data["ids"]

        if request.method not in ["DELETE"]:
            return None

        # Get the user's permission related to the Http method
        perms = self.get_required_object_permissions(request.method, model_cls)

        if not user.has_perms(perms):
            # If the user does not have permissions we need to determine if
            # they have read permissions to see 403, or not, and simply see
            # a 404 response.

            if request.method in SAFE_METHODS:
                # Read permissions already checked and failed, no need
                # to make another lookup.
                raise Response(status=HTTP_403_FORBIDDEN)

            read_perms = self.get_required_object_permissions("GET", model_cls)
            if not user.has_perms(read_perms, obj):
                raise Response(status=HTTP_403_FORBIDDEN)

            return False

        elif user.type != User.Type.ADMIN:
            # Prevent the non admin user from multiple deleting
            if len(ids) > 1:
                raise DeleteMultipleUsers()

            elif user.id == ids[0]:
                return True

            return False

        return True


class UserUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Override the has_object_permission for adding more constraints on users

        Args:
            request (_type_): _description_
            view (_type_): _description_
            obj (_type_): _description_

        Raises:
            Response: HTTP_403_FORBIDDEN
            Response: HTTP_403_FORBIDDEN
            DeleteMultipleUsers: Delete multiple user exception

        Returns:
            _type_: _description_
        """

        queryset = self._queryset(view)
        model_cls = queryset.model
        user = request.user
        data = request.data

        if request.method not in ["PUT", "PATCH"]:
            return None

        # Get the user's permission related to the Http method
        perms = self.get_required_object_permissions(request.method, model_cls)  # noqa: F841

        if user.type != User.Type.ADMIN:
            # Prevent the non admin user from multiple deleting
            if len(data) > 1:
                raise UpdateMultipleUsers()

            elif user.email == data["email"]:
                return True

            return False

        return True
