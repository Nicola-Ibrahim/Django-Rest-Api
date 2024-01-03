from apps.accounts.models import Teacher
from django.db.signals import post_save
from hypothesis import HealthCheck, Verbosity, given, settings
from hypothesis.extra.django import from_model


class TestTeacherModel:
    @settings(
        suppress_health_check=[HealthCheck.function_scoped_fixture],
        verbosity=Verbosity.verbose,
        max_examples=10,
    )
    @given(teacher=from_model(Teacher))
    def test_post_save_teacher(self, teacher, mocker):
        # Mock the TeacherProfile model
        teacher_profile_mock_model = mocker.patch("apps.accounts.TeacherProfile")

        # Act
        post_save.send(Teacher, instance=teacher, created=True)

        # Assert
        teacher_profile_mock_model.objects.create.assert_called_once_with(teacher=teacher)
