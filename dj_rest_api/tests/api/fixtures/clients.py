import pytest
from apps.accounts.models.factory import UserFactory
from apps.authentication.services import get_tokens_for_user
from rest_framework import test


@pytest.fixture
def api_client():
    return test.APIClient()


@pytest.fixture
def authenticated_superuser_api_client(api_client):
    # Create a user
    user = UserFactory.create(
        first_name="test_", last_name="authenticated_user", password="password123", is_superuser=True
    )

    access_token = get_tokens_for_user(user)["access"]

    # Create an API client and force authentication for the user
    api_client.force_authenticate(user=user, token=access_token)

    return api_client


@pytest.fixture
def authenticated_one_user_api_client(one_user):
    access_token = get_tokens_for_user(one_user)["access"]

    # Create an API client and force authentication for the user
    api_client.force_authenticate(user=one_user, token=access_token)

    return api_client
