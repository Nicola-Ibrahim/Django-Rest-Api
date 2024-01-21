from datetime import timedelta

from apps.accounts.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import utils


class OTPNumber(models.Model):
    number = models.CharField(
        max_length=16,
        null=True,
        verbose_name=_("number"),
        help_text=_("The OTP number sent to the user"),
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_("verified"),
        help_text=_("Whether the OTP number has been verified by the user"),
    )
    valid_until = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("valid until"),
        help_text=_("The timestamp of the moment of expiry of the saved number."),
    )

    user = models.ForeignKey(
        to=User,
        related_name="otp_number",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("user"),
        help_text=_("The user associated with the OTP number"),
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
