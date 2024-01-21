from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from ...core.tasks.tasks import send_otp_number_email
from . import models


@receiver(post_save, sender=models.OTPNumber)
def send_otp_number_to_user(sender, instance, created, **kwargs) -> None:
    """
    Signal handler to send OTP (One-Time Password) to the user after saving OTPNumber instance.

    Args:
        sender: The model class.
        instance: The saved instance of the OTPNumber model.
        created (bool): True if a new instance was created, False if it was updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    Note:
        The email sending is deferred until after the transaction commit to ensure the instance
        is saved completely with its services.

    Usage Example:
        This signal is automatically triggered when a new OTPNumber instance is created.
    """
    if created:
        # Defer sending email until after transaction commit
        # Using transaction to ensure the instance is saved completely with its services.
        transaction.on_commit(
            lambda: send_otp_number_email.delay(otp_number=instance.number, user_email=instance.email)
        )
