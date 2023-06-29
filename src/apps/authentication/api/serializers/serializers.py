from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from src.apps.accounts.api import exceptions as accounts_exceptions
from src.apps.accounts.models.models import OTPNumber
from src.apps.accounts.models.validators import user_validate_password
from src.apps.core.base_api import tokens
from src.apps.core.base_api.serializers import BaseSerializer

from .. import exceptions as authentication_exceptions


class LoginSerializer(BaseSerializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)

        email = attrs["email"]
        password = attrs["password"]

        if email and password:
            # Check if the user is inactive
            user = get_user_model().objects.filter(email=email)
            if not user.exists():
                raise accounts_exceptions.UserNotExists()

            user = user.first()

            if not user.is_active:
                raise accounts_exceptions.UserNotActive()

            # Authenticate the user
            user = authenticate(
                request=self.context["request"],
                username=email,
                password=password,
            )

            if not user:
                raise accounts_exceptions.CredentialsNotValid()

            if not user.is_password_changed:
                raise authentication_exceptions.FirstTimePasswordError(user=user)

            attrs["user"] = user
        return attrs


class LogoutSerializer(BaseSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get("refresh")

        return attrs

    def create(self, validated_data):
        tokens.CustomRefreshToken(
            validated_data.get("refresh"), verify=True
        ).blacklist()
        return True


class ForgetPasswordRequestSerializer(BaseSerializer):
    """This serializer is responsible for creating a number for the user who requested password reset"""

    email = serializers.EmailField(min_length=2, required=True)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email", "")

        # Check the user existence
        user = get_user_model().objects.filter(email=email)

        if not user.exists():
            raise accounts_exceptions.UserNotExists()

        user = user.first()

        attrs["email"] = email
        attrs["otp"] = OTPNumber.get_number()
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """Create an OTP number for the user"""

        instance = OTPNumber.objects.update_or_create(
            defaults={
                "number": validated_data.get("otp"),
                "user": validated_data.get("user"),
                "is_verified": False,
            }
        )
        return instance


class VerifyOTPNumberSerializer(BaseSerializer):
    otp = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        otp = attrs.get("otp", "")

        user = self.context["request"].user
        otp_instance = OTPNumber.objects.filter(user=user, number=otp)

        # Check if the OTP number does not exists
        if not otp_instance.exists():
            raise authentication_exceptions.WrongOTP()

        # If the OTP number is expired
        if not otp_instance.first().check_num(otp):
            raise authentication_exceptions.OTPExpired()

        return attrs

    def create(self, validated_data):
        """Update the is_verified field after validate the otp number assigned to user"""

        # Get the OTP number of the user
        instance = OTPNumber.objects.get(
            user=self.context["request"].user, number=validated_data.get("otp")
        )

        # Set OTP number to be verified
        instance.is_verified = True
        instance.save()

        return True


class ChangePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate(self, attrs: dict):
        """Validate the inserted data, passwords and otp number"""

        # Validate the if the old password is correct for the request user
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise accounts_exceptions.WrongPassword()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise accounts_exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs

    def create(self, validated_data):
        """Update the user's password"""

        # Get user from the request
        user = self.context["request"].user

        # Set the new password for the user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Delete otp number for the user
        OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


class ForgetPasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )
    otp = serializers.CharField(min_length=1, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, passwords and otp number"""

        otp = attrs.get("otp", "")

        user = self.context["request"].user
        otp_instance = OTPNumber.objects.filter(user=user, number=otp)

        # Check if the OTP number does not exists
        if not otp_instance.exists():
            raise authentication_exceptions.WrongOTP()

        # Check if the user OTP number is verified
        if not otp_instance.first().is_verified:
            raise authentication_exceptions.OTPNotVerified()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise accounts_exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs

    def create(self, validated_data):
        """Update the user's password"""

        # Get user from the request
        user = self.context["request"].user

        # Set the new password for the user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Delete otp number for the user
        OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


class FirstTimePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a first time password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate(self, attrs: dict):
        """Validate the inserted data, validate passwords and otp number"""

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise accounts_exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs

    def create(self, validated_data):
        """Update the user's password"""
        user = self.context["request"].user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Set password changed to true
        if not user.is_password_changed:
            user.is_password_changed = True
            user.save()

        user.save()
        return user
