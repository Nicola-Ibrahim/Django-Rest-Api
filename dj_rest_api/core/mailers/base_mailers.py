from abc import ABC, abstractmethod
from collections.abc import Iterable

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class BaseMailer(ABC):
    """
    An factory abstract mailer for sending an email.

    This class provides a common interface and functionality for different
    email services. Subclasses can customize subject, body, and from_email.
    """

    subject = ""
    body = ""
    from_email = settings.EMAIL_HOST_USER

    def __init__(self, to_emails: Iterable[str], from_email=None) -> None:
        """
        Initialize the BaseMailer with the given arguments.

        Args:
            to_emails (iterable): The recipient(s) of the email.
            from_email (str, optional): The sender's email address. Defaults to settings.DEFAULT_FROM_EMAIL.
        """
        self.from_email = from_email or self.from_email
        self.to_emails = [to_emails] if not isinstance(to_emails, list) else to_emails

    def create_service(self) -> EmailMultiAlternatives:
        """
        Create an EmailMultiAlternatives instance for sending the email.
        """
        mail = EmailMultiAlternatives(
            subject=self.subject,
            body=self.body,
            from_email=self.from_email,
            to=self.to_emails,
        )

        # Add HTML content as an alternative
        html_content = self._get_html_content()
        mail.attach_alternative(html_content, "text/html")

        return mail

    @abstractmethod
    def _get_html_content(self) -> str:
        """Get the html data to render in the email body."""
        return ""
