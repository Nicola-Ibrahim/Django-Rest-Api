from abc import ABC, abstractmethod

from django.conf import settings
from django.core.mail import EmailMessage


class BaseEmailService(ABC):
    """An abstract base class for email service.

    This class defines a common interface for sending emails using different
    email backends. Subclasses should implement the send_email method to
    provide the specific logic for each backend.
    """

    def __init__(self, subject: str, body: str, from_email: str, to: list[str]) -> None:
        """Initialize the email service with the message details.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
            from_email (str): The sender's email address.
            to (list[str]): A list of recipient's email addresses.
        """
        self.mail = EmailMessage(subject=subject, body=body, from_email=from_email, to=to)

    @abstractmethod
    def send_email(self):
        """Send the email using the specific backend.

        This method should be implemented by subclasses to provide the logic
        for sending the email using the desired backend. It should use the
        self.mail attribute as the message object.

        Raises:
            Exception: If not implemented by subclasses.
        """
        raise Exception("Must implement")


class GmailService(BaseEmailService):
    """A concrete Gmail service for sending emails using Gmail SMTP.

    This class inherits from BaseEmailService and implements the send_email

    """

    def send_email(self) -> None:
        self.mail.send(fail_silently=False)


class ConsolEmailService(BaseEmailService):
    """A concrete console service for displaying emails in console.

    This class inherits from BaseEmailService and implements the send_email
    """

    def send_email(self) -> None:
        """Display the email in console."""
        self.mail.send(fail_silently=False)


class EmailServiceFactory:
    """A factory class for creating email service objects.

    This class provides a factory method that creates email service objects
    based on the settings.EMAIL_BACKEND value. It supports Gmail and console
    backends, and returns an instance of a subclass of BaseEmailService.
    """

    def __init__(self, subject: str, body: str, from_email: str, to_emails: list[str]) -> None:
        """Initialize the factory with the email message details.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
            from_email (str): The sender's email address.
            to_emails (list[str]): A list of recipient's email addresses.
        """
        # Store the message details as attributes
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.to_emails = to_emails

    def create_service(self) -> BaseEmailService:
        """Create an email service object based on the settings.EMAIL_BACKEND value.

        This method uses the settings.EMAIL_BACKEND value to determine which
        subclass of BaseEmailService to instantiate and return. It passes the
        message details to the constructor of the subclass.

        Returns:
            BaseEmailService: An instance of a subclass of BaseEmailService.

        Raises:
            ValueError: If settings.EMAIL_BACKEND is not a valid option.
        """

        # Email in Gmail
        if settings.EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
            if settings.EMAIL_HOST == "smtp.gmail.com":
                # Return an instance of GmailService
                return GmailService(
                    subject=self.subject,
                    body=self.body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=self.to_emails,
                )

        # Email in console
        elif settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
            # Return an instance of ConsolEmailService
            return ConsolEmailService(
                subject=self.subject,
                body=self.body,
                from_email=self.from_email,
                to=self.to_emails,
            )

        # Invalid option
        else:
            raise ValueError(f"Invalid service type: {settings.EMAIL_BACKEND}")
