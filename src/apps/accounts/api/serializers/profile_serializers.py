from src.apps.accounts.models.profiles import StudentProfile, TeacherProfile
from src.apps.core.base_api.serializers import BaseModelSerializer


class TeacherProfileSerializer(BaseModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = [
            "first_name",
            "last_name",
            "num_courses",
            "teacher",
        ]

        extra_kwargs = {
            "teacher": {"write_only": True},
        }


class StudentProfileSerializer(BaseModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "first_name",
            "last_name",
            "study_hours",
            "student",
        ]

        extra_kwargs = {
            "student": {"write_only": True},
        }
