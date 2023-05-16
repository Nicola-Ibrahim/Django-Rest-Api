from django.core.validators import RegexValidator


class NameRegexValidator(RegexValidator):
    """Custom name regex validator that validates if the name value starts by a character"""

    regex = "^[a-zA-Z]{1,}[a-zA-Z0-9]*$"
    message = "name must start by Alphabets"


validate_name = NameRegexValidator()
