from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from src.apps.core.api.serializers import BaseModelSerializer, BaseSerializer

from ...models.models import Student, Teacher
from ..utils import get_user_from_access_token
from .profile_serializers import StudentProfileSerializer, TeacherProfileSerializer


class UserSerializer(BaseModelSerializer):
    """Serializer is responsible for creation and updating an instance"""

    manager_name = serializers.ReadOnlyField(source="manager.admin_profile.first_name")

    groups = serializers.ReadOnlyField(source="groups.all.values")

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    # url = serializers.HyperlinkedIdentityField(
    #     view_name="auth:details", read_only=True
    # )

    class Meta:
        model = get_user_model()
        ordering = ["-id"]
        profile_related_name = ""
        profile_relation_field = ""
        profile_serializer = None

        fields = [
            "id",
            "email",
            "password",
            "confirm_password",
            "phone_number",
            "state",
            "city",
            "street",
            "zipcode",
            "identification",
            "type",
            "manager_name",
            "is_staff",
            "is_active",
            "is_verified",
            "groups",
            "manager",
        ]

        read_only_fields = ("is_active", "is_staff")
        extra_kwargs = {
            "manager": {"write_only": True},
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }

    def validate(self, attrs):
        """Override validate method to ensure user entered the same password values

        Args:
            attrs (list): the user data

        Raises:
            serializers.ValidationError: raise an error when the two inserted passwords are not similar

        Returns:
            user data: the user data after validation
        """
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        # Get user profile data
        profile_data = validated_data.pop("profile")

        # Update main data of the user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update profile data of the user
        profile = instance.teacher_profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)

        # Save instance
        profile.save()
        instance.save()

        return instance

    def create(self, validated_data: dict[str, str]):
        """Override the create method create a new user with the profile data

        Args:
            validated_data (dict[str, str]): validated data by the serializer

        Returns:
            User: a new inserted user
        """

        # Get the profile data of the user
        user_profile_data = validated_data.pop(self.Meta.profile_related_name)

        # Remove confirm_password field value from the inserted data
        validated_data.pop("confirm_password")

        # Create a new teacher user without saving
        user = super().create(validated_data)

        # Create profile data for the user
        user_profile_data[self.Meta.profile_relation_field] = user.id
        profile_serializer = self.Meta.profile_serializer(data=user_profile_data)
        profile_serializer.is_valid(raise_exception=True)

        # Save the user's profile
        profile_serializer.save()

        # Save the user
        user.save()

        return user


class TeacherUserSerializer(UserSerializer):
    """
    A subclass of UserSerializer for handling teacher users
    """

    profile = TeacherProfileSerializer(source="teacher_profile")

    class Meta(UserSerializer.Meta):
        model = Teacher
        fields = UserSerializer.Meta.fields + ["profile"]
        profile_related_name = "teacher_profile"
        profile_relation_field = "teacher"
        profile_serializer = TeacherProfileSerializer


class StudentUserSerializer(UserSerializer):
    profile = StudentProfileSerializer(source="student_profile")

    class Meta(UserSerializer.Meta):
        model = Student
        fields = UserSerializer.Meta.fields + ["profile"]
        profile_related_name = "student_profile"
        profile_relation_field = "student"
        profile_serializer = StudentProfileSerializer


class AccountVerificationSerializer(BaseSerializer):
    token = serializers.CharField()

    def validate(self, attrs):
        # Get the use id from the payload
        user = get_user_from_access_token(attrs.get("token"))

        # Add the user instance to validated data
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """Update the user's password"""
        user = validated_data.get("user")

        # Check if the user is not verified
        if not user.is_verified:
            user.is_verified = True
            user.save()

        return user
