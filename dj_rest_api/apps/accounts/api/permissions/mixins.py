from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import (
    BasePermission,
    UserCreatePermission,
    UserDeletePermission,
    UserListPermission,
    UserUpdatePermission,
)


class IsAuthenticatedMixin:
    permission_classes = [IsAuthenticated]


class BasePermissionMixin:
    permission_classes = [BasePermission, IsAuthenticated]


class UserListCreatePermissionMixin:
    permission_classes = [UserListPermission, UserCreatePermission]


class UserDetailsUpdateDestroyPermissionMixin:
    permission_classes = [UserUpdatePermission, UserDeletePermission, IsAuthenticated]


class VerifyUserAccountPermissionMixin:
    permission_classes = [AllowAny]


class VerifyOTPNumberPermissionMixin:
    permission_classes = [AllowAny]


class ForgetPasswordRequestPermissionMixin:
    permission_classes = [AllowAny]
