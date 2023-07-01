from src.apps.accounts.models import profiles
from src.apps.core.base_api.serializers import BaseModelSerializer


class AdminProfileSerializer(BaseModelSerializer):
    class Meta:
        model = profiles.AdminProfile
        fields = [
            "first_name",
            "last_name",
        ]

        extra_kwargs = {
            "teacher": {"write_only": True},
        }


class TeacherProfileSerializer(BaseModelSerializer):
    class Meta:
        model = profiles.TeacherProfile
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
        model = profiles.StudentProfile
        fields = [
            "first_name",
            "last_name",
            "study_hours",
            "student",
        ]

        extra_kwargs = {
            "student": {"write_only": True},
        }
