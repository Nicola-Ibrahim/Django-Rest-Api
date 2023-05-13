from rest_framework.permissions import IsAuthenticated

from .mixins import BasePermission, DeleteUserPermission, UpdateUserPermission


class PermissionMixin:
    permission_classes = [BasePermission, IsAuthenticated]


class DeleteUserPermissionMixin:
    permission_classes = [DeleteUserPermission, IsAuthenticated]


class UpdateUserPermissionMixin:
    permission_classes = [UpdateUserPermission, IsAuthenticated]
