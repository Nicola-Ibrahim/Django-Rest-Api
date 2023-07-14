import pytest

from . import factories


@pytest.fixture
def one_user(db):
    return factories.UserFactory.create(first_name="Django", last_name="D")


@pytest.fixture(autouse=True)
def one_admin_user(db):
    return factories.AdminUserFactory.create()


@pytest.fixture
def one_teacher_user(db):
    return factories.TeacherUserFactory.create()


@pytest.fixture
def one_student_user(db):
    return factories.StudentUserFactory.create()


@pytest.fixture
def users(db, request):
    return factories.UserFactory.create_batch(3)
