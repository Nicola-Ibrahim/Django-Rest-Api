from django.db import models
from django.utils.translation import gettext_lazy as _

from .models import Admin, Student, Teacher


class AdminProfile(models.Model):
    admin = models.OneToOneField(
        Admin,
        related_name="admin_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    section = models.CharField(_("section"), max_length=50)


class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student,
        related_name="student_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    study_hours = models.IntegerField(default=0)


class TeacherProfile(models.Model):
    teacher = models.OneToOneField(
        Teacher,
        related_name="teacher_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    num_courses = models.IntegerField(default=0)
    is_idle = models.BooleanField(default=False)
