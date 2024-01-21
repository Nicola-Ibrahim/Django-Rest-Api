# OTP number's expiratoin time configuration (in seconds)
OTP_EXPIRATION = 300  # seconds

# Django Superuser configuration
ROOT_USER_EMAIL = "admin@gmail.com"
ROOT_USER_FIRSTNAME = "admin"
ROOT_USER_LASTNAME = "admin"
ROOT_USER_PASSWORD = "admin"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"},
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "colorlog.StreamHandler",
            "formatter": "colored",
            "filters": [],
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logging/django.log",
            "formatter": "colored",
        },
    },
    "loggers": {
        logger_name: {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        }
        for logger_name in (
            "django",
            "django.request",
            "django.db.backends",
            "django.template",
            "dj_rest_api",
            "urllib3",
            "asyncio",
        )
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}
