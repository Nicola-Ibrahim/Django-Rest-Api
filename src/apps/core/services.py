import logging
from abc import ABC, abstractmethod

from django.conf import settings
from django.core.mail import EmailMessage


class BaseEmailService(ABC):
    """An abstract class for email service"""

    def __init__(self, subject: str, message: str, to: str) -> None:
        self.subject = subject
        self.message = message
        self.to = [to]

    @abstractmethod
    def init_email(self):
        raise Exception("Must implement")

    @abstractmethod
    def send_email(self):
        raise Exception("Must implement")


class GmailService(BaseEmailService):
    """Concrete Gmail service for establishing a Gmail service for sending an email"""

    def __init__(self, subject: str, message: str, from_email: str, to: str) -> None:
        self.mail = EmailMessage()
        self.from_email = from_email
        super().__init__(subject, message, to)

    def init_email(self) -> None:
        self.mail.subject = self.subject
        self.mail.body = self.message
        self.mail.from_email = self.from_email
        self.mail.to = self.to

    def send_email(self) -> None:
        self.init_email()
        self.mail.send(fail_silently=False)


class ConsolEmailService(BaseEmailService):
    """Concrete consol service for displaying an email in consol (For debugging goal)"""

    def __init__(self, subject: str, message: str, to: str) -> None:
        self.logger = logging.getLogger(__name__)
        super().__init__(subject, message, to)

    def init_email(self) -> str:
        message = f"{self.subject}\n{self.message}\n{self.to}"
        return message

    def send_email(self) -> None:
        message = self.init_email()
        self.logger.info(message)


class EmailServiceFactory:
    def __init__(self, subject: str, message: str, to_email: str) -> None:
        self.subject = subject
        self.message = message
        self.to_email = to_email

    def create_service(self) -> BaseEmailService:
        """Factory method to create suitable email services depending on the define settings.

        This method assigns the email_service attribute to an instance of a subclass of
        BaseEmailService based on the value of settings.EMAIL_BACKEND. It also calls the
        edit_message method to add any changes to the message.

        Raises:
            ValueError: If settings.EMAIL_BACKEND is not a valid option.
        """

        # Email in Gmail
        if settings.EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
            return GmailService(
                subject=self.subject,
                message=self.message,
                from_email=settings.EMAIL_HOST_USER,
                to=self.to_email,
            )

        # Email in consol
        elif settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
            return ConsolEmailService(subject=self.subject, message=self.message, to=self.to_email)
