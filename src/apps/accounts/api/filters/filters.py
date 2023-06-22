import django_filters.rest_framework as filters

from ...models.models import Student, Teacher, User


class UserFilter(filters.FilterSet):
    """A FilterSet subclass for filtering User model instances.

    This class defines the fields and lookup expressions that can be used to filter
    the User queryset by email and verification status.

    Attributes:
        Meta: A class that contains the model and fields information for the FilterSet.
    """

    class Meta:
        model = User
        fields = {
            "email": ["icontains"],  # Case-insensitive containment match
            "is_verified": ["exact"],  # Exact match
        }


class TeacherFilter(filters.FilterSet):
    """A FilterSet subclass for filtering Teacher model instances.

    This class defines the fields and lookup expressions that can be used to filter
    the Teacher queryset by warehouse profile name and section name.

    Attributes:
        Meta: A class that contains the model and fields information for the FilterSet.
    """

    class Meta:
        model = Teacher
        fields = {
            # "teacher_profile__name": [
            #     "icontains"
            # ],  # Case-insensitive containment match
            # "teacher_profile__sections__name": [
            #     "icontains",
            #     "exact",
            # ],  # Case-insensitive containment match or exact match
        }


class StudentFilter(filters.FilterSet):
    """A FilterSet subclass for filtering Student model instances.

    This class defines the fields and lookup expressions that can be used to filter
    the Student queryset by doctor profile first name, last name and subscription name.

    Attributes:
        Meta: A class that contains the model and fields information for the FilterSet.
    """

    class Meta:
        model = Student
        fields = {
            # "student_profile__first_name": [
            #     "icontains"
            # ],  # Case-insensitive containment match
            # "student_profile__last_name": [
            #     "icontains"
            # ],  # Case-insensitive containment match
            # "student_profile__subscription__name": ["icontains"],  # Case-insensitive containment match
        }
