import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import mailers
from ..models.models import OTPNumber
from . import exceptions, responses
from .permissions.mixins import IsAuthenticatedMixin, PermissionMixin
from .queryset.mixins import InUserTypeQuerySetMixin, KwargUserTypeQuerySetMixin
from .serializers.mixins import (
    InUserTypeSerializerMixin,
    KwargUserTypeSerializerMixin,
)


class VerifyEmail(APIView):
    """Verify the user by the token send it to the email"""

    permission_classes = (AllowAny,)

    def get(self, request) -> Response:
        """Override get method to verify the new registered user via email

        Args:
            request: the incoming request

        Raises:
            jwt.ExpiredSignatureError | jwt.exceptions.DecodeError: jwt exceptions

        Returns:
            Response | Exception: rest framework response with verified message or exception
        """

        token = request.GET.get("token")
        try:
            # Decode the token coming with the request
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"], type=jwt
            )

            # Get the use id from the payload
            user = get_user_model().objects.get(id=payload["user_id"])

            # Check if the user is not verified
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation Expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserSignView(KwargUserTypeSerializerMixin, generics.CreateAPIView):
    """View for adding a new user"""

    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs) -> Response:
        """Override post method to control the behavior of inserting a new user

        Returns:
            Response: rest framework response with user data
        """
        user_data = request.data
        serializer = self.get_serializer(
            data=user_data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        # Send verification message to user's email
        mailers.VerificationMailer()

        return Response(user_data, status=status.HTTP_201_CREATED)


class UserDetailsView(
    InUserTypeQuerySetMixin,
    InUserTypeSerializerMixin,
    PermissionMixin,
    generics.RetrieveAPIView,
):
    """
    Class based view to Get User Details using Token Authentication
    """

    def get(self, request, *args, **kwargs) -> Response:
        """Override get method to obtain details depending on login user type

        Args:
            request: incoming request

        Returns:
            Response: rest framework response with user data
        """

        serializer = self.get_serializer(
            request.user, context={"request": request}
        )
        return Response(serializer.data)


class UserUpdateView(
    InUserTypeQuerySetMixin,
    # InUserTypeSerializerMixin,
    PermissionMixin,
    generics.UpdateAPIView,
):
    serializer_class = UserSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserDeleteView(
    InUserTypeQuerySetMixin,
    InUserTypeSerializerMixin,
    DeleteUserPermissionMixin,
    generics.DestroyAPIView,
):
    def get_object(self):
        """
        Returns the object the view is displaying.
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.user.id}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def destroy(self, request, *args, **kwargs):
        """Override destroy method to handle deleting for multiple users

        Args:
            request: incoming request
        """

        # Get the users to be deleted
        ids = request.data["ids"]

        # Get the user who perform the delete action
        _ = self.get_object()

        # Execute delete the ids
        users_deleted = self.perform_destroy(ids)

        msg = {"details": f"Deleted the users: {users_deleted}"}
        return Response(data=msg, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, ids):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"pk__in": ids}
        users_deleted = queryset.filter(**filter_kwargs).delete()
        return users_deleted


class UsersListView(
    KwargUserTypeQuerySetMixin,
    KwargUserTypeSerializerMixin,
    FilterMixin,
    PermissionMixin,
    generics.ListAPIView,
):
    pass


class LoginView(APIView):
    """View for user logging"""

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        if email and password:
            # Check if the user is inactive
            user = get_user_model().objects.filter(email=email)
            if not user.exists():
                raise exceptions.UserNotExistsError()

            user = user.first()
            if not user.is_active:
                raise exceptions.UserNotActiveResponse()

            # Authenticate the user
            user = authenticate(
                request=request,
                username=email,
                password=password,
            )

            if not user:
                raise exceptions.CredentialsError()

            if not user.is_password_changed:
                otp_number = OTPNumber.get_number()
                user.otp_number.update_or_create(defaults={"number": otp_number})
                mailers.OTPMailer(
                    to_email=user.email, otp_number=otp_number
                ).send_email()

                return responses.FirstTimePasswordError(user=user)

            return responses.LoginResponse(user=user)


class LogoutView(IsAuthenticatedMixin, generics.GenericAPIView):
    """View for user logout"""

    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return responses.LogoutResponse()


class UserListCreateView(GrantedAdminPermissionMixin, generics.ListCreateAPIView):
    """View for adding a new user"""

    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer

        return UserListSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Override post method to control the behavior of inserting a new user
        Returns:
            Response: rest framework response with user data
        """
        user_data = request.data
        serializer = self.get_serializer(
            data=user_data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create random password for user
        password = get_user_model().objects.make_random_password()
        user.set_password(password)
        user.save(update_fields=["password"])

        # Send welcome email
        # mailers.RegisterMailer(
        #     to_email=user.email, password=password
        # ).send_email()
        mailers.VerificationMailer(
            token=user.tokens()["access"], to_emails=[user.email], request=request
        )
        return responses.UserCreateResponse()


class UserDetailsUpdateDestroyView(
    permissions.IsOwnerOrAdminPermissionMixin,
    generics.RetrieveUpdateDestroyAPIView,
):
    queryset = get_user_model().objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            if self.request.user.is_granted_group:
                return UserAdminUpdateSerializer
            else:
                return UserNotAdminUpdateSerializer

        return UserDetailSerializer

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = queryset.filter(**filter_kwargs)
        if not obj.exists():
            raise exceptions.UserNotExistsException()

        obj = obj.first()

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return responses.UserUpdateResponse()

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return responses.UserDestroyResponse()


class ForgetPasswordRequestView(generics.GenericAPIView):
    """View for sending a number to the user's email for resetting password"""

    serializer_class = ForgetPasswordRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Send reset password message to user's email
        mailers.OTPMailer(
            to_email=serializer.validated_data.get("email"),
            otp_number=serializer.validated_data.get("otp"),
        ).send_email()

        user = serializer.validated_data.get("user")
        return responses.ForgetPasswordRequestResponse(user=user)


class VerifyOTPNumberView(generics.GenericAPIView):
    """View for checking the generated opt token for the user who wants to reset password."""

    serializer_class = VerifyOTPNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return responses.VerifyOTPResponse()


class ResetPasswordView(generics.GenericAPIView):
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


class ChangePasswordView(ResetPasswordView):
    """View for changing the forgotten password"""

    serializer_class = ChangePasswordSerializer


class FirstTimePasswordView(ResetPasswordView):
    """View for changing the forgotten password"""

    serializer_class = FirstTimePasswordSerializer
