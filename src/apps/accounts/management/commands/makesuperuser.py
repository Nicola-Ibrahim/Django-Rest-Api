from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands import createsuperuser
from django.db.utils import IntegrityError


class Command(createsuperuser.Command):
    help = "Crate a superuser, and allow password to be provided"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Creating root superuser..."))

        try:
            get_user_model().objects.create_superuser(
                email=settings.ROOT_USER_EMAIL,
                first_name=settings.ROOT_USER_FIRSTNAME,
                last_name=settings.ROOT_USER_LASTNAME,
                password=settings.ROOT_USER_PASSWORD,
            )

            self.stdout.write(self.style.SUCCESS("Root Superuser has been created!"))

        except AttributeError as e:
            self.stdout.write(
                self.style.ERROR(
                    f"""The following '{str(e).split("'")[-2]}' attribute\nPlease define it in .env file or /local/settings.dev.py file."""
                )
            )
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(
                    f"The root super user with following email '{settings.ROOT_USER_EMAIL}' address is already exists."
                )
            )
