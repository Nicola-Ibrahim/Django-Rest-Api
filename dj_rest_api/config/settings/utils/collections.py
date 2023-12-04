def deep_update(base_dict: dict, update_with: dict) -> dict:
    """Update the base settings with custom dev settings

    Args:
        base_dict (dict): base settings file
        update_with (dict): custom settings file

    Returns:
        dict: the new overridden dict
    """

    # Iterate over each item in the new dict (new settings)
    for key, value in update_with.items():
        # If the value is a dict
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)

            # If the original value is also a dict then run it through this same function
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)

            # If the original value is not a dict then just set the new value
            else:
                base_dict[key] = value

        # If the new value is not a dict
        else:
            base_dict[key] = value

    return base_dict
