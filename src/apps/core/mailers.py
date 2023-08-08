from abc import ABC, abstractmethod
from collections.abc import Iterable

from django.conf import settings
from django.core.mail import EmailMessage


class BaseMailer(ABC):
    """An abstract mailer for sending an email.

    This class provides a common interface and functionality for different
    email services. It uses a factory method to create suitable email services
    depending on the settings. It also defines an abstract method to edit the
    body if additional data should be added.
    """

    def __init__(self, to_emails: Iterable[str]) -> None:
        """Initialize the BaseMailer with the given arguments.

        Args:
            subject (str): The subject of the email.
            body (str): The body of the email.
            to_emails (str): The recipient of the email.
        """
        # Subject of the sent email
        self.subject = self._get_subject()

        # Body of the sent email
        self.body = self._get_body()

        # Main website email
        self.from_email = settings.EMAIL_HOST_USER

        # To user/s email
        self.to_emails = to_emails

        self._create_mail_service()

    def _create_mail_service(self):
        # Create an email services depending on the configuration settings
        self.mail = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            to=self.to_emails,
        )

    def send_email(self) -> None:
        """Send the email to the user/s"""
        self.mail.send(fail_silently=False)

    @abstractmethod
    def _get_body(self) -> str:
        """Inject additional data to email body.

        An abstract method that should be implemented by subclasses of BaseMailer
        to modify the body attribute if necessary. For example, adding a signature or a
        greeting.
        """

    @abstractmethod
    def _get_subject(self) -> str:
        """Get the subject of the email.

        An abstract method that should be implemented by subclasses of BaseMailer
        to modify the subject attribute if necessary.
        """
