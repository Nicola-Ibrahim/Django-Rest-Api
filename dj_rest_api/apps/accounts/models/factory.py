import factory
from django.utils.translation import gettext_lazy as _
from factory import fuzzy

from .users import Admin, Student, Teacher, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name}.{obj.last_name}@gmail.com".lower())
    phone_number = fuzzy.FuzzyInteger(25, 42)
    state = factory.Faker("state")
    city = factory.Faker("city")
    zipcode = fuzzy.FuzzyInteger(10000, 99999)
    identification = fuzzy.FuzzyInteger(100000, 999999)
    type = fuzzy.FuzzyChoice(choices=[User.Type.STUDENT, User.Type.TEACHER, User.Type.ADMIN])
    is_verified = factory.Faker("boolean")
    is_password_changed = factory.Faker("boolean")

    @factory.post_generation
    def set_password(self, create, extracted, **kwargs):
        # Set a default password for the user
        self.set_password("password")
        self.save()


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
