from apps.accounts.api.exceptions import FirstTimePasswordError, UserNotActive, UserNotExists
from apps.accounts.models.validators import user_validate_password
from apps.authentication.api import tokens
from django.contrib.auth import authenticate, get_user_model
from lib.api.serializers import BaseSerializer
from rest_framework import serializers

from ... import models
from .. import exceptions


class LoginSerializer(BaseSerializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)

        email = attrs["email"]
        password = attrs["password"]

        if email and password:
            # Check if the user is exists
            user = get_user_model().objects.filter(email=email)
            if not user.exists():
                raise UserNotExists()

            user = user.first()
            # Check if the user is inactive
            if not user.is_active:
                raise UserNotActive()

            # if not user.is_password_changed:
            #     raise FirstTimePasswordError(user=user)

            # Authenticate the user
            user = authenticate(
                request=self.context["request"],
                username=email,
                password=password,
            )

            if not user:
                raise exceptions.CredentialsNotValid()

            attrs["user"] = user
        return attrs


class LogoutSerializer(BaseSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get("refresh")

        return attrs

    def create(self, validated_data):
        tokens.CustomRefreshToken(validated_data.get("refresh"), verify=True).blacklist()
        return True


class ForgetPasswordRequestSerializer(BaseSerializer):
    """This serializer is responsible for creating a number for the user who requested password reset"""

    email = serializers.EmailField(min_length=2, required=True)

    class Meta:
        fields = ["email"]

    def validate_email(self, value):
        # Check if the email exists in the user model
        if not get_user_model().objects.filter(email=value).exists():
            raise exceptions.UserNotExists()

        return value

    def create(self, validated_data):
        """Create an OTP number for the user"""
        email = validated_data.get("email")
        user = get_user_model().objects.get(email=email)

        otp_instance, created = models.OTPNumber.objects.update_or_create(
            defaults={
                "number": models.OTPNumber.get_number(),
                "user": user,
                "is_verified": False,
            }
        )
        return otp_instance


class VerifyOTPNumberSerializer(BaseSerializer):
    email = serializers.EmailField(min_length=1, write_only=True)
    otp = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        user = get_user_model().objects.filter(email=attrs["email"])
        if not user.exists():
            raise exceptions.UserNotExists()

        otp_instance = models.OTPNumber.objects.filter(user=user.first(), number=attrs["otp"])

        # Check if the OTP number does not exists
        if not otp_instance.exists():
            raise exceptions.WrongOTP()

        otp_instance = otp_instance.first()

        # If the OTP number is expired
        if not otp_instance.check_num(attrs["otp"]):
            raise exceptions.OTPExpired()

        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        user = get_user_model().objects.get(email=email)
        otp_instance = models.OTPNumber.objects.get(user=user, number=validated_data["otp"])

        # Set the is_verified flag to True
        otp_instance.is_verified = True
        otp_instance.save()
        return otp_instance


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
            raise exceptions.WrongPassword()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

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
        models.OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


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
            raise exceptions.WrongOTP()

        # Check if the user OTP number is verified
        if not otp_instance.first().is_verified:
            raise exceptions.OTPNotVerified()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        validators.user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs

    def create(self, validated_data):
        """Update the user's password"""

        # Get user from the request
        user = self.context["request"].user

        # Set the new password for the user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Delete otp number for the user
        models.OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


class FirstTimePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a first time password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, validate passwords and otp number"""

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        validators.user_validate_password(attrs["new_password"], self.context["request"].user)

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
