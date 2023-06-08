from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.core.api.serializers import BaseModelSerializer, BaseSerializer

from ...models.models import OTPNumber, Student, Teacher
from ...utils import get_user_from_access_token
from ...validators import user_validate_password
from .. import exceptions, tokens
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


class LoginSerializer(BaseSerializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        attrs = super().validate(attrs)

        email = attrs["email"]
        password = attrs["password"]

        if email and password:
            # Check if the user is inactive
            user = get_user_model().objects.filter(email=email)
            if not user.exists():
                raise exceptions.UserNotExists()

            user = user.first()

            if not user.is_active:
                raise exceptions.UserNotActive()

            # Authenticate the user
            user = authenticate(
                request=self.context["request"],
                username=email,
                password=password,
            )

            if not user:
                raise exceptions.CredentialsNotValid()

            if not user.is_password_changed:
                raise exceptions.FirstTimePasswordError(user=user)

            attrs["user"] = user
        return attrs


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


class LogoutSerializer(BaseSerializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get("refresh")

        return attrs

    def create(self, validated_data):
        tokens.CustomRefreshToken(validated_data.get("refresh"), verify=True).blacklist()
        return True


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
        attrs["otp"] = OTPNumber.get_number()
        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        """Create an OTP number for the user"""

        instance = OTPNumber.objects.update_or_create(
            defaults={
                "number": validated_data.get("otp"),
                "user": validated_data.get("user"),
                "is_verified": False,
            }
        )
        return instance


class VerifyOTPNumberSerializer(BaseSerializer):
    otp = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        otp = attrs.get("otp", "")

        user = self.context["request"].user
        otp_instance = OTPNumber.objects.filter(user=user, number=otp)

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
        instance = OTPNumber.objects.get(user=self.context["request"].user, number=validated_data.get("otp"))

        # Set OTP number to be verified
        instance.is_verified = True
        instance.save()

        return True


class ChangePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)

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
        user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs

    def create(self, validated_data):
        """Update the user's password"""

        # Get user from the request
        user = self.context["request"].user

        # Set the new password for the user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Delete otp number for the user
        OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


class ForgetPasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a new password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)
    otp = serializers.CharField(min_length=1, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, passwords and otp number"""

        otp = attrs.get("otp", "")

        user = self.context["request"].user
        otp_instance = OTPNumber.objects.filter(user=user, number=otp)

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
        user_validate_password(attrs["new_password"], self.context["request"].user)

        return attrs

    def create(self, validated_data):
        """Update the user's password"""

        # Get user from the request
        user = self.context["request"].user

        # Set the new password for the user
        password = validated_data.get("new_password")
        user.set_password(password)

        # Delete otp number for the user
        OTPNumber.objects.filter(user=user).delete()

        user.save()

        return user


class FirstTimePasswordSerializer(BaseSerializer):
    """This serializer is responsible for setting a first time password of the user"""

    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirmed_password = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate(self, attrs: dict):
        """Validate the inserted data, validate passwords and otp number"""

        # Check if the two inserted password are similar
        if attrs["new_password"] != attrs["confirmed_password"]:
            raise exceptions.NotSimilarPasswords()

        # Validate the password if it meets all validator requirements
        user_validate_password(attrs["new_password"], self.context["request"].user)

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
