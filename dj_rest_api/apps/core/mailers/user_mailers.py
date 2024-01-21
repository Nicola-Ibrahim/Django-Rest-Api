from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from mailers import BaseMailer

from ...accounts import services


class RegisterMailer(BaseMailer):
    """
    Mailer for sending a welcome email to the client with a token value.

    This class inherits from BaseMailer and customizes the email body by rendering a template.
    """

    template_name = "accounts/emails/appointment_welcome_email.html"
    subject = _("Welcome to Our Service")

    def __init__(self, full_name: str, to_emails: list[str]) -> None:
        """Initialize the RegisterMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            full_name (str): The user's full name.
        """
        self.full_name = full_name
        super().__init__(to_emails=to_emails)

    def _get_html_content(self) -> str:
        context = {
            "full_name": self.full_name,
        }

        return render_to_string(template_name=self.template_name, context=context)


class VerificationMailer(BaseMailer):
    """Mailer for sending a verification email to the new registered user with token value.

    This class inherits from BaseMailer and customizes the email body by rendering a template.
    """

    template_name = "accounts/emails/account_verification.html"
    subject = _("Verify your account")

    def __init__(self, to_email: list[str], request) -> None:
        """Initialize the VerificationMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            request (HttpRequest): The request object that contains information about the current site domain.
        """
        self.request = request

        super().__init__(to_emails=to_email)

    def _get_html_content(self) -> str:
        """Edit body by adding a link with a token value for verifying the email.

        This method overrides the abstract method of BaseMailer and appends a link with a token value
        for verifying the email to the body attribute. It uses some helper functions and models to
        construct the link.

        """
        absurl = services.get_verification_url(self.request, email=self.to_emails[0])

        context = {
            "email": self.to_emails[0],
            "link": absurl,
        }

        return render_to_string(template_name="authentication/account_verification.html", context=context)
