"""
This file contains custom users manager classes
"""

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    """
    Creates and saves a User with the given email and password.
    """

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email or len(email) <= 0:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_verified") is not True:
            raise ValueError("Superuser must have is_verified=True.")

        return self._create_user(email, password, **extra_fields)


class ProxyUserManger(CustomUserManager):
    def __init__(self, user_type):
        self.user_type = user_type
        super().__init__()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(type=self.user_type)
