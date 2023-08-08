from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from src.apps.accounts.api import exceptions as accounts_exceptions
from src.apps.authentication.api import tokens
from src.apps.core.base_api.serializers import BaseSerializer

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
                raise accounts_exceptions.UserNotExists()

            user = user.first()
            # Check if the user is inactive
            if not user.is_active:
                raise accounts_exceptions.UserNotActive()

            # if not user.is_password_changed:
            #     raise accounts_exceptions.FirstTimePasswordError(user=user)

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
