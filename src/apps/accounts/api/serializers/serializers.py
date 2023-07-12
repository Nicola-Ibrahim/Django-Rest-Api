from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.db.models import signals
from rest_framework import serializers

from src.apps.accounts.api import exceptions
from src.apps.accounts.models import models, profiles, utils, validators
from src.apps.accounts.models.signals import (
    create_student_profile,
    create_teacher_profile,
    signal_wrapper,
)
from src.apps.core.base_api.serializers import BaseModelSerializer, BaseSerializer

from . import profile_serializers


class UserListSerializer(BaseModelSerializer):
    """An abstract serializer for managing User model"""

    url = serializers.HyperlinkedIdentityField(
        view_name="accounts-api:user-details-update-destroy",
        lookup_field="id",
        read_only=True,
    )

    manager = serializers.SlugRelatedField(
        many=False, slug_field="email", read_only=True
    )

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

    def get_profile(self, obj):
        """Get the appropriate profile data for different user type"""
        profiles_serializers = {
            "admin": profile_serializers.AdminProfileSerializer(
                instance=profiles.AdminProfile.objects.filter(admin=obj.id).first()
            ),
            "teacher": profile_serializers.TeacherProfileSerializer(
                instance=profiles.TeacherProfile.objects.filter(teacher=obj.id).first()
            ),
            "student": profile_serializers.StudentProfileSerializer(
                instance=profiles.StudentProfile.objects.filter(student=obj.id).first()
            ),
        }
        serializer = profiles_serializers.get(obj.type.lower(), None)
        return serializer.data


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
            "admin": profile_serializers.AdminProfileSerializer(
                instance=profiles.AdminProfile.objects.filter(admin=obj.id).first()
            ),
            "teacher": profile_serializers.TeacherProfileSerializer(
                instance=profiles.TeacherProfile.objects.filter(teacher=obj.id).first()
            ),
            "student": profile_serializers.StudentProfileSerializer(
                instance=profiles.StudentProfile.objects.filter(student=obj.id).first()
            ),
        }
        serializer = profiles_serializers.get(obj.type.lower(), None)
        return serializer.data


class UserCreateSerializer(BaseModelSerializer):
    """Template base serializer is responsible for creation and updating a user"""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = None
        ordering = ["-id"]
        profile_related_name = ""
        profile_relation_field = ""
        profile_serializer = None

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
        ]

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
            raise exceptions.NotSimilarPasswords()

        return attrs

    def create(self, validated_data: dict[str, str]):
        """Create a new user with the profile data

        Args:
            validated_data (dict[str, str]): validated data by the serializer

        Returns:
            User: a new inserted user
        """
        # Get the profile data of the user
        user_profile_data = validated_data.pop(self.Meta.profile_related_name)  # type: ignore # noqa:F841

        # Remove confirm_password field value from the inserted data
        validated_data.pop("confirm_password")

        # Create a new user
        user = self.Meta.model.objects.create_user(**validated_data)

        # Create profile data for the user
        user_profile_data[self.Meta.profile_relation_field] = user.id
        profile_serializer = self.Meta.profile_serializer(data=user_profile_data)
        profile_serializer.is_valid(raise_exception=True)

        # Save the user's profile
        profile_serializer.save()

        return user


class AdminUserCreateSerializer(UserCreateSerializer):
    """
    A subclass of UserCreateSerializer for handling teacher users
    """

    profile = profile_serializers.AdminProfileSerializer(source="admin_profile")

    class Meta(UserCreateSerializer.Meta):
        model = models.Admin
        fields = UserCreateSerializer.Meta.fields + ["profile"]
        profile_related_name = "admin_profile"
        profile_relation_field = "admin"
        profile_serializer = profile_serializers.AdminProfileSerializer

    # Decorate create method to disconnect post_save signal for creating a profile
    @signal_wrapper(
        signal=signals.post_save,
        sender=models.Teacher,
        receiver=create_teacher_profile,
        dispatch_uid="admin_post_save",
    )
    def create(self, validated_data: dict[str, str]):
        return super().create(validated_data)


class TeacherUserCreateSerializer(UserCreateSerializer):
    """
    A subclass of UserCreateSerializer for handling teacher users
    """

    profile = profile_serializers.TeacherProfileSerializer(source="teacher_profile")

    class Meta(UserCreateSerializer.Meta):
        model = models.Teacher
        fields = UserCreateSerializer.Meta.fields + ["profile"]
        profile_related_name = "teacher_profile"
        profile_relation_field = "teacher"
        profile_serializer = profile_serializers.TeacherProfileSerializer

    # Decorate create method to disconnect post_save signal for creating a profile
    @signal_wrapper(
        signal=signals.post_save,
        sender=models.Teacher,
        receiver=create_teacher_profile,
        dispatch_uid="teacher_post_save",
    )
    def create(self, validated_data: dict[str, str]):
        return super().create(validated_data)


class StudentUserCreateSerializer(UserCreateSerializer):
    profile = profile_serializers.StudentProfileSerializer(source="student_profile")

    class Meta(UserCreateSerializer.Meta):
        model = models.Student
        fields = UserCreateSerializer.Meta.fields + ["profile"]
        profile_related_name = "student_profile"
        profile_relation_field = "student"
        profile_serializer = profile_serializers.StudentProfileSerializer

    # Decorate create method to disconnect post_save signal for creating a profile
    @signal_wrapper(
        signal=signals.post_save,
        sender=models.Student,
        receiver=create_student_profile,
        dispatch_uid="student_post_save",
    )
    def create(self, validated_data: dict[str, str]):
        return super().create(validated_data)


