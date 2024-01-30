import pytest
from rest_framework import test
from rest_framework.test import force_authenticate

from . import factories


@pytest.fixture
def api_client():
    return test.APIClient()


@pytest.fixture
def authenticated_superuser_api_client(api_client):
    # Create a user
    user = factories.UserFactory.create(
        first_name="test_", last_name="authenticated_user", password="password123", is_superuser=True
    )

    access_token = user.get_tokens()["access"]

    # Create an API client and force authentication for the user
    api_client.force_authenticate(user=user, token=access_token)

    return api_client


@pytest.fixture
def authenticated_one_user_api_client(one_user):
    access_token = one_user.get_tokens()["access"]

    # Create an API client and force authentication for the user
    api_client.force_authenticate(user=one_user, token=access_token)

    return api_client
