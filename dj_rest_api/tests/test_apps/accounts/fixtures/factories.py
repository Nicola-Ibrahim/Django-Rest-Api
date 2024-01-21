import factory
from factory import fuzzy

from ...models import Admin, Student, Teacher, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker(provider="first_name")
    last_name = factory.Faker(provider="last_name")

    # email will use first_name and last_name (the default or the one you provide)
    email = factory.LazyAttribute(lambda a: f"{a.first_name}.{a.last_name}@gmail.com".lower())

    # type = fuzzy.FuzzyChoice(choices=[x[0] for x in User.Type])

    phone_number = fuzzy.FuzzyInteger(25, 42)


class AdminUserFactory(UserFactory):
    class Meta:
        model = Admin

    type = "Admin"


class StudentUserFactory(UserFactory):
    class Meta:
        model = Student

    type = "Student"


class TeacherUserFactory(UserFactory):
    class Meta:
        model = Teacher

    type = "Teacher"
