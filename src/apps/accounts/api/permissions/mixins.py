from rest_framework.permissions import IsAuthenticated

from .permissions import (
    BasePermission,
    DeleteUserPermission,
    ListUserPermission,
    UpdateUserPermission,
)


class IsAuthenticatedMixin:
    permission_classes = [IsAuthenticated]


class BasePermissionMixin:
    permission_classes = [BasePermission, IsAuthenticated]


class ListUserPermissionMixin:
    permission_classes = [ListUserPermission]


class DeleteUserPermissionMixin:
    permission_classes = [DeleteUserPermission, IsAuthenticated]


class UpdateUserPermissionMixin:
    permission_classes = [UpdateUserPermission, IsAuthenticated]
