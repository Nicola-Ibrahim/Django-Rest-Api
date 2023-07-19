import yaml


def yaml_coerce(value: str):
    """Convert string value to proper Python

    Args:
        value (str):
    """

    if isinstance(value, str):
        return yaml.load(f"dummy: {value}", Loader=yaml.SafeLoader)["dummy"]

    return value
