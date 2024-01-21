from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from mailers import OTPMailer, RegisterMailer, VerificationMailer


@shared_task(bind=True, max_retries=3)
def send_otp_number_email(self, otp_number: str, user_email: str) -> None:
    """
    Sends an email containing the OTP number for user verification.

    Args:
        self: Reference to the shared task instance.
        otp_number (str): One-Time Password to be sent. Should be a numerical code.
        user_email (str): Email address of the user.

    Returns:
        str: Success message if the email is sent successfully. Returns None in case of failure.

    Raises:
        MaxRetriesExceededError: If maximum retry attempts are exceeded.

    Note:
        This task uses exponential backoff for retries (2^retry_number seconds).

    Usage Example:
        send_otp_number_email.delay(args=["123456", "user@example.com"])
    """
    try:
        mail = OTPMailer(otp_number=otp_number, to_emails=user_email).create_service()

        # Send the OTP email
        mail.send(fail_silently=False)

    except Exception as exc:
        # Retry the task if the maximum retries are not reached
        if self.request.retries < self.max_retries:
            self.retry(exc=exc, countdown=2**self.request.retries)
        else:
            # Handle the case where retries are exhausted
            raise MaxRetriesExceededError(f"Max retries exceeded: {exc}") from exc


@shared_task(bind=True, max_retries=3)
def send_account_created_email(self, full_name: str, user_email: str):
    try:
        mail = RegisterMailer(full_name=full_name, to_emails=user_email).create_service()

        mail.send(fail_silently=False)

        return "Created account email has been sent...!"
    except Exception as exc:
        if self.request.retries < self.max_retries:
            # Retry the task with exponential backoff (2^retry_number seconds)
            self.retry(exc=exc, countdown=2**self.request.retries)
        else:
            # Handle the case where retries are exhausted (optional)
            raise MaxRetriesExceededError(f"Max retries exceeded: {exc}") from exc


@shared_task(bind=True, max_retries=3)
def send_account_verification_email(self, request, user_email: str):
    try:
        mail = VerificationMailer(request=request, to_emails=user_email).create_service()

        mail.send(fail_silently=False)

        return "Account verification email has been sent...!"
    except Exception as exc:
        if self.request.retries < self.max_retries:
            # Retry the task with exponential backoff (2^retry_number seconds)
            self.retry(exc=exc, countdown=2**self.request.retries)
        else:
            # Handle the case where retries are exhausted (optional)
            raise MaxRetriesExceededError(f"Max retries exceeded: {exc}") from exc
