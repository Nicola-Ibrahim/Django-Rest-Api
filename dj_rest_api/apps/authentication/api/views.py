from apps.accounts.api.permissions.mixins import BasePermissionMixin
from apps.core.base_api.views import BaseAPIView, BaseGenericAPIView
from django.contrib.auth import get_user_model

from . import exceptions, permissions, responses, serializers


class LoginView(BaseGenericAPIView):
    """
    View for processing user login requests.

    Attributes:
        serializer_class (class): The serializer class for validating and processing the request data.

    Methods:
        post(request): Handles POST requests for user login.
        Validates the request data, performs user authentication, and returns the login response.

    Example:
        To log in a user, send a POST request with the required login credentials.
    """

    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            LoginResponse: A response containing user details upon successful login.
        """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get("user")

        return responses.LoginResponse().with_data(user_details=user.get_user_details())


class LogoutView(BasePermissionMixin, BaseGenericAPIView):
    """
    View for processing user logout requests.

    Attributes:
        serializer_class (class): The serializer class for validating and processing the request data.

    Methods:
        post(request): Handles POST requests for user logout.
        Validates the request data, performs user logout, and returns the logout response.

    Example:
        To log out a user, send a POST request.
    """

    serializer_class = serializers.LogoutSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user logout.

        Args:
            request (HttpRequest): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            LogoutResponse: A response indicating successful user logout.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return responses.LogoutResponse()


class ForgetPasswordRequestView(
    permissions.ForgetPasswordRequestPermissionMixin,
    BaseGenericAPIView,
):
    """
    View for sending an OTP number to the user's email for changing the password.

    Attributes:
        serializer_class: The serializer class for validating and processing the request data.
        permission_classes: The permission classes for allowing access to the view.

    Methods:
        post(request): Handles POST requests for sending an OTP number to the user's email.
        Validates the user's email, checks existence, creates an OTP number, and returns the response.

    Example:
        To request a password reset, send a POST request with the user's email.
    """

    serializer_class = serializers.ForgetPasswordRequestSerializer

    def post(self, request):
        """
        Handles POST requests for sending an OTP number to the user's email.

        Validates the user's email, checks existence, creates an OTP number, and returns the response.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The password reset request response.
        """
        serializer = self.get_serializer(data=request.data)

        # Validate user's email and check existence
        serializer.is_valid(raise_exception=True)

        # Create OTP number for the user
        serializer.save()

        return responses.ForgetPasswordRequestResponse()


class VerifyOTPNumberView(
    permissions.VerifyOTPNumberPermissionMixin,
    BaseGenericAPIView,
):
    """
    View for verifying the generated OTP number for the user who wants to change password.

    Attributes:
        serializer_class: The serializer class for validating and processing the request data.
        permission_classes: The permission classes for allowing access to the view.

    Methods:
        post(request, *args, **kwargs): Handles POST requests for verifying the OTP number.
        Validates the OTP number, updates verification status, and returns the response.

    Example:
        To verify the OTP number, send a POST request with the user's email and OTP number.
    """

    serializer_class = serializers.VerifyOTPNumberSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for verifying the generated OTP number.

        Validates the OTP number, updates verification status, and returns the response.

        Args:
            request: The HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The OTP verification response with an access token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Add access token to the response
        user = get_user_model().objects.get(email=request.data.get("email"))

        return responses.VerifyOTPResponse().with_data(access_token=user.get_tokens()["access"])


class BaseResetPasswordView(BaseGenericAPIView):
    """
    Abstract base view for setting a new password.
    This view implements the patch method, so the concrete ResetPassword class
    only has to set the serializer_class attribute.

    Attributes:
        Meta: The metadata class indicating that this is an abstract view.

    Methods:
        patch(request): Handles PATCH requests for setting a new password.
        Validates the request data, performs the password reset, and returns the response.

    Example:
        To set a new password, send a PATCH request with the required data.
    """

    class Meta:
        abstract = True

    def patch(self, request):
        """
        Handles PATCH requests for setting a new password.

        Validates the request data, performs the password reset, and returns the response.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The password reset response.
        """
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return responses.ResetPasswordResponse()


class ForgetPasswordView(BaseResetPasswordView):
    """
    View for processing forget password requests and setting a new password.

    Attributes:
        serializer_class: The serializer class for validating and processing the request data.

    Methods:
        patch(request): Handles PATCH requests for setting a new password after forget password request.
        Validates the request data, performs the password reset, and returns the response.

    Example:
        To set a new password after forget password request, send a PATCH request with the required data.
    """

    serializer_class = serializers.ForgetPasswordSerializer


class ChangePasswordView(BaseResetPasswordView):
    """
    View for processing change password requests and setting a new password.

    Attributes:
        serializer_class: The serializer class for validating and processing the request data.

    Methods:
        patch(request): Handles PATCH requests for setting a new password after change password request.
        Validates the request data, performs the password reset, and returns the response.

    Example:
        To set a new password after change password request, send a PATCH request with the required data.
    """

    serializer_class = serializers.ChangePasswordSerializer


class FirstTimePasswordView(BaseResetPasswordView):
    """
    View for processing first time password requests and setting a new password.

    Attributes:
        serializer_class: The serializer class for validating and processing the request data.

    Methods:
        patch(request): Handles PATCH requests for setting a new password as a first-time password.
        Validates the request data, performs the password reset, and returns the response.

    Example:
        To set a new password as a first-time password, send a PATCH request with the required data.
    """

    serializer_class = serializers.FirstTimePasswordSerializer


class CheckJWTTokenView(BasePermissionMixin, BaseAPIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_password_changed:
            raise exceptions.FirstTimePasswordError().with_data(token=self.request.user.get_tokens()["access"])

        return responses.CheckJWTTokenResponse(user=request.user)
