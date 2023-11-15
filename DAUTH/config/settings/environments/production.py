# In production mode, override DAUTH_SETTINGS_SECRET_KEY and assign value to it
SECRET_KEY = NotImplemented

DEBUG = False

if IN_DOCKER:  # type: ignore # noqa: F821
    # We need it to serve static files with DEBUG=False
    assert MIDDLEWARE[:1] == ["django.middleware.security.SecurityMiddleware"]  # type: ignore # noqa: F821
