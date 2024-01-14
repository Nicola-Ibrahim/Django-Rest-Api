from apps.accounts.api.exceptions import UserNotFoundAPIException
from apps.accounts.models import User
from apps.accounts.models.validators import user_validate_password
from django.contrib.auth import get_user_model
from lib.api.serializers import BaseSerializer
from rest_framework import serializers

from .. import models
from . import exceptions


class LoginSerializer(BaseSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, value):
        if value:
            # Check if the email exists in the user mode
            user = User.objects.filter(email=value)
            if not user.exists():
                raise UserNotFoundAPIException()

            user = user.first()
            # Check if the user is inactive
            if not user.is_active:
                raise exceptions.UserNotActiveAPIException()

            # if not user.is_password_changed:
            #     raise FirstTimePasswordError(user=user)

        return value


class LogoutSerializer(BaseSerializer):
    refresh = serializers.CharField()


class ForgetPasswordRequestSerializer(BaseSerializer):
    """This serializer is responsible for creating a number for the user who requested password reset"""

    email = serializers.EmailField(min_length=2, required=True)

    class Meta:
        fields = ["email"]

    def validate_email(self, value):
        # Check if the email exists in the user model
        if not get_user_model().objects.filter(email=value).exists():
            raise UserNotFoundAPIException()

        return value


class VerifyOTPNumberSerializer(BaseSerializer):
    email = serializers.EmailField(min_length=1, write_only=True)
    otp = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        user = get_user_model().objects.filter(email=attrs["email"])
        if not user.exists():
            raise UserNotFoundAPIException()

        otp_instance = models.OTPNumber.objects.filter(user=user.first(), number=attrs["otp"])

        # Check if the OTP number does not exists
        if not otp_instance.exists():
            raise exceptions.WrongOTPAPIException()

        otp_instance = otp_instance.first()

        # If the OTP number is expired
        if not otp_instance.check_num(attrs["otp"]):
            raise exceptions.ExpiredOTPAPIException()

        return attrs


class ChangePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, passwords and otp number"""

        # Validate the if the old password is correct for the request user
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise exceptions.WrongPasswordAPIException()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswordsAPIException()

        # Validate the password if it meets all validator requirements
        user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs


class ForgetPasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)
    otp = serializers.CharField(min_length=1, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, passwords and otp number"""

        user = self.context["request"].user
        otp_instance = models.OTPNumber.objects.filter(user=user, number=attrs["otp"])

        # Check if the OTP number does not exists
        if not otp_instance.exists():
            raise exceptions.WrongOTPAPIException()

        # Check if the user OTP number is verified
        if not otp_instance.first().is_verified:
            raise exceptions.OTPNotVerified()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswordsAPIException()

        # Validate the password if it meets all validator requirements
        user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs


class FirstTimePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a first time password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, validate passwords and otp number"""

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswordsAPIException()

        # Validate the password if it meets all validator requirements
        user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs
