import logging
from abc import ABC, abstractmethod

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.services import BaseEmailService, EmailServiceFactory


class BaseMailer(ABC):
    """An abstract mailer for sending an email.

    This class provides a common interface and functionality for different
    email services. It uses a factory method to create suitable email services
    depending on the settings. It also defines an abstract method to edit the
    body if additional data should be added.
    """

    def __init__(self, subject: str, body: str, to_emails: list[str]) -> None:
        """Initialize the BaseMailer with the given arguments.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
            to_email (str): The recipient of the email.
        """
        self.subject = subject
        self.body = body
        self.from_email = settings.EMAIL_HOST_USER
        self.to_emails = to_emails

        # Add new changes to email's body if there is any.
        self.edit_body()

        # Create an email services depending on the configuration settings
        self.create_service()

    def create_service(self):
        self.email_service: BaseEmailService = EmailServiceFactory(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            to_emails=self.to_emails,
        ).create_service()

    # def init_email(self) -> None:
    #     """Create an email entity with the plugged data.

    #     This method calls the init_email method of the email_service object to create an
    #     email entity with the given subject, body and recipient.

    #     Raises:
    #         Exception: If email_service is None.
    #     """
    #     if not self.email_service:
    #         raise Exception("You must provide an email service")

    #     self.email_service.init_email()

    def send_email(self) -> None:
        """Send the email using the email service.

        This method calls the send_email method of the email_service object to send the
        email entity. It also handles any exceptions that may occur during the process and
        logs them using a logger object.

        """
        # self.init_email()

        try:
            self.email_service.send_email()

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Error at %s", "mailer", exc_info=e)

    @abstractmethod
    def edit_body(self) -> None:
        """Edit body if addition data should be added.

        This is an abstract method that should be implemented by subclasses of BaseMailer
        to modify the body attribute if necessary. For example, adding a signature or a
        greeting.
        """


class RegisterMailer(BaseMailer):
    """Concrete Mailer for sending a welcome email with password to the user.

    This class inherits from BaseMailer and implements the edit_body method to add the
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
        super().__init__(
            subject=settings.EMAIL_REGISTER_SUBJECT,
            body="",
            to_emails=to_emails,
        )

    def edit_body(self) -> None:
        """Edit body by adding the user's full name and password.

        This method overrides the abstract method of BaseMailer and appends the user's full
        name and password to the body attribute.

        """

        context = {"full_name": self.full_name, "password": self.password}

        self.body = render_to_string(template_name="authentication/registration_email.html", context=context)


class OTPMailer(BaseMailer):
    """Concrete Mailer for sending an email with OTP number to the user.

    This class inherits from BaseMailer and implements the edit_body method to add the
    OTP number to the body.

    """

    def __init__(self, otp_number: str, to_emails: list[str]) -> None:
        """Initialize the OTPMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            otp_number (str): The OTP number for resetting the password.
        """
        self.otp_number = otp_number
        super().__init__(
            subject=settings.EMAIL_RESETPASSWORD_SUBJECT,
            body="",
            to_emails=to_emails,
        )

    def edit_body(self) -> None:
        """Edit body by adding the OTP number.

        This method overrides the abstract method of BaseMailer and appends the OTP number
        to the body attribute.

        """
        context = {"email": self.to_emails[0], "otp_number": self.otp_number}

        self.body = render_to_string(template_name="authentication/forget_password.html", context=context)


class VerificationMailer(BaseMailer):
    """Concrete Mailer for sending a verification email to the new registered user with token value.

    This class inherits from BaseMailer and implements the edit_body method to add a link
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

        super().__init__(
            subject=settings.EMAIL_EMAIL_VERIFICATION_SUBJECT,
            body=settings.EMAIL_EMAIL_VERIFICATION_body,
            to_emails=to_emails,
        )

    def edit_body(self) -> None:
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

        self.body = render_to_string(template_name="authentication/account_verification.html", context=context)
