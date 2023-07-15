from hypothesis import HealthCheck, Verbosity, given, settings
from hypothesis import strategies as st
from hypothesis.extra.django import from_model

from src.apps.accounts.models import models


class TestUserModel:
    user_strategy: st.SearchStrategy = from_model(models.User)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=40,
    )
    @given(user=user_strategy)
    def test_full_name(self, user):
        assert user.get_full_name() == f"{user.first_name} {user.last_name}".strip()

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=10,
    )
    @given(user=user_strategy)
    def test_set_password(self, user):
        user.set_password("Django pass")
        user.save()
        assert user.check_password("Django pass") is True


class TestAdminModel:
    user_admin_strategy: st.SearchStrategy = from_model(models.Admin)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=10,
    )
    @given(user=user_admin_strategy)
    def test_is_admin(self, user):
        assert isinstance(user, models.Admin)
        assert user.type == models.User.Type.ADMIN
        assert user.is_staff and user.is_superuser


class TestStudentModel:
    user_student_strategy: st.SearchStrategy = from_model(models.Student)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=10,
    )
    @given(user=user_student_strategy)
    def test_is_student(self, user):
        assert isinstance(user, models.Student)
        assert user.type == models.User.Type.STUDENT
        assert not (user.is_staff or user.is_superuser)


class TestTeacherModel:
    user_teacher_strategy: st.SearchStrategy = from_model(models.Teacher)

    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        deadline=2000,
        max_examples=10,
    )
    @given(user=user_teacher_strategy)
    def test_is_teacher(self, user):
        assert isinstance(user, models.Teacher)
        assert user.type == models.User.Type.TEACHER
        assert not (user.is_staff or user.is_superuser)
