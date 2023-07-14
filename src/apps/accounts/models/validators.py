from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from ..api import exceptions


class NameRegexValidator(RegexValidator):
    """Custom name regex validator that validates if the name value starts by a character"""

    regex = "^[a-zA-Z]{1,}[a-zA-Z0-9]*$"
    message = "name must start by Alphabets"


validate_name = NameRegexValidator()


def user_validate_password(password, user=None, password_validators=None):
    """
    Validate that the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
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
        raise exceptions.PasswordNotValid(errors=errors)
