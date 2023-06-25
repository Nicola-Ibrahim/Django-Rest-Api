from rest_framework.permissions import IsAuthenticated

from .permissions import (
    BasePermission,
    DeleteUserPermission,
    ListCreateUserPermission,
    UpdateUserPermission,
)


class IsAuthenticatedMixin:
    permission_classes = [IsAuthenticated]


class BasePermissionMixin:
    permission_classes = [BasePermission, IsAuthenticated]


class ListCreateUserPermissionMixin:
    permission_classes = [ListCreateUserPermission]


class DeleteUserPermissionMixin:
    permission_classes = [DeleteUserPermission, IsAuthenticated]


class UpdateUserPermissionMixin:
    permission_classes = [UpdateUserPermission, IsAuthenticated]
