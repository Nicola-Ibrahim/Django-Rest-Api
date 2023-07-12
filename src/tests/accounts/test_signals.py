import pytest
from django.db.models.signals import post_save

from src.apps.accounts.models import models


class TestTeacherModel:
    def test_post_save(self, one_teacher_user, mocker):
        # Mock the TeacherProfile model
        teacher_profile_mock_model = mocker.patch(
            "src.apps.accounts.models.profiles.TeacherProfile"
        )
        post_save.send(models.Teacher, instance=one_teacher_user, created=True)

        # Assert that the create method of the TeacherProfile manager was called once with the teacher instance as an argument
        teacher_profile_mock_model.objects.create.assert_called_once_with(
            teacher=one_teacher_user
        )
