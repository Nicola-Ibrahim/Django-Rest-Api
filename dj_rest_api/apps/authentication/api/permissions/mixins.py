from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import BasePermission


class IsAuthenticatedMixin:
    permission_classes = [IsAuthenticated]


class BasePermissionMixin:
    permission_classes = [BasePermission, IsAuthenticated]


class VerifyOTPNumberPermissionMixin:
    permission_classes = [AllowAny]


class ForgetPasswordRequestPermissionMixin:
    permission_classes = [AllowAny]
