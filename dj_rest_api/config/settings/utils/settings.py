import os

from .misc import yaml_coerce


def get_settings_from_environment(prefix):
    """
    Retrieve settings from environment variables with a given prefix.

    This function scans all environment variables and filters those that start
    with the specified `prefix`. It then creates a dictionary with keys obtained
    by removing the prefix and values obtained by coercing the corresponding
    environment variable value using the `yaml_coerce` function.

    Args:
        prefix (str): The prefix used to filter environment variables.

    Returns:
        dict: A dictionary containing settings extracted from environment variables.

    Example:
        If prefix='DREST_SETTINGS_', and the following environment variable exists:
        DREST_SETTINGS_DEBUG = 1
        The function will return {'DEBUG': 1}.
    """
    # Calculate the length of the prefix to later remove it from keys
    prefix_len = len(prefix)

    # Create a dictionary comprehension to filter and process environment variables
    settings_dict = {
        key[prefix_len:]: yaml_coerce(value) for key, value in os.environ.items() if key.startswith(prefix)
    }

    return settings_dict
