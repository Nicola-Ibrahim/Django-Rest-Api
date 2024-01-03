from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from lib.mailers import BaseMailer
from rest_framework_simplejwt.tokens import RefreshToken


class OTPMailer(BaseMailer):
    """Mailer for sending an email with OTP number to the user.

    This class inherits from BaseMailer and customizes the email body by rendering a template.
    """

    template_name = "accounts/emails/forget_password.html"
    subject = _("Reset the password")

    def __init__(self, otp_number: str, to_emails: list[str]) -> None:
        """Initialize the OTPMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            otp_number (str): The OTP number for resetting the password.
        """
        self.otp_number = otp_number
        self.to_emails = to_emails
        super().__init__(to_emails=to_emails)

    def _get_html_content(self) -> str:
        context = {
            "email": self.to_emails[0],
            "otp_number": self.otp_number,
        }

        return render_to_string(template_name=self.template_name, context=context)
