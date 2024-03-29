# Database configurations
# It could be overridden when put in production or development
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "drest",
        "USER": "drest",
        "PASSWORD": "drest",
        "HOST": "localhost",
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 0,
    }
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
