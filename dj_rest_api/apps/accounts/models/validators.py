from django.core.validators import RegexValidator


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
