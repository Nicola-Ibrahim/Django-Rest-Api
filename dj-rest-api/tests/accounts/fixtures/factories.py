import factory
from apps.accounts.models import models
from factory import fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = factory.Faker(provider="first_name")
    last_name = factory.Faker(provider="last_name")

    # email will use first_name and last_name (the default or the one you provide)
    email = factory.LazyAttribute(lambda a: f"{a.first_name}.{a.last_name}@gmail.com".lower())

    # type = fuzzy.FuzzyChoice(choices=[x[0] for x in models.User.Type])

    phone_number = fuzzy.FuzzyInteger(25, 42)


class AdminUserFactory(UserFactory):
    class Meta:
        model = models.Admin

    type = "Admin"


class StudentUserFactory(UserFactory):
    class Meta:
        model = models.Student

    type = "Student"


class TeacherUserFactory(UserFactory):
    class Meta:
        model = models.Teacher

    type = "Teacher"
