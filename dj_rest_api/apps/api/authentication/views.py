from apps.api.base.permissions import BasePermission
from apps.api.base.views import BaseGenericAPIView
from apps.authentication import services
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import responses, serializers


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
            LoginAPIResponse: A response containing user details upon successful login.
        """

        # Validate the email and password
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # Login with the passed credentials
        email, password = serializer.data.get("email"), serializer.data.get("password")

        user = services.login(request=request, email=email, password=password)

        return responses.LoginAPIResponse(data=user.get_user_details())


class LogoutView(BaseGenericAPIView):
    """
    View for processing user logout requests.

    Methods:
        post(request): Handles POST requests for user logout.
        Validates the request data, performs user logout, and returns the logout response.

    Example:
        To log out a user, send a POST request.
    """

    permission_classes = [BasePermission, IsAuthenticated]
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

        # Validate token
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Logout user
        services.logout(refresh_token=serializer.data.get("refresh_token"))

        return responses.LogoutResponse()


class ForgetPasswordRequestView(BaseGenericAPIView):
    """
    View for sending an OTP number to the user's email for changing the password.

    Methods:
        post(request): Handles POST requests for sending an OTP number to the user's email.
        Validates the user's email, checks existence, creates an OTP number, and returns the response.

    Example:
        To request a password reset, send a POST request with the user's email.
    """

    permission_classes = [AllowAny]
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

        user = get_user_by_email(email)

        # Create OTP number for the user
        services.create_otp_number_for_user(user)

        return responses.ForgetPasswordRequestAPIResponse()


class VerifyOTPNumberView(BaseGenericAPIView):
    """
    View for verifying the generated OTP number for the user who wants to change password.

    Methods:
        post(request, *args, **kwargs): Handles POST requests for verifying the OTP number.
        Validates the OTP number, updates verification status, and returns the response.

    Example:
        To verify the OTP number, send a POST request with the user's email and OTP number.
    """

    permission_classes = [AllowAny]
    serializer_class = serializers.VerifyOTPNumberSerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests for verifying the generated OTP number.

        Validates the OTP number, updates verification status, and returns the response.

        Returns:
            Response: The OTP verification response with an access token.
        """

        # Validate user and otp number
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user
        user = get_user_by_email(email)

        # Add access token to the response
        verified, user = services.verify_otp_number_for_user(
            email=serializer.data.get("email"), number=serializer.data.get("opt_number")
        )

        return responses.VerifyOTPAPIResponse(data=user.get_tokens()["access"])


class ForgetPasswordView(BaseGenericAPIView):
    """
    View for processing forget password requests and setting a new password.

    Methods:
        patch(request): Handles PATCH requests for setting a new password after forget password request.
        Validates the request data, performs the password reset, and returns the response.

    Example:
        To set a new password after forget password request, send a PATCH request with the required data.
    """

    serializer_class = serializers.ForgetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        # Validate passed password
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # Set first time password
        services.set_new_password_for_user(user=request.User, password=serializer.data.get("new_password"))

        return responses.ResetPasswordAPIResponse()


class ChangePasswordView(BaseGenericAPIView):
    """
    View for processing change password requests and setting a new password.

    Methods:
        patch(request): Handles PATCH requests for setting a new password after change password request.
        Validates the request data, performs the password reset, and returns the response.

    Example:
        To set a new password after change password request, send a PATCH request with the required data.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ChangePasswordSerializer

    def patch(self, request, *args, **kwargs):
        # Validate passed password
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # Set first time password
        services.set_new_password_for_user(user=request.User, password=serializer.data.get("new_password"))

        return responses.ResetPasswordAPIResponse()


class FirstTimePasswordView(BaseGenericAPIView):
    """
    View for processing first time password requests and setting a new password.

    Methods:
        patch(request): Handles PATCH requests for setting a new password as a first-time password.
        Validates the request data, performs the password reset, and returns the response.

    Example:
        To set a new password as a first-time password, send a PATCH request with the required data.
    """

    serializer_class = serializers.FirstTimePasswordSerializer

    def patch(self, request):
        """
        Handles PATCH requests for setting a new password.

        Validates the request data, performs the password reset, and returns the response.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The password reset response.
        """
        # Validate passed password
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        # Set first time password
        services.set_first_time_password_for_user(user=request.User, password=serializer.data.get("password"))

        return responses.ResetPasswordAPIResponse()
