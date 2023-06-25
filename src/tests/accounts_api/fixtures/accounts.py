import pytest
from model_bakery import baker


@pytest.fixture
def users(db):
    return baker.make("accounts.User", email="user1@hotmail.com")
