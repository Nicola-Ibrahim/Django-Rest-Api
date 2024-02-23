from apps.accounts import models as accounts_models
from apps.authentication import models as auth_models
from apps.authentication import tokens
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


def login(request, email: str, password: str) -> accounts_models.User:
    """
    Logs in a user using their email and password.

    Args:
        request: HTTP request object.
        email: User's email address.
        password: User's password.

    Returns:
        User: Authenticated user.

    Raises:
        CredentialsNotValidAPIException: If the provided credentials are not valid.
    """
    user = authenticate(
        request=request,
        username=email,
        password=password,
    )

    if not user:
        raise Exception()

    return user


def logout(refresh_token: str) -> bool:
    """
    Logs out a user by blacklisting their refresh token.

    Args:
        refresh_token: User's refresh token.

    Returns:
        bool: True if logout is successful.

    """
    tokens.CustomRefreshToken(refresh_token, verify=True).blacklist()
    return True


def create_otp_number_for_user(user: accounts_models.User) -> auth_models.OTPNumber:
    """
    Creates or retrieves an OTP number for a user.

    Args:
        user: User instance for whom to create or retrieve the OTP number.

    Returns:
        auth_models.OTPNumber: Created or retrieved OTP instance.
    """
    otp_instance, created = auth_models.OTPNumber.objects.update_or_create(
        defaults={
            "number": auth_models.OTPNumber.get_number(),
            "user": user,
            "is_verified": False,
        }
    )
    return otp_instance


def verify_otp_number_for_user(user: accounts_models.User, number: str | int) -> bool:
    """
    Verifies an OTP number for a user.

    Args:
        user: User instance.
        number: OTP number to be verified.

    Returns:
        bool: True if OTP is successfully verified.

    """

    otp_instance = auth_models.OTPNumber.objects.get(user=user, number=number)

    # Set the is_verified flag to True
    otp_instance.is_verified = True
    otp_instance.save()
    return True


def delete_otp_number_for_user(user: accounts_models.User) -> bool:
    """
    Deletes the OTP number associated with a user.

    Args:
        user: User instance.

    Returns:
        bool: True if the OTP number is successfully deleted.
    """

    auth_models.OTPNumber.objects.filter(user=user).delete()
    return True


def set_new_password_for_user(user: accounts_models.User, password: str) -> bool:
    """
    Sets a new password for a user and deletes their OTP number.

    Args:
        user: User object.
        password: New password for the user.

    Returns:
        bool: True if the password is successfully updated.
    """
    # Set the new password for the user
    user.set_password(password)
    user.save()

    delete_otp_number_for_user(user=user)

    return True


def set_first_time_password_for_user(user: accounts_models.User, password: str) -> bool:
    """
    Sets the first-time password for a user and marks it as changed.

    Args:
        user: User object.
        password: Password to be set.

    Returns:
        bool: True if the password is successfully set.
    """
    user.set_password(password)

    # Set password changed to true
    if not user.is_password_changed:
        user.is_password_changed = True

    user.save()
    return True


def validate_access_token(token: str) -> bool:
    token_obj = tokens.JWTAccessToken(token, verify=True)
    user_id = token_obj["user_id"]

    if not user_id:
        return False
    return True


def get_tokens_for_user(user: accounts_models.User) -> dict:
    token = RefreshToken.for_user(user)

    return {
        "refresh": str(token),
        "access": str(token.access_token),
    }
