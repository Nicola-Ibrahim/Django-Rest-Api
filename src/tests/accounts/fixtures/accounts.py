import pytest

from . import factories


@pytest.fixture
def one_user(db):
    return factories.UserFactory.create(first_name="Django", last_name="D")


@pytest.fixture
def one_teacher_user(db):
    return factories.TeacherUserFactory.create()


@pytest.fixture
def users(db, request):
    return factories.UserFactory.create_batch(3)
