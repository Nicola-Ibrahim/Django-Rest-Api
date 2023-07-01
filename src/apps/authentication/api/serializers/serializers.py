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
        tokens.CustomRefreshToken(validated_data.get("refresh"), verify=True).blacklist()
        return True
