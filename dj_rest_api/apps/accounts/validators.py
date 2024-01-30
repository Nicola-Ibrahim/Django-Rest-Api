from   import exceptions
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError


def user_validate_password(password: str, user=None, password_validators=None):
    """
    Validate a user's password against the specified password validators.

    This function takes a password and optionally a user and password validators.
    It iterates through the provided password validators, validating the password
    according to each validator's rules.

    Args:
        password (str): The password to be validated.
        user: (optional): The user for whom the password is being validated. Defaults to None.
        password_validators (list, optional): A list of password validators. If not provided,
            the default password validators are used.

    Raises:
        exceptions.PasswordNotValidAPIException: If the password fails validation, a PasswordNotValidAPIException
            exception is raised. The exception includes a `data` attribute containing a list
            of error messages from the failed validators.

    Example:
        ```python
        password = "SecurePassword123"
        user_validate_password(password)
        ```

    Note:
        If no `password_validators` are provided, the default Django password validators
        are used. The function raises a `PasswordNotValidAPIException` exception with a list of error
        messages if the password fails validation.
    """
    errors = []

    if password_validators is None:
        password_validators = get_default_password_validators()

    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error.message)

    if errors:
        raise exceptions.PasswordNotValidAPIException(errors=errors)
