from django.db import models

from .models import Admin, Student, Teacher
from .validators import validate_name


class AdminProfile(models.Model):
    admin = models.OneToOneField(Admin, related_name="admin_profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student,
        related_name="student_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=200,
        validators=[validate_name],
    )
    working_hours = models.FloatField()
    profit_percentage = models.FloatField()

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class TeacherProfile(models.Model):
    teacher = models.OneToOneField(
        Teacher,
        related_name="teacher_profile",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=200, validators=[validate_name])
    last_name = models.CharField(max_length=200, validators=[validate_name])
    distance = models.FloatField(max_length=200)
    duration = models.FloatField()
    profit_percentage = models.FloatField()
    is_idle = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name
