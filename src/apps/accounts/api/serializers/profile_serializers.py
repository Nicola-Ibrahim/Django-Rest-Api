from src.apps.core.api.serializers import BaseModelSerializer

from ...models.profiles import StudentProfile, TeacherProfile


class TeacherProfileSerializer(BaseModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = [
            "name",
            "working_hours",
            "profit_percentage",
            "teacher",
        ]

        extra_kwargs = {
            "teacher": {"write_only": True},
        }


class StudentProfileSerializer(BaseModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ["first_name", "last_name", "student"]

        extra_kwargs = {
            "student": {"write_only": True},
        }
