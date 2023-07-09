import pytest

from .factories import UserFactory


@pytest.fixture
def user1(db):
    return UserFactory.create(first_name="Django", last_name="D")


@pytest.fixture
def users(db, request):
    return UserFactory.create_batch(3)
