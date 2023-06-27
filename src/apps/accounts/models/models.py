import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from . import utils
from .managers import CustomUserManager, ProxyUserManger


class User(AbstractUser):
    objects = CustomUserManager()

    class Type(models.TextChoices):
        STUDENT = "Student", "student"
        TEACHER = "Teacher", "teacher"
        ADMIN = "Admin", "admin"

    # Set username to none
    username = None
    # first_name = None
    # last_name = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(("email address"), unique=True, validators=[validate_email])
    USERNAME_FIELD = "email"  # Set email field as a username
    REQUIRED_FIELDS = ["password"]  # Remove email from required fields

    phone_number = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    identification = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=Type.choices, blank=True, default=Type.ADMIN)
    is_verified = models.BooleanField(default=False)
    manager = models.ForeignKey("Admin", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class Teacher(User):
    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.TEACHER)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.TEACHER
        return super().save(*args, **kwargs)


class Student(User):
    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.STUDENT)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.STUDENT
        return super().save(*args, **kwargs)


class Admin(User):
    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.ADMIN)

    def save(self, *args, **kwargs) -> None:
        self.is_staff = True
        self.is_superuser = True
        self.type = User.Type.ADMIN
        return super().save(*args, **kwargs)


class OTPNumber(models.Model):
    number = models.CharField(max_length=16, null=True)
    is_verified = models.BooleanField(default=False)
    valid_until = models.DateTimeField(
        default=timezone.now,
        help_text="The timestamp of the moment of expiry of the saved number.",
    )

    user = models.ForeignKey(
        to="User",
        related_name="otp_number",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs) -> None:
        self.valid_until = timezone.now() + timedelta(seconds=settings.OTP_EXPIRATION)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.number}"

    def check_num(self, number: str) -> bool:
        """Verifies a number by content and expiry.

        Args:
            number (str): the number which to be checked

        Returns:
            bool: success or fail
        """
        _now = timezone.now()

        if (self.number is not None) and (number == self.number) and (_now < self.valid_until):
            # self.number = None
            self.valid_until = _now
            self.save()

            return True
        else:
            return False

    @staticmethod
    def get_number(length=6) -> str:
        """Generate an OTP number for the user.

        Args:
            length (int, optional): The number of digits to return. Defaults to 6.

        Returns:
            str: A string of decimal digits
        """

        return utils.generate_random_number(length)
