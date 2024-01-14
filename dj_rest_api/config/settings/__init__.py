"""
settings module
this module contains many sub-configuration file for the project.
It gathers them all and treat them as a one settings file.

INSPIRATION FROM:
    - https://github.com/thenewboston-developers/Cooking-Core/tree/068c56d2190da814a6d64543ce4fb2abcf5fcda9/cooking_core/project/settings
"""

import logging
import os
import os.path
from pathlib import Path

from split_settings.tools import include

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Namespace the custom environment variables
ENVVAR_SETTINGS_PREFIX = "DREST_SETTINGS_"

DJANGO_ENV = os.environ.get(f"{ENVVAR_SETTINGS_PREFIX}DJANGO_ENV", "development")

include(
    "components/base.py",
    "components/i18n.py",
    "components/database.py",
    "components/email.py",
    "components/custom.py",
    "components/third_party.py",
    f"environments/{DJANGO_ENV}.py",  # Select the right env
    "envvars.py",
)


logging.captureWarnings(True)
