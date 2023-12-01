from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.mailers import BaseMailer


class RegisterMailer(BaseMailer):
    """Concrete Mailer for sending a welcome email with password to the user.

    This class inherits from BaseMailer and implements the _get_body method to add the
    user's full name and password to the body.

    """

    def __init__(self, full_name, password, to_emails: list[str]) -> None:
        """Initialize the RegisterMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            full_name (str): The user's full name.
            password (str): The user's password.
        """
        self.full_name = full_name
        self.password = password
        super().__init__(to_emails=to_emails)

    def _get_body(self) -> str:
        """Edit body by adding the user's full name and password.

        This method overrides the abstract method of BaseMailer and appends the user's full
        name and password to the body attribute.

        """

        context = {"full_name": self.full_name, "password": self.password}

        return render_to_string(template_name="accounts/registration_email.html", context=context)

    def _get_subject(self) -> str:
        return settings.EMAIL_REGISTER_SUBJECT


class OTPMailer(BaseMailer):
    """Concrete Mailer for sending an email with OTP number to the user.

    This class inherits from BaseMailer and implements the _get_body method to add the
    OTP number to the body.

    """

    def __init__(self, otp_number: str, to_emails: list[str]) -> None:
        """Initialize the OTPMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            otp_number (str): The OTP number for resetting the password.
        """
        self.otp_number = otp_number
        self.to_emails = to_emails
        super().__init__(to_emails=to_emails)

    def _get_body(self) -> str:
        """Edit body by adding the OTP number.

        This method overrides the abstract method of BaseMailer and appends the OTP number
        to the body attribute.

        """
        context = {"email": self.to_emails[0], "otp_number": self.otp_number}

        return render_to_string(template_name="accounts/forget_password.html", context=context)

    def _get_subject(self) -> str:
        return settings.EMAIL_RESETPASSWORD_SUBJECT


class VerificationMailer(BaseMailer):
    """Concrete Mailer for sending a verification email to the new registered user with token value.

    This class inherits from BaseMailer and implements the _get_body method to add a link
    with a token value for verifying the user's email.

    """

    def __init__(self, token: str, to_emails: list[str], request) -> None:
        """Initialize the VerificationMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            token (str): The token value for verifying the email.
            request (HttpRequest): The request object that contains information about the current site domain.
        """
        self.token = token
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

    def _get_subject(self) -> str:
        return settings.EMAIL_EMAIL_VERIFICATION_SUBJECT
