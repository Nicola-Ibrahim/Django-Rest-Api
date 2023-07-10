import factory
from factory import fuzzy

from src.apps.accounts.models import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = factory.Faker(provider="first_name")
    last_name = factory.Faker(provider="last_name")

    # email will use first_name and last_name (the default or the one you provide)
    email = factory.LazyAttribute(
        lambda a: "{0}.{1}@gmail.com".format(a.first_name, a.last_name).lower()
    )

    # type = fuzzy.FuzzyChoice(choices=[x[0] for x in models.User.Type])

    phone_number = fuzzy.FuzzyInteger(25, 42)


class AdminUserFactory(UserFactory):
    type = "Admin"


class StudentUserFactory(UserFactory):
    type = "Student"


class TeacherUserFactory(UserFactory):
    type = "Teacher"
