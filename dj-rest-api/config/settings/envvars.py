"""
This script is responsible to override settings variable from .env file

INSPIRATION FROM:
    - https://github.com/thenewboston-developers/Cooking-Core/blob/068c56d2190da814a6d64543ce4fb2abcf5fcda9/cooking_core/project/settings/envvars.py

"""

from .utils.collections import deep_update
from .utils.settings import get_settings_from_environment

# update the project settings variables with environment variables
deep_update(globals(), get_settings_from_environment(ENVVAR_SETTINGS_PREFIX))  # type: ignore
