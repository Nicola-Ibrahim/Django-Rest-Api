from django.db import transaction
from django.db.models import ManyToManyField

from .api.exceptions import UserNotCreatedAPIException, UserNotFoundAPIException
from .models import models


def create_user(data) -> models.User:
    """
    Create a new user with the provided data.

    Args:
        data (dict): A dictionary containing user data, such as username, password, etc.

    Returns:
        models.User: The created user object.

    Raises:
        UserNotCreatedAPIException: If there is an issue during user creation, a specific exception
            is raised.

    Example:
        ```python
        data = {
            'username': 'john_doe',
            'password': 'secure_password',
            'email': 'john@example.com',
            'type' : 'teacher'
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
                    field = getattr(models.User, field_name)
                    if isinstance(field, ManyToManyField):
                        many_to_many[field_name] = data.pop(field_name)
                except AttributeError:
                    pass

            # Create user using the default manager's create method
            user = model.objects.create(**data)

            # Set many-to-many relationships after user creation
            for field_name, value in many_to_many.items():
                field = getattr(user, field_name)
                field.set(value)

            return user

    except Exception:
        raise UserNotCreatedAPIException(detail="The user could not be inserted")


def update_user(user_id, data) -> models.User:
    """
    Update a user's information.

    Args:
        user_id (int): The ID of the user to update.
        data (dict): A dictionary containing the updated user data.

    Returns:
        models.User: The updated user object.

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


def get_user_by_id(user_id) -> models.User:
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        models.User: The user object.

    Raises:
        UserNotFoundException: If no user with the specified ID is found, a
            `UserNotFoundException` exception is raised.

    Example:
        ```python
        user_id = 42
        get_user_by_id(user_id)
    """
    try:
        user = models.User.objects.get(pk=user_id)
        return user
    except models.User.DoesNotExist as exc:
        raise UserNotFoundAPIException(detail=f"User with ID {user_id} does not exist.") from exc


def get_user_by_email(email: str) -> models.User:
    """
    Retrieve a user by their ID.

    Args:
        email (int): The ID of the user to retrieve.

    Returns:
        models.User: The user object.

    Raises:
        UserNotFoundException: If no user with the specified ID is found, a
            `UserNotFoundException` exception is raised.

    Example:
        ```python
        email = "email@example.com"
        get_user_by_id(email)
    """
    try:
        user = models.User.objects.get(email=email)
        return user
    except models.User.DoesNotExist as exc:
        raise UserNotFoundAPIException(detail=f"User with ID {email} does not exist.") from exc


def delete_user(user_id) -> None:
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


def get_user_sub_model(user_type: str) -> models.User:
    """
    Get the appropriate user sub model based on the user type.

    Args:
        user_type (str): The type of user crud to retrieve, e.g., "admin," "teacher," or "student."

    Returns:
        models.User: An instance of the appropriate User subclass.

    Example:
        ```python
        user_type = "admin"
        admin_crud = get_create_crud(user_type)
        ```
    """
    sub_models = {
        "admin": models.Admin,
        "teacher": models.Teacher,
        "student": models.Student,
    }

    sub_model = sub_models.get(user_type, None)
    return sub_model
