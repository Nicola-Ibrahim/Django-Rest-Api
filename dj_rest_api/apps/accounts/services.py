from abc import ABC, abstractmethod
from typing import Any

from django.db import transaction
from django.db.models import signals

from . import models
from .models.receivers import create_admin_profile, create_student_profile, create_teacher_profile, signal_reconnect


class UserAndProfileBuilder(ABC):
    def __init__(self):
        self.user_data = {}
        self.profile_data = {}

    @abstractmethod
    def set_user_data(self, user_data: dict[str, Any]):
        raise NotImplementedError("set_user_data method not implemented")

    @abstractmethod
    def set_profile_data(self, profile_data: dict[str, Any]):
        raise NotImplementedError("set_profile_data method not implemented")

    @abstractmethod
    def set_user_id(self, user_id: Any):
        raise NotImplementedError("set_user_id method not implemented")

    def create_user(self) -> models.User:
        raise NotImplementedError("create_user method not implemented")

    @abstractmethod
    def create_profile(self) -> models.TeacherProfile:
        raise NotImplementedError("create_profile method not implemented")

    @classmethod
    def construct(cls, user_data: dict[str, Any]) -> bool:
        builder = cls()

        with transaction.atomic():
            profile_data = user_data.pop("profile")

            builder.set_user_data(user_data)
            user = builder.create_user()

            builder.set_user_id(user.id)
            builder.set_profile_data(profile_data)
            builder.create_profile()


class StudentUserAndProfileBuilder(UserAndProfileBuilder):
    profile_relation_field = "student"

    def set_user_data(self, user_data: dict[str, Any]):
        self.user_data = user_data

    def set_profile_data(self, profile_data: dict[str, Any]):
        self.profile_data = profile_data

    def set_user_id(self, user_id: Any):
        self.profile_data[self.profile_relation_field] = user_id

    @signal_reconnect(  # Decorate create method to disconnect and reconnect post_save signal for creating a profile
        signal=signals.post_save,
        sender=models.Student,
        receiver=create_student_profile,
        dispatch_uid="student_post_save",
    )
    def create_user(self) -> models.User:
        user = models.Student.objects.create_user(**self.user_data)
        return user

    def create_profile(self) -> models.TeacherProfile:
        profile = models.StudentProfile.objects.create(**self.profile_data)
        return profile


class TeacherUserAndProfileBuilder(UserAndProfileBuilder):
    profile_relation_field = "teacher"

    def set_user_data(self, user_data: dict[str, Any]):
        self.user_data = user_data

    def set_profile_data(self, profile_data: dict[str, Any]):
        self.profile_data = profile_data

    def set_user_id(self, user_id: Any):
        self.profile_data[self.profile_relation_field] = user_id

    @signal_reconnect(  # Decorate create method to disconnect and reconnect post_save signal for creating a profile
        signal=signals.post_save,
        sender=models.Teacher,
        receiver=create_teacher_profile,
        dispatch_uid="teacher_post_save",
    )
    def create_user(self) -> models.User:
        user = models.Teacher.objects.create_user(**self.user_data)
        return user

    def create_profile(self) -> models.TeacherProfile:
        profile = models.TeacherProfile.objects.create(**self.profile_data)
        return profile


class AdminUserAndProfileBuilder(UserAndProfileBuilder):
    profile_relation_field = "admin"

    def set_user_data(self, user_data: dict[str, Any]):
        self.user_data = user_data

    def set_profile_data(self, profile_data: dict[str, Any]):
        self.profile_data = profile_data

    def set_user_id(self, user_id: Any):
        self.profile_data[self.profile_relation_field] = user_id

    @signal_reconnect(  # Decorate create method to disconnect and reconnect post_save signal for creating a profile
        signal=signals.post_save,
        sender=models.Teacher,
        receiver=create_admin_profile,
        dispatch_uid="admin_post_save",
    )
    def create_user(self) -> models.User:
        user = models.Admin.objects.create_user(**self.user_data)
        return user

    def create_profile(self) -> models.TeacherProfile:
        profile = models.AdminProfile.objects.create(**self.profile_data)
        return profile
