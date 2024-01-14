from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from ..api import exceptions


class NameRegexValidator(RegexValidator):
    """
    Validator for checking if a name starts with alphabets.

    This validator checks if a given name follows the pattern of starting with alphabets
    and allowing alphanumeric characters afterward.

    Attributes:
        regex (str): Regular expression pattern for the validator.
        message (str): Error message to be raised if validation fails.

    Pattern Details:
        - `^[a-zA-Z]{1,}[a-zA-Z0-9]*$`:
        - `^[a-zA-Z]{1,}`: The name must start with one or more alphabets.
        - `[a-zA-Z0-9]*$`: Followed by zero or more alphanumeric characters.

    Usage Example:
        ```python
        from django.core.exceptions import ValidationError

        name_validator = NameRegexValidator()

        try:
            name_validator("JohnDoe123")
        except ValidationError as e:
            print(e.message)  # Output: "name must start by Alphabets"
        ```

    Note:
        This class extends Django's `RegexValidator` and sets the regex pattern to
        enforce the condition that the name must start with alphabets.

    Reference:
        - Django `RegexValidator`: https://docs.djangoproject.com/en/stable/ref/validators/#regexvalidator
    """

    regex = "^[a-zA-Z]{1,}[a-zA-Z0-9]*$"
    message = "name must start by Alphabets"


validate_name = NameRegexValidator()


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
        exceptions.PasswordNotValid: If the password fails validation, a PasswordNotValid
            exception is raised. The exception includes a `data` attribute containing a list
            of error messages from the failed validators.

    Example:
        ```python
        password = "SecurePassword123"
        user_validate_password(password)
        ```

    Note:
        If no `password_validators` are provided, the default Django password validators
        are used. The function raises a `PasswordNotValid` exception with a list of error
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
        raise exceptions.PasswordNotValid().format_data(errors=errors)
