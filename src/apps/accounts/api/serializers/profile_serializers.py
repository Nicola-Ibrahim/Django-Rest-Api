from src.apps.accounts.models import profiles
from src.apps.core.base_api.serializers import BaseModelSerializer


class AdminProfileSerializer(BaseModelSerializer):
    class Meta:
        model = profiles.AdminProfile
        fields = [
            "section",
        ]


class TeacherProfileSerializer(BaseModelSerializer):
    class Meta:
        model = profiles.TeacherProfile
        fields = [
            "num_courses",
        ]


class StudentProfileSerializer(BaseModelSerializer):
    class Meta:
        model = profiles.StudentProfile
        fields = [
            "study_hours",
        ]

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)
