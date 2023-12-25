from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from .mailers import RegisterMailer, VerificationMailer


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
