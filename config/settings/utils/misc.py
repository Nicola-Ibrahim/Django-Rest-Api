import os

import yaml


def yaml_coerce(value: str):
    """Convert string value to proper Python

    Args:
        value (str):
    """

    if isinstance(value, str):
        return yaml.load(f"dummy: {value}", Loader=yaml.SafeLoader)["dummy"]

    return value


def get_singing_key(file_path):
    """Get the generated singing key for JWT configs"""
    if os.path.isfile(file_path):
        with open(file_path) as f:
            return f.readline()
