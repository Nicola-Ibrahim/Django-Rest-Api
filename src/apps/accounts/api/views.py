from django.contrib.auth import get_user_model
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.apps.core import mailers
from src.apps.core.base_api import views as base_views

from . import responses
from .filters.mixins import FilterMixin
from .permissions import mixins as permissions_mixin
from .queryset.mixins import InUserTypeQuerySetMixin, QueryParamUserTypeQuerySetMixin
from .serializers import factories as serializer_factory
from .serializers import serializers
from .serializers.mixins import (
    InUserTypeSerializerMixin,
    QueryParamUserTypeSerializerMixin,
)


class VerifyAccount(base_views.BaseGenericAPIView):
    """Verify the user by the token send it to the email"""

    permission_classes = (AllowAny,)
    serializer_class = serializers.AccountVerificationSerializer

    def get(self, request):
        serializer = self.get_serializer(
            request.GET.get("token"), context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return responses.ActivatedAccount()


class UserListView(
    # FilterMixin,
    # permissions_mixin.ListCreateUserPermissionMixin,
    ListModelMixin,
    base_views.BaseGenericAPIView,
):

    """View for listing a new user."""

    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserCreateView(
    QueryParamUserTypeQuerySetMixin,
    # FilterMixin,
    # permissions_mixin.ListCreateUserPermissionMixin,
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
        serializer_class = serializer_factory.get_serializer(
            self.kwargs.get("user_type")
        )
        return serializer_class

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # TODO: pass the type of created user to the serializer to put the user type attribute
        # Create the user
        user = serializer.save()

        # Send welcome email
        # mailers.RegisterMailer(
        #     to_email=user.email, password=password
        # ).send_email()
        mailers.VerificationMailer(
            token=user.tokens()["access"], to_emails=[user.email], request=request
        )
        return responses.UserCreateResponse()


class UserDetailsUpdateDestroyView(
    # permissions_mixin.BasePermissionMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    base_views.BaseGenericAPIView,
):
    queryset = get_user_model().objects.all()
    lookup_field = "id"

    def get_serializer_class(self, *args, **kwargs):
        serializer_class = serializer_factory.get_serializer(
            user_type=self.request.user.type
        )
        return serializer_class

    def get(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return responses.UserUpdateResponse()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return responses.UserDestroyResponse()


class ForgetPasswordRequestView(base_views.BaseGenericAPIView):
    """View for sending an OTP number to the user's email for changing the password"""

    serializer_class = serializers.ForgetPasswordRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        # Validate user's email and check existence
        serializer.is_valid(raise_exception=True)

        # Create OTP number for the user
        serializer.save()

        # Send reset password message with OTP to user's email
        mailers.OTPMailer(
            to_email=serializer.validated_data.get("email"),
            otp_number=serializer.validated_data.get("otp"),
        ).send_email()

        user = serializer.validated_data.get("user")
        return responses.ForgetPasswordRequestResponse(user=user)


class VerifyOTPNumberView(base_views.BaseGenericAPIView):
    """View for verifying the generated OTP number for the user who wants to change password."""

    serializer_class = serializers.VerifyOTPNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return responses.VerifyOTPResponse()


class BaseResetPasswordView(base_views.BaseGenericAPIView):
    """
    Abstract base view for setting new password
    This model implements patch method, so the
    concrete ResetPassword class only have to set serializer_class attribute.
    """

    class Meta:
        abstract = True

    def patch(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
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
