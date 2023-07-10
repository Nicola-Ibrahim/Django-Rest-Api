import logging

from django.core.management.base import BaseCommand, CommandParser

from src.tests.accounts.fixtures import factories


class Command(BaseCommand):
    help = "Create users of a given type and count"
    logger = logging.getLogger(__name__)

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--type",
            type=str,
            choices=["admin", "student", "teacher"],
            required=True,
            help="The type of user to create",
        )
        parser.add_argument(
            "--count", type=int, default=1, help="The number of users to create"
        )

    def handle(self, *args, **options):
        type = options["type"]
        count = options["count"]
        print("Creating users...")

        factory_map = {
            "user": factories.UserFactory,
            "admin": factories.AdminUserFactory,
            "student": factories.StudentUserFactory,
            "teacher": factories.TeacherUserFactory,
        }

        user_factory = factory_map[type]

        user_factory.create_batch(count)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {count} {type} users")
        )
