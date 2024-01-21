import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import CustomUserManager, ProxyUserManger
from .signals import user_proxy_model_instance_saved
from .validators import validate_name


class User(AbstractUser):
    objects = CustomUserManager()

    class Type(models.TextChoices):
        STUDENT = "student", _("Student")
        TEACHER = "teacher", _("Teacher")
        ADMIN = "admin", _("Admin")

    # Set username to none
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True, validators=[validate_email])
    first_name = models.CharField(_("first name"), max_length=150, blank=True, validators=[validate_name])
    last_name = models.CharField(_("last name"), max_length=150, blank=True, validators=[validate_name])
    phone_number = models.IntegerField(_("phone_number"), null=True, blank=True)
    state = models.CharField(_("state"), max_length=50, null=True, blank=True)
    city = models.CharField(_("city"), max_length=50, null=True, blank=True)
    street = models.CharField(_("street"), max_length=50, null=True, blank=True)
    zipcode = models.IntegerField(_("zipcode"), null=True, blank=True)
    identification = models.IntegerField(_("identification"), null=True, blank=True)
    type = models.CharField(
        _("user type"),
        max_length=50,
        choices=Type.choices,
        blank=True,
        default=Type.ADMIN,
    )
    is_verified = models.BooleanField(_("verified"), default=False)
    is_password_changed = models.BooleanField(_("is_password_changed"), default=False)

    manager = models.ForeignKey("Admin", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.email

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        print(refresh)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def get_user_details(self):
        return {
            "name": self.get_full_name(),
            "tokens": self.get_tokens(),
        }


class Teacher(User):
    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.TEACHER)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.TEACHER
        super().save(*args, **kwargs)

        # Send and trigger the signal
        user_proxy_model_instance_saved.send(sender=self.__class__, instance=self, created=True)


class Student(User):
    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.STUDENT)

    def save(self, *args, **kwargs) -> None:
        self.type = User.Type.STUDENT
        super().save(*args, **kwargs)

        # Send and trigger the signal
        user_proxy_model_instance_saved.send(sender=self.__class__, instance=self, created=True)


class Admin(User):
    class Meta:
        proxy = True

    objects = ProxyUserManger(User.Type.ADMIN)

    def save(self, *args, **kwargs) -> None:
        self.is_staff = True
        self.is_superuser = True
        self.type = User.Type.ADMIN
        super().save(*args, **kwargs)

        # Send and trigger the signal
        user_proxy_model_instance_saved.send(sender=self.__class__, instance=self, created=True)


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
