from django.db.models.signals import post_save
from hypothesis import HealthCheck, Verbosity, given, settings
from hypothesis.extra.django import from_model

from src.apps.accounts.models import models


class TestTeacherModel:
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        max_examples=10,
    )
    @given(teacher=from_model(models.Teacher))
    def test_post_save_teacher(self, teacher, mocker):
        # Mock the TeacherProfile model
        teacher_profile_mock_model = mocker.patch("src.apps.accounts.models.profiles.TeacherProfile")

        # Act
        post_save.send(models.Teacher, instance=teacher, created=True)

        # Assert
        teacher_profile_mock_model.objects.create.assert_called_once_with(teacher=teacher)
