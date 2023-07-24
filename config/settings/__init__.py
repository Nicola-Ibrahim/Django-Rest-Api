import logging
import os
import os.path
from pathlib import Path

import dotenv
from split_settings.tools import include, optional

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Namespacing our own custom environment variables
ENVVAR_SETTINGS_PREFIX = "DAUTH_SETTINGS_"

LOCAL_SETTINGS_PATH = os.getenv(f"{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = "local/settings.dev.py"

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)


DJANGO_ENV = os.environ.get(f"{ENVVAR_SETTINGS_PREFIX}DJANGO_ENV", "development")

if DJANGO_ENV == "development":
    dotenv.load_dotenv(".envs/.env.dev")
elif DJANGO_ENV == "productions":
    dotenv.load_dotenv(".envs/.env.prod")

include(
    "components/base.py",
    "components/database.py",
    "components/email.py",
    "components/custom.py",
    "envvars.py",
    # Select the right env:
    f"environments/{DJANGO_ENV}.py",
    optional(LOCAL_SETTINGS_PATH),
    "components/third_party.py",
)


logging.captureWarnings(True)
