import os
from urllib.parse import urlparse

import psycopg2
import yaml


def yaml_coerce(value: str):
    """Convert string value to proper Python

    Args:
        value (str):
    """

    if isinstance(value, str):
        return yaml.load(f"dummy: {value}", Loader=yaml.SafeLoader)["dummy"]

    return value


def get_postgres_database_config():
    """
    Try to connect to a PostgreSQL database using environment variables.
    If successful, return the PostgreSQL database configuration.
    If unsuccessful, return None.
    """
    try:
        db_config = {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "drest_db_dev",
            "USER": "drest",
            "PASSWORD": "drest",
            "HOST": "localhost",
            "PORT": "5432",
            "ATOMIC_REQUESTS": True,
            "CONN_MAX_AGE": 0,
        }

        # Test the connection to the PostgreSQL database
        with psycopg2.connect(database_url):
            pass

        return db_config

    except (psycopg2.OperationalError, ValueError) as e:
        # Handle potential exceptions and log the error if necessary
        print(f"Error connecting to PostgreSQL: {e}")
        return None
