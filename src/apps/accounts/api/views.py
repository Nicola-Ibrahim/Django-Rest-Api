from typing import Any

from django.contrib.auth import get_user_model

# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.apps.core.base_api import views as base_views

from . import responses
from .permissions import mixins as permissions_mixins
from .serializers import factories as serializer_factory
from .serializers import serializers


class VerifyAccount(base_views.BaseGenericAPIView):
    """Verify the user by the token send it to the email"""

    permission_classes = (AllowAny,)
    serializer_class = serializers.AccountVerificationSerializer

    def get(self, request):
        serializer = self.get_serializer(request.GET.get("token"), context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return responses.ActivatedAccount()


class UserListView(
    # filters_mixins.FilterMixin,
    permissions_mixins.ListUserPermissionMixin,
    ListModelMixin,
    base_views.BaseGenericAPIView,
):

    """View for listing a new user."""

    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserListSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return responses.UserListResponse().with_data(users_data=serializer.data)


class UserCreateView(
    # FilterMixin,
    # permissions_mixins.ListUserPermissionMixin,
    ListModelMixin,
    CreateModelMixin,
    base_views.BaseGenericAPIView,
):

    """View for creating a user.
    It supports creating different user types.
    """

    def get_serializer_class(self):
        """
        Get the appropriate serializer depending on the url user_type param
        """
        serializer_class = serializer_factory.get_create_serializer(self.kwargs.get("user_type"))
        return serializer_class

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return responses.UserCreateResponse().with_data(user_data=serializer.data)


class UserDetailsUpdateDestroyView(
    # permissions_mixins.BasePermissionMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    base_views.BaseGenericAPIView,
):
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = None

        if self.request.method == "GET":
            serializer_class = serializers.UserDetailsSerializer

        elif self.request.method in ["PUT", "PATCH"]:
            user = self.get_object()
            serializer_class = serializer_factory.get_update_serializer(user_type=user.type)

        return serializer_class

    def get(self, request, *args, **kwargs) -> Response:
        user = self.get_object()
        serializer = self.get_serializer(instance=user, context={"request": request})
        return responses.UserDetailsResponse().with_data(serializer.data)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            partial=partial,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return responses.UserUpdateResponse().with_data(user_data=serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance=instance,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return responses.UserUpdateResponse().with_data(user_data=serializer.data)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        self.perform_destroy(user)
        return responses.UserDestroyResponse()


class ForgetPasswordRequestView(base_views.BaseGenericAPIView):
    """View for sending an OTP number to the user's email for changing the password"""

    serializer_class = serializers.ForgetPasswordRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        # Validate user's email and check existence
        serializer.is_valid(raise_exception=True)

        # Create OTP number for the user
        serializer.save()

        return responses.ForgetPasswordRequestResponse()


class VerifyOTPNumberView(base_views.BaseGenericAPIView):
    """View for verifying the generated OTP number for the user who wants to change password."""

    serializer_class = serializers.VerifyOTPNumberSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Add access token to the response
        user = get_user_model().objects.get(email=request.data.get("email"))

        return responses.VerifyOTPResponse().with_data(access_token=user.get_tokens()["access"])


class BaseResetPasswordView(base_views.BaseGenericAPIView):
    """
    Abstract base view for setting new password
    This model implements patch method, so the
    concrete ResetPassword class only have to set serializer_class attribute.
    """

    class Meta:
        abstract = True

    def patch(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return responses.ResetPasswordResponse()


class ForgetPasswordView(BaseResetPasswordView):
    """View for resetting the forgotten password"""

    serializer_class = serializers.ForgetPasswordSerializer


class ChangePasswordView(BaseResetPasswordView):
    """View for changing password"""

    serializer_class = serializers.ChangePasswordSerializer


class FirstTimePasswordView(BaseResetPasswordView):
    """View for setting the first time password"""

    serializer_class = serializers.FirstTimePasswordSerializer
