from apps.accounts.models import User
from apps.accounts.services import get_user_by_email, get_user_by_id
from apps.authentication.api import tokens
from django.contrib.auth import authenticate

from . import models
from .api import exceptions


def login(request, email: str, password: str) -> User:
    user = authenticate(
        request=request,
        username=email,
        password=password,
    )

    if not user:
        raise exceptions.CredentialsNotValidAPIException()

    return user


def logout(refresh_token: str) -> bool:
    tokens.CustomRefreshToken(refresh_token, verify=True).blacklist()
    return True


def create_otp_number_for_user(email: str):
    user = get_user_by_email(email)

    otp_instance, created = models.OTPNumber.objects.update_or_create(
        defaults={
            "number": models.OTPNumber.get_number(),
            "user": user,
            "is_verified": False,
        }
    )
    return otp_instance


def verify_otp_number_for_user(email: str, number: str | int) -> bool | User:
    user = get_user_by_email(email)
    otp_instance = models.OTPNumber.objects.get(user=user, number=number)

    # Set the is_verified flag to True
    otp_instance.is_verified = True
    otp_instance.save()
    return True, User


def delete_otp_number_for_user(user_id: int | str) -> bool:
    user = get_user_by_id(user_id)

    # Delete otp number for the user
    models.OTPNumber.objects.filter(user=user).delete()
    return True


def set_new_password_for_user(user: User, password: str) -> bool:
    # Set the new password for the user
    user.set_password(password)
    user.save()

    delete_otp_number_for_user(user_id=user.id)

    return True


def set_first_time_password_for_user(user: User, password: str) -> bool:
    user.set_password(password)

    # Set password changed to true
    if not user.is_password_changed:
        user.is_password_changed = True

    user.save()
    return True
