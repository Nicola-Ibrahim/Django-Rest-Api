from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from lib.api.serializers import BaseModelSerializer, BaseSerializer
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .. import models
from . import exceptions


class AdminProfileSerializer(BaseModelSerializer):
    class Meta:
        model = models.AdminProfile
        fields = [
            "section",
        ]


class TeacherProfileSerializer(BaseModelSerializer):
    class Meta:
        model = models.TeacherProfile
        fields = [
            "num_courses",
        ]


class StudentProfileSerializer(BaseModelSerializer):
    class Meta:
        model = models.StudentProfile
        fields = [
            "study_hours",
        ]


class UserListSerializer(BaseModelSerializer):
    """Serializer for listing user details."""

    url = serializers.HyperlinkedIdentityField(
        view_name="api:accounts-api:user-details-update-destroy",
        lookup_field="id",
        read_only=True,
    )

    manager = serializers.SlugRelatedField(many=False, slug_field="email", read_only=True)

    # Use SlugRelatedField for only accepting the name of the group (No need for other info)
    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        many=False,
        slug_field="name",
        allow_null=True,
    )

    profile = serializers.HyperlinkedIdentityField(
        view_name="api:accounts-api:profile-details-update",
        lookup_field="id",
        read_only=True,
    )

    class Meta:
        model = get_user_model()

        fields = [
            "id",
            "url",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_verified",
            "is_superuser",
            "groups",
            "manager",
            "type",
            "profile",
        ]


class UserDetailsSerializer(BaseModelSerializer):
    """An abstract serializer for managing User model"""

    # Use SlugRelatedField for only accepting the name of the group (No need for other info)
    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        many=False,
        slug_field="name",
        allow_null=True,
    )

    profile = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()

        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_verified",
            "is_superuser",
            "groups",
            "profile",
        ]

    def get_profile(self, obj):
        """Get the appropriate profile data for different user type"""
        profiles_serializers = {
            "admin": AdminProfileSerializer(instance=models.AdminProfile.objects.filter(admin=obj.id).first()),
            "teacher": TeacherProfileSerializer(instance=models.TeacherProfile.objects.filter(teacher=obj.id).first()),
            "student": StudentProfileSerializer(instance=models.StudentProfile.objects.filter(student=obj.id).first()),
        }
        serializer = profiles_serializers.get(obj.type.lower(), None)
        return serializer.data


class UserCreateSerializer(BaseModelSerializer):
    """Template base serializer is responsible for validation the data for a new user"""

    password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = models.User

        fields = [
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "phone_number",
            "state",
            "city",
            "street",
            "zipcode",
            "identification",
            "type",
        ]

    @property
    def data(self):
        ret = super().data
        ret.pop("confirm_password")
        return ReturnDict(ret, serializer=self)

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
            raise exceptions.NotSimilarPasswordsAPIException()

        return attrs


class UserUpdateSerializer(BaseModelSerializer):
    """Serializer is responsible for creation and updating a user"""

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        ordering = ["-id"]
        profile_related_name = ""
        profile_relation_field = ""
        profile_serializer = None

        fields = [
            "first_name",
            "last_name",
            "password",
            "confirm_password",
            "phone_number",
            "state",
            "city",
            "street",
            "zipcode",
            "identification",
        ]

    def update(self, instance, validated_data):
        """Update an existence user with the profile data

        Args:
            validated_data (dict[str, str]): validated data by the serializer

        Returns:
            User: a new inserted user
        """
        user = instance

        # Get user profile data
        profile_data = validated_data.pop(self.Meta.profile_related_name)

        # Update main data of the user
        for attr, value in validated_data.items():
            setattr(user, attr, value)

        # Update profile data of the user
        profile_instance = getattr(user, self.Meta.profile_related_name)
        profile_serializer = self.Meta.profile_serializer(instance=profile_instance, data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        user.save()

        return user


class AdminUserUpdateSerializer(UserUpdateSerializer):
    """
    A subclass of UserUpdateSerializer for handling teacher users
    """

    profile = AdminProfileSerializer(source="admin_profile")

    class Meta(UserUpdateSerializer.Meta):
        model = models.Admin
        fields = UserUpdateSerializer.Meta.fields + ["profile"]
        profile_related_name = "admin_profile"
        profile_relation_field = "admin"
        profile_serializer = AdminProfileSerializer


class TeacherUserUpdateSerializer(UserUpdateSerializer):
    """
    A subclass of UserUpdateSerializer for handling teacher users
    """

    profile = TeacherProfileSerializer(source="teacher_profile")

    class Meta(UserUpdateSerializer.Meta):
        model = models.Teacher
        fields = UserUpdateSerializer.Meta.fields + ["profile"]
        profile_related_name = "teacher_profile"
        profile_relation_field = "teacher"
        profile_serializer = TeacherProfileSerializer


class StudentUserUpdateSerializer(UserUpdateSerializer):
    profile = StudentProfileSerializer(source="student_profile")

    class Meta(UserUpdateSerializer.Meta):
        model = models.Student
        fields = UserUpdateSerializer.Meta.fields + ["profile"]
        profile_related_name = "student_profile"
        profile_relation_field = "student"
        profile_serializer = StudentProfileSerializer


class AccountVerificationSerializer(BaseSerializer):
    token = serializers.CharField()

    def validate(self, attrs):
        # Get the use id from the payload
        user = utils.get_user_from_access_token(attrs.get("token"))

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
