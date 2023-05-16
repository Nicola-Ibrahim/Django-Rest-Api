import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands import createsuperuser
from django.db.utils import IntegrityError


class Command(createsuperuser.Command):
    help = "Crate a superuser, and allow password to be provided"
    logger = logging.getLogger(__name__)

    def handle(self, *args, **options):
        print("Creating root superuser...")

        try:
            get_user_model().objects.create_superuser(
                email=settings.ROOT_USER_EMAIL,
                first_name=settings.ROOT_USER_FIRSTNAME,
                last_name=settings.ROOT_USER_LASTNAME,
                password=settings.ROOT_USER_PASSWORD,
            )

            self.logger.info("Root Superuser has been created!")

        except AttributeError as e:
            self.logger.error(
                f"""The following '{str(e).split("'")[-2]}' attribute\nPlease define it in .env file or /local/settings.dev.py file."""
            )

        except IntegrityError:
            self.logger.error(
                f"The root super user with following email '{settings.ROOT_USER_EMAIL}' address is already exists."
            )
