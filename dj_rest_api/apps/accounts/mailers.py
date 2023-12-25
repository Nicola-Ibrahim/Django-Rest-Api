from apps.core.mailers import BaseMailer
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken


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

    def __init__(self, to_emails: list[str], request) -> None:
        """Initialize the VerificationMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            request (HttpRequest): The request object that contains information about the current site domain.
        """
        self.request = request

        super().__init__(to_emails=to_emails)

    def _get_body(self) -> str:
        """Edit body by adding a link with a token value for verifying the email.

        This method overrides the abstract method of BaseMailer and appends a link with a token value
        for verifying the email to the body attribute. It uses some helper functions and models to
        construct the link.

        """
        # Get the user by the inserted email
        user = get_user_model().objects.get(email=self.to_email)

        # Get refresh token to this user
        token = RefreshToken.for_user(user).access_token

        # Get the current site domain
        current_site = get_current_site(self.request).domain

        # Get the url of the "email-verify" view
        relativeLink = reverse("authentication:email-verify")  # -> /api/authentication/verify_email/

        # Sum up the final url for verification
        absurl = "http://" + current_site + relativeLink + "?token=" + str(token)

        context = {
            "email": user.email,
            "link": absurl,
        }

        return render_to_string(template_name="authentication/account_verification.html", context=context)
