from typing import Any

from apps.accounts import models as accounts_models
from apps.authentication.services import get_tokens_for_user
from apps.authentication.tokens import JWTAccessToken
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.db.models import ManyToManyField
from django.http import HttpRequest
from rest_framework.reverse import reverse

from .exceptions import UserNotCreatedAPIException, UserNotFoundAPIException


def create_user(data) -> accounts_models.User:
    """
    Create a new user with the provided data.

    Args:
        data (dict): A dictionary containing user data, such as username, password, etc.

    Returns:
        accounts_models.User: The created user object.

    Raises:
        UserNotCreatedAPIException: If there is an issue during user creation, a specific exception
            is raised.

    Example:
        ```python
        data = {
            "first_name": "Django",
            "last_name": "D",
            "password": "secure_password",
            "email": "john@example.com",
            "type" : "teacher"
        }
        create_user(data)
        ```
    """
    model = get_user_sub_model(user_type=data.get("type"))

    try:
        with transaction.atomic():
            # Extract many-to-many relationships from data
            many_to_many = {}
            for field_name in data.keys():
                try:
                    field = getattr(accounts_models.User, field_name)
                    if isinstance(field, ManyToManyField):
                        many_to_many[field_name] = data.pop(field_name)
                except AttributeError:
                    pass

            # Create user using the default manager's create method
            user = model.objects.create_user(**data)

            # Set many-to-many relationships after user creation
            for field_name, value in many_to_many.items():
                field = getattr(user, field_name)
                field.set(value)

            return user

    except Exception as exc:
        raise UserNotCreatedAPIException(detail="The user could not be inserted") from exc


def update_user(user_id: int, data: dict[str:Any]) -> accounts_models.User:
    """
    Update a user's information.

    Args:
        user_id (int): The ID of the user to update.
        data (dict): A dictionary containing the updated user data.

    Returns:
        accounts_models.User: The updated user object.

    Raises:
        SomeSpecificException: If there is an issue during user update, a specific exception
            is raised.

    Example:
        ```python
        user_id = 42
        updated_data = {'email': 'new_email@example.com'}
        update_user(user_id, updated_data)
        ```
    """

    with transaction.atomic():
        user = get_user_by_id(user_id)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user


def get_user_by_id(pk: int) -> accounts_models.User:
    """
    Retrieve a user by their ID.

    Args:
        pk (int): The ID of the user to retrieve.

    Returns:
        accounts_models.User: The user object.

    Raises:
        UserNotFoundAPIException: If no user with the specified ID is found, a
            `UserNotFoundAPIException` exception is raised.

    Example:
        ```python
        pk = 42
        get_user_by_id(pk)
    """
    try:
        user = accounts_models.User.objects.get(pk=pk)
        return user
    except accounts_models.User.DoesNotExist as exc:
        raise UserNotFoundAPIException(detail=f"User with ID '{pk}' does not exist.") from exc


def get_user_by_email(email: str) -> accounts_models.User:
    """
    Retrieve a user by their email.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        accounts_models.User: The user object.

    Raises:
        UserNotFoundAPIException: If no user with the specified email is found, a
            `UserNotFoundAPIException` exception is raised.

    Example:
        ```python
        email = "email@example.com"
        get_user_by_email(email)
    """
    try:
        user = accounts_models.User.objects.get(email=email)
        return user
    except accounts_models.User.DoesNotExist as exc:
        raise UserNotFoundAPIException(detail=f"User with email '{email}' does not exist.") from exc


def delete_user(user_id: int) -> None:
    """
    Delete a user by their ID.

    Args:
        user_id (int): The ID of the user to delete.

    Raises:
        SomeSpecificException: If there is an issue during user deletion, a specific exception
            is raised.

    Example:
        ```python
        user_id = 42
        delete_user(user_id)
        ```
    """
    with transaction.atomic():
        user = get_user_by_id(user_id)
        user.delete()


def get_user_sub_model(user_type: str) -> accounts_models.User:
    """
    Get the appropriate user sub model based on the user type.

    Args:
        user_type (str): The type of user crud to retrieve, e.g., "admin," "teacher," or "student."

    Returns:
        accounts_models.User: An instance of the appropriate User subclass.

    Example:
        ```python
        user_type = "admin"
        admin_crud = get_create_crud(user_type)
        ```
    """
    sub_models = {
        "admin": accounts_models.Admin,
        "teacher": accounts_models.Teacher,
        "student": accounts_models.Student,
    }

    sub_model = sub_models.get(user_type, None)
    return sub_model


def get_verification_url(request: HttpRequest, email: str) -> str:
    """
    Generate a verification URL for the email verification process.

    Args:
        request (HttpRequest): The Django HTTP request object.
        email (str): The email address for which to generate the verification URL.

    Returns:
        str: The absolute URL for email verification.

    Example:
        Assuming the view name for email verification is 'accounts-api:verify-account',
        this function can be used as follows:

        ```python
        request = HttpRequest()
        email = "user@example.com"
        verification_url = get_verification_url(request, email)
        print(verification_url)
        ```

    Expected Output:
        Assuming the current site domain is 'example.com' and the relative link for
        email verification is '/api/v1/accounts/verify/', the expected output
        should be something like:

        ```
        'http://example.com/api/v1/accounts/verify/?token=your_access_token_here'

        ```
    """
    # Get the user by the inserted email
    user = get_user_by_email(email)

    # Get refresh token for this user
    token = get_tokens_for_user(user)["access"]

    # Get the current site domain
    current_site = get_current_site(request).domain

    # Get the URL of the "verify-account" view
    relative_link = reverse("accounts:v1:verify-account")

    # Determine protocol based on whether the request is secure (HTTPS)
    protocol = "https" if request.is_secure() else "http"

    # Construct the final URL for verification
    abs_url = f"{protocol}://{current_site}{relative_link}?token={token}"  # type:ignore # noqa:E231

    return abs_url


def verify_user_account(user: accounts_models.User) -> bool:
    """
    Verify a user's account.

    Args:
        user (User): The user object to verify.

    Returns:
        bool: True if the user's account is successfully verified.

    Example:
        ```python
        user = User.objects.get(username='example_user')
        verify_user_account(user)
        ```
    """
    if not user.is_verified:
        user.is_verified = True
        user.save()

    return True


def get_user_details(user: accounts_models.User):
    """
    Retrieve details of a user.

    Args:
        user (User): The user object for which to retrieve details.

    Returns:
        dict: A dictionary containing the user's name and tokens.

    Example:
        ```python
        user = User.objects.get(username='example_user')
        user_details = get_user_details(user)
        print(user_details)
        # Output: {'name': 'Example User', 'tokens': {'access_token': '...', 'refresh_token': '...'}}
        ```
    """
    return {
        "name": user.get_full_name(),
        "tokens": get_tokens_for_user(user=user),
    }


def get_user_from_access_token(token: str):
    token_obj = JWTAccessToken(token, verify=True)
    user_id = token_obj["user_id"]
    user = get_user_by_id(pk=user_id)
    return user
