from src.apps.core.base_api.serializers import BaseModelSerializer

from ...models import profiles


class AdminProfileSerializer(BaseModelSerializer):
    class Meta:
        model = profiles.AdminProfile
        fields = [
            "admin",
            "section",
        ]

        extra_kwargs = {
            "admin": {"write_only": True},
        }


class TeacherProfileSerializer(BaseModelSerializer):
    class Meta:
        model = profiles.TeacherProfile
        fields = [
            "teacher",
            "num_courses",
        ]

        extra_kwargs = {
            "teacher": {"write_only": True},
        }


class StudentProfileSerializer(BaseModelSerializer):
    class Meta:
        model = profiles.StudentProfile
        fields = [
            "student",
            "study_hours",
        ]

        extra_kwargs = {
            "student": {"write_only": True},
        }
