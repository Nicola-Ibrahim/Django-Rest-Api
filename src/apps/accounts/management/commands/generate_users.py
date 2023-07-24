import logging

from django.core import exceptions
from django.core.management.base import BaseCommand, CommandParser

from src.tests.accounts.fixtures import factories


class Command(BaseCommand):
    help = "Create users of a given type and count"
    logger = logging.getLogger(__name__)
    user_types = ["admin", "student", "teacher"]

    def get_input_data(self, field, message, default=None):
        """
        Override this method if you want to customize data inputs or
        validation exceptions.
        """
        raw_value = input(message)
        if default and raw_value == "":
            raw_value = default
        try:
            val = field.clean(raw_value, None)
        except exceptions.ValidationError as e:
            self.stderr.write("Error: %s" % "; ".join(e.messages))
            val = None

        return val

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--type",
            type=str,
            choices=self.user_types,
            required=False,
            help="The type of user to create",
        )
        parser.add_argument(
            "--count", type=int, default=1, help="The number of users to create"
        )

    def handle(self, *args, **options):
        # Prompt for user type.
        user_type = None
        while user_type is None:
            user_type = input(
                "Enter the type of user to create (admin/student/teacher):"
            )

            if user_type not in self.user_types:
                self.stderr.write(f"Please select existed user types {self.user_types}")
                user_type = None
                continue

        # Prompt for count.
        count = None
        while count is None:
            count = input("Enter the number of users to create: ")

            if not count.isnumeric():
                self.stderr.write("Please enter valid number")
                count = None
                continue

        self.stdout.write(self.style.NOTICE("Creating users..."))

        factory_map = {
            "user": factories.UserFactory,
            "admin": factories.AdminUserFactory,
            "student": factories.StudentUserFactory,
            "teacher": factories.TeacherUserFactory,
        }

        user_factory = factory_map[user_type]

        user_factory.create_batch(int(count))

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} {type} users")
        )
