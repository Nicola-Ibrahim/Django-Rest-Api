from unittest import mock

import pytest
from rest_framework.permissions import IsAuthenticated

from . import factories


@pytest.fixture
def one_user(db):
    """
    Fixture to create and return a single user with specific details.

    Args:
        db: Django database fixture.

    Returns:
        User: A user instance with first name "Django" and last name "D".
    """
    return factories.UserFactory.create(first_name="Django", last_name="D")


@pytest.fixture(autouse=True)
def one_admin_user(db):
    """
    Fixture to create and return a single admin user.

    Args:
        db: Django database fixture.

    Returns:
        AdminUser: A created admin user instance.
    """
    return factories.AdminUserFactory.create()


@pytest.fixture
def one_teacher_user(db):
    """
    Fixture to create and return a single teacher user.

    Args:
        db: Django database fixture.

    Returns:
        TeacherUser: A created teacher user instance.
    """
    return factories.TeacherUserFactory.create()


@pytest.fixture
def one_student_user(db):
    """
    Fixture to create and return a single student user.

    Args:
        db: Django database fixture.

    Returns:
        StudentUser: A created student user instance.
    """
    return factories.StudentUserFactory.create()


@pytest.fixture
def users(db):
    """
    Fixture to create and return a batch of three user instances.

    Args:
        db: Django database fixture.

    Returns:
        List[User]: A list containing three user instances.
    """
    return factories.UserFactory.create_batch(3)


@pytest.fixture(scope="session", autouse=True)
def mock_views_permissions():
    # little util I use for testing for DRY when patching multiple objects
    patch_perm = lambda perm: mock.patch.multiple(  # noqa:E731
        perm,
        has_permission=mock.Mock(return_value=True),
        has_object_permission=mock.Mock(return_value=True),
    )
    with (
        patch_perm(IsAuthenticated),
        # ...add other permissions you may have below
    ):
        yield
