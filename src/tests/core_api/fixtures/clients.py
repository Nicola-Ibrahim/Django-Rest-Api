import pytest
from rest_framework import test


@pytest.fixture
def api_client():
    return test.APIClient()
