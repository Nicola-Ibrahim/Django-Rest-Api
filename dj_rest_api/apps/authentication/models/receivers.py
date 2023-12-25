from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.OTPNumber)
def send_otp_number_to_user(sender, instance, **kwargs):
    """Send otp number to user for password resetting"""

    # Send reset password message with OTP to user's email
    mailers.OTPMailer(otp_number=instance.number, to_emails=[instance.user.email]).send_email()
