import pytest
from apps.accounts.exceptions import UserNotCreatedAPIException, UserNotFoundAPIException
from apps.accounts.models import Admin, Student, Teacher, User
from apps.accounts.services import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    get_user_details,
    get_user_sub_model,
    get_verification_url,
    update_user,
    verify_user_account,
)
from hypothesis import HealthCheck, Verbosity, given, settings
from hypothesis.extra.django import from_model


def test_create_user():
    data = {
        "first_name": "Django",
        "last_name": "D",
        "password": "another_secure_password",
        "email": "jane@example.com",
        "type": "teacher",
    }
    user = create_user(data)
    assert user.email == data["email"]


def test_create_user_exception():
    data = {
        "first_name": "Django",
        "last_name": "D",
        "password": "another_secure_password",
        "email": "jane@example.com",
        "type": "non-user-type",
    }
    with pytest.raises(UserNotCreatedAPIException):
        # This should raise an exception because the 'type' is not recognized
        create_user(data)


@settings(
    suppress_health_check=[HealthCheck.function_scoped_fixture],
    verbosity=Verbosity.verbose,
    max_examples=5,
)
@given(user=from_model(User))
def test_update_user(user):
    updated_data = {"first_name": "example_first_name"}
    updated_user = update_user(user.id, updated_data)
    assert updated_user.first_name == "example_first_name"


@settings(
    suppress_health_check=[HealthCheck.function_scoped_fixture],
    verbosity=Verbosity.verbose,
    max_examples=5,
)
@given(user=from_model(User))
def test_get_user_by_id(user):
    retrieved_user = get_user_by_id(user.id)
    assert retrieved_user.email == user.email


@settings(
    suppress_health_check=[HealthCheck.function_scoped_fixture],
    verbosity=Verbosity.verbose,
    max_examples=5,
)
@given(user=from_model(User))
def test_get_user_by_email(user):
    retrieved_user = get_user_by_email(user.email)
    assert retrieved_user.email == user.email


@settings(
    suppress_health_check=[HealthCheck.function_scoped_fixture],
    verbosity=Verbosity.verbose,
    max_examples=5,
)
@given(user=from_model(User))
def test_delete_user(user):
    delete_user(user.id)
    with pytest.raises(UserNotFoundAPIException):
        get_user_by_id(user.id)


def test_get_user_sub_model():
    assert get_user_sub_model("admin") == Admin
    assert get_user_sub_model("teacher") == Teacher
    assert get_user_sub_model("student") == Student
    assert get_user_sub_model("invalid") is None


def test_get_verification_url(one_user, rf):
    request = rf.get("/")
    verification_url = get_verification_url(request, one_user.email)
    assert "verify" in verification_url


def test_verify_user_account(one_user):
    verify_user_account(one_user)
    assert one_user.is_verified


def test_get_user_details(one_user):
    user_details = get_user_details(one_user)
    assert user_details["name"] == one_user.get_full_name()
    assert "tokens" in user_details
