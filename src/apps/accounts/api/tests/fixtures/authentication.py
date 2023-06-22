import pytest
from model_bakery import baker


@pytest.fixture
def users(db):
    return baker.make("accounts.User", balance=2000)
