import logging

from django.core import exceptions
from django.core.management.base import BaseCommand, CommandParser

from ...tests.fixtures import factories  # Import your factories module


class Command(BaseCommand):
    """
    Management command to create users of a given type and count.

    This command allows you to create users of different types (admin, student, teacher)
    with a specified count.

    Attributes:
        help (str): Help message for the command.
        logger (logging.Logger): Logger instance for logging messages.
        user_types (list): List of available user types.

    Methods:
        get_input_data(field, message, default=None): Override for customized data inputs or validation exceptions.
        add_arguments(parser): Add command-line arguments to the parser.
        handle(*args, **options): Handle the command execution.

    Usage Example:
        ```bash
        python manage.py generate_users --type student --count 5
        ```

    Note:
        This command prompts the user for the type of users to create and the count.
        It then utilizes factory functions to create users based on the provided inputs.

    Reference:
        - Django BaseCommand: https://docs.djangoproject.com/en/stable/howto/custom-management-commands/
    """

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
        """
        Add command-line arguments to the parser.

        Args:
            parser (CommandParser): The command parser instance.
        """
        parser.add_argument(
            "--type",
            type=str,
            choices=self.user_types,
            required=False,
            help="The type of user to create",
        )
        parser.add_argument("--count", type=int, default=1, help="The number of users to create")

    def handle(self, *args, **options):
        """
        Handle the command execution.

        Args:
            *args: Additional command-line arguments.
            **options: Additional command-line options.
        """
        # Prompt for user type.
        user_type = None
        while user_type is None:
            user_type = input("Enter the type of user to create (admin/student/teacher):")

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

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} {type} users"))