class UserUpdateSerializer(BaseModelSerializer):
    """Serializer is responsible for creation and updating a user"""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = None
        ordering = ["-id"]
        profile_related_name = ""
        profile_relation_field = ""
        profile_serializer = None

        fields = [
            "first_name",
            "last_name",
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
        profile_serializer = self.Meta.profile_serializer(
            instance=profile_instance, data=profile_data
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

        user.save()

        return user


class AdminUserUpdateSerializer(UserUpdateSerializer):
    """
    A subclass of UserUpdateSerializer for handling teacher users
    """

    profile = profile_serializers.AdminProfileSerializer(source="admin_profile")

    class Meta(UserUpdateSerializer.Meta):
        model = models.Admin
        fields = UserUpdateSerializer.Meta.fields + ["profile"]
        profile_related_name = "admin_profile"
        profile_relation_field = "admin"
        profile_serializer = profile_serializers.AdminProfileSerializer


class TeacherUserUpdateSerializer(UserUpdateSerializer):
    """
    A subclass of UserUpdateSerializer for handling teacher users
    """

    profile = profile_serializers.TeacherProfileSerializer(source="teacher_profile")

    class Meta(UserUpdateSerializer.Meta):
        model = models.Teacher
        fields = UserUpdateSerializer.Meta.fields + ["profile"]
        profile_related_name = "teacher_profile"
        profile_relation_field = "teacher"
        profile_serializer = profile_serializers.TeacherProfileSerializer


class StudentUserUpdateSerializer(UserUpdateSerializer):
    profile = profile_serializers.StudentProfileSerializer(source="student_profile")

    class Meta(UserUpdateSerializer.Meta):
        model = models.Student
        fields = UserUpdateSerializer.Meta.fields + ["profile"]
        profile_related_name = "student_profile"
        profile_relation_field = "student"
        profile_serializer = profile_serializers.StudentProfileSerializer


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


class ForgetPasswordRequestSerializer(BaseSerializer):
    """This serializer is responsible for creating a number for the user who requested password reset"""

    email = serializers.EmailField(min_length=2, required=True)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email", "")

        # Check the user existence
        user = get_user_model().objects.filter(email=email)

        if not user.exists():
            raise exceptions.UserNotExists()

        user = user.first()

        attrs["email"] = email
        attrs["otp"] = models.OTPNumber.get_number()
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """Create an OTP number for the user"""

        otp_instance = models.OTPNumber.objects.update_or_create(
            defaults={
                "number": validated_data.get("otp"),
                "user": validated_data.get("user"),
                "is_verified": False,
            }
        )
        return otp_instance


class VerifyOTPNumberSerializer(BaseSerializer):
    otp = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        otp = attrs.get("otp", "")

        user = self.context["request"].user
        otp_instance = models.OTPNumber.objects.filter(user=user, number=otp)

        # Check if the OTP number does not exists
        if not otp_instance.exists():
            raise exceptions.WrongOTP()

        # If the OTP number is expired
        if not otp_instance.first().check_num(otp):
            raise exceptions.OTPExpired()

        return attrs

    def create(self, validated_data):
        """Update the is_verified field after validate the otp number assigned to user"""

        # Get the OTP number of the user
        instance = models.OTPNumber.objects.get(
            user=self.context["request"].user, number=validated_data.get("otp")
        )

        # Set OTP number to be verified
        instance.is_verified = True
        instance.save()

        return True


class ChangePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate(self, attrs: dict):
        """Validate the inserted data, passwords and otp number"""

        # Validate the if the old password is correct for the request user
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise exceptions.WrongPassword()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        validators.user_validate_password(
            attrs["new_password"], self.context["request"].user
        )

        return attrs

    def create(self, validated_data):
        """Update the user's password"""

        # Get user from the request
        user = self.context["request"].user

        # Set the new password for the user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Delete otp number for the user
        models.OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


class ForgetPasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )
    otp = serializers.CharField(min_length=1, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, passwords and otp number"""

        otp = attrs.get("otp", "")

        user = self.context["request"].user
        otp_instance = models.OTPNumber.objects.filter(user=user, number=otp)

        # Check if the OTP number does not exists
        if not otp_instance.exists():
            raise exceptions.WrongOTP()

        # Check if the user OTP number is verified
        if not otp_instance.first().is_verified:
            raise exceptions.OTPNotVerified()

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        validators.user_validate_password(
            attrs["new_password"], self.context["request"].user
        )

        return attrs

    def create(self, validated_data):
        """Update the user's password"""

        # Get user from the request
        user = self.context["request"].user

        # Set the new password for the user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Delete otp number for the user
        models.OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


class FirstTimePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a first time password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def validate(self, attrs: dict):
        """Validate the inserted data, validate passwords and otp number"""

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        validators.user_validate_password(
            attrs["new_password"], self.context["request"].user
        )

        return attrs

    def create(self, validated_data):
        """Update the user's password"""
        user = self.context["request"].user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Set password changed to true
        if not user.is_password_changed:
            user.is_password_changed = True
            user.save()

        user.save()
        return user
