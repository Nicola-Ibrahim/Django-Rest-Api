from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from mailers import BaseMailer


class OTPMailer(BaseMailer):
    """
    Email service for sending OTP (One-Time Password) for password reset.

    Usage Example:
        otp_mailer = OTPMailer(otp_number="123456", to_emails=["user@example.com"])
        mail_service = otp_mailer.create_service()
        mail_service.send(fail_silently=False)
    """

    template_name = "accounts/emails/forget_password.html"
    subject = _("Reset the password")

    def __init__(self, otp_number: str, to_emails: list[str]) -> None:
        """
        Initializes the OTPMailer instance.

        Args:
            otp_number (str): One-Time Password to be included in the email.
            to_emails (list[str]): List of recipient email addresses.

        Returns:
            None
        """
        self.otp_number = otp_number
        self.to_emails = to_emails
        super().__init__(to_emails=to_emails)

    def _get_html_content(self) -> str:
        """
        Generates the HTML content for the email body.

        Returns:
            str: HTML content for the email body.
        """
        context = {
            "email": self.to_emails[0],
            "otp_number": self.otp_number,
        }

        return render_to_string(template_name=self.template_name, context=context)
