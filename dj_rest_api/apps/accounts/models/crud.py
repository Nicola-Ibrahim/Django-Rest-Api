from django.db import transaction
from django.db.models import ManyToManyField

from . import exceptions, models


class UserCRUD:
    model = None

    def create_user(self, data) -> models.User:
        """
        Create a new user with the provided data.

        Args:
            data (dict): A dictionary containing user data, such as username, password, etc.

        Returns:
            models.User: The created user object.

        Raises:
            SomeSpecificException: If there is an issue during user creation, a specific exception
                is raised.

        Example:
            ```python
            data = {
                'username': 'john_doe',
                'password': 'secure_password',
                'email': 'john@example.com',
                'type' : 'teacher'
            }
            user_crud.create_user(data)
            ```
        """

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
                user = models.User.objects.create(**data)

                # Set many-to-many relationships after user creation
                for field_name, value in many_to_many.items():
                    field = getattr(user, field_name)
                    field.set(value)

                return user

        except Exception:
            raise exceptions.UserNotCreatedException(details="The user could not be inserted")

    def get_user_by_id(self, user_id) -> models.User:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            models.User: The user object.

        Raises:
            exceptions.UserNotFoundException: If no user with the specified ID is found, a
                `UserNotFoundException` exception is raised.

        Example:
            ```python
            user_id = 42
            user_crud.get_user_by_id(user_id)
        """
        try:
            user = self.model.objects.get(pk=user_id)
            return user
        except models.User.DoesNotExist as exc:
            raise exceptions.UserNotFoundException(f"User with ID {user_id} does not exist.") from exc

    def update_user(self, user_id, data) -> models.User:
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
            user_crud.update_user(user_id, updated_data)
            ```
        """
        with transaction.atomic():
            user = self.get_user_by_id(user_id)
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
            return user

    def delete_user(self, user_id) -> None:
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
            user_crud.delete_user(user_id)
            ```
        """
        with transaction.atomic():
            user = self.get_user_by_id(user_id)
            user.delete()


class StudentCRUD(UserCRUD):
    model = models.Student


class TeacherCRUD(UserCRUD):
    model = models.Teacher


class AdminCRUD(UserCRUD):
    model = models.Admin


def get_crud_instance(user_type: str) -> UserCRUD:
    """
    Get the appropriate UserCRUD based on the user type.

    Args:
        user_type (str): The type of user crud to retrieve, e.g., "admin," "teacher," or "student."

    Returns:
        UserCRUD: An instance of the appropriate UserCRUD subclass.

    Example:
        ```python
        user_type = "admin"
        admin_crud = get_create_crud(user_type)
        ```
    """
    cruds_classes = {
        "admin": StudentCRUD,
        "teacher": TeacherCRUD,
        "student": AdminCRUD,
    }

    crud = cruds_classes.get(user_type, None)
    return crud()
