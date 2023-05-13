import logging
from abc import ABC, abstractmethod

from core.services import BaseEmailService, GmailService, 
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from core.services import EmailServiceFactory

class BaseMailer(ABC):
    """An abstract mailer for sending an email.

    This class provides a common interface and functionality for different
    email services. It uses a factory method to create suitable email services
    depending on the settings. It also defines an abstract method to edit the
    message if additional data should be added.
    """

    def __init__(self, subject: str, message: str, to_email: str) -> None:
        """Initialize the BaseMailer with the given arguments.

        Args:
            subject (str): The subject of the email.
            message (str): The body of the email.
            to_email (str): The recipient of the email.
        """
        self.subject = subject
        self.message = message
        self.to_email = to_email

        

        # Add new changes to email's message if there is any.
        self.edit_message()

        # Create an email services depending on the configuration settings
        self.create_service()

    
    def create_service(self):    
        
        self.email_service: BaseEmailService = EmailServiceFactory(self.subject, self.message, self.to_email).create_service()

    def init_email(self) -> None:
        """Create an email entity with the plugged data.

        This method calls the init_email method of the email_service object to create an
        email entity with the given subject, message and recipient.

        Raises:
            Exception: If email_service is None.
        """
        if not self.email_service:
            raise Exception("You must provide an email service")

        self.email_service.init_email()

    def send_email(self) -> None:
        """Send the email using the email service.

        This method calls the send_email method of the email_service object to send the
        email entity. It also handles any exceptions that may occur during the process and
        logs them using a logger object.

        """
        self.init_email()

        try:
            self.email_service.send_email()

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Error at %s", "mailer", exc_info=e)

    @abstractmethod
    def edit_message(self) -> None:
        """Edit message if addition data should be added.

        This is an abstract method that should be implemented by subclasses of BaseMailer
        to modify the message attribute if necessary. For example, adding a signature or a
        greeting.
        """


class RegisterMailer(BaseMailer):
    """Concrete Mailer for sending a welcome email with password to the user.

    This class inherits from BaseMailer and implements the edit_message method to add the
    user's full name and password to the message.

    """

    def __init__(self, to_email, full_name, password) -> None:
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
            message=settings.EMAIL_REGISTER_MESSAGE,
            to_email=to_email,
        )

    def edit_message(self) -> None:
        """Edit message by adding the user's full name and password.

        This method overrides the abstract method of BaseMailer and appends the user's full
        name and password to the message attribute.

        """
        self.message += f"\n{self.full_name}\nYour password is:'{self.password}'"


class OTPMailer(BaseMailer):
    """Concrete Mailer for sending an email with OTP number to the user.

    This class inherits from BaseMailer and implements the edit_message method to add the
    OTP number to the message.

    """

    def __init__(self, to_email: str, otp_number: str) -> None:
        """Initialize the OTPMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            otp_number (str): The OTP number for resetting the password.
        """
        self.otp_number = otp_number
        super().__init__(
            subject=settings.EMAIL_RESETPASSWORD_SUBJECT,
            message=settings.EMAIL_RESETPASSWORD_MESSAGE,
            to_email=to_email,
        )

    def edit_message(self) -> None:
        """Edit message by adding the OTP number.

        This method overrides the abstract method of BaseMailer and appends the OTP number
        to the message attribute.

        """
        self.message += f"\n otp:'{self.otp_number}'"


class VerificationMailer(BaseMailer):
    """Concrete Mailer for sending a verification email to the new registered user with token value.

    This class inherits from BaseMailer and implements the edit_message method to add a link
    with a token value for verifying the user's email.

    """

    def __init__(self, to_email: str, token: str, request) -> None:
        """Initialize the VerificationMailer with the given arguments.

        Args:
            to_email (str): The recipient of the email.
            token (str): The token value for verifying the email.
            request (HttpRequest): The request object that contains information about the current site domain.
        """
        self.to_email = to_email
        self.token = token
        self.request = request

        super().__init__(
            subject=settings.EMAIL_EMAIL_VERIFICATION_SUBJECT,
            message=settings.EMAIL_EMAIL_VERIFICATION_MESSAGE,
            to_email=to_email,
        )

    def edit_message(self) -> None:
        """Edit message by adding a link with a token value for verifying the email.

        This method overrides the abstract method of BaseMailer and appends a link with a token value
        for verifying the email to the message attribute. It uses some helper functions and models to
        construct the link.

        """
        # Get the user by the inserted email
        user = get_user_model().objects.get(email=self.to_email)

        # Get refresh token to this user
        token = RefreshToken.for_user(user).access_token

        # Get the current site domain
        current_site = get_current_site(self.request).domain

        # Get the url of the "email-verify" view
        relativeLink = reverse("accounts:email-verify")  # -> /api/accounts/verify_email/

        # Sum up the final url for verification
        absurl = "http://" + current_site + relativeLink + "?token=" + str(token)

        self.message += f"Hi {user.email} Use the link below to verify your email\n{absurl}"
