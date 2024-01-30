DEBUG = True

SECRET_KEY = "jd@11j#vr_+36p&f)nm9_9ocpt^o!^*fgd(nyhrx1r#xf9_p&5"

SIMPLE_JWT["SIGNING_KEY"] = "jd@11j#vr_+36p&f)nm9_9ocpt^o!^*fgd(nyhrx1r#xf9_p&5"

# Database configuration for tests
# Override default DB configuration to create sqlite db
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test-db.sqlite3",
        "ATOMIC_REQUESTS": True,
    }
}


# Disable Celery during tests (optional)
CELERY_TASK_ALWAYS_EAGER = True

# Speed up password hashing for tests (optional)
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Use a dummy email backend during tests (optional)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"


LOGGING["formatters"]["colored"] = {  # type: ignore # noqa: F821
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}
LOGGING["loggers"]["dj_rest_api"]["level"] = "DEBUG"  # type: ignore # noqa: F821
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # type: ignore # noqa: F821
