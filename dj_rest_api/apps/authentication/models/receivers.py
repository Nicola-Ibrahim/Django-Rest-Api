from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..tasks import send_otp_number_email
from . import models


@receiver(post_save, sender=models.OTPNumber)
def send_otp_number_to_user(sender, instance, created, **kwargs):
    """Send otp number to user for password resetting"""

    if created:
        # Defer sending email until after transaction commit
        # * Using transaction to ensure the instance is save completely with its services.
        transaction.on_commit(
            lambda: send_otp_number_email.delay(otp_number=instance.number, user_email=instance.email)
        )
