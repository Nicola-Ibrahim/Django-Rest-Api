DEBUG = True
SECRET_KEY = "jd@11j#vr_+36p&f)nm9_9ocpt^o!^*fgd(nyhrx1r#xf9_p&5"

SIMPLE_JWT["SIGNING_KEY"] = "jd@11j#vr_+36p&f)nm9_9ocpt^o!^*fgd(nyhrx1r#xf9_p&5"


# Add third-party development apps
INSTALLED_APPS += (  # type: ignore # noqa: F821
    "drf_yasg",
    "debug_toolbar",
    "django_extensions",
)

# Override default DB configuration to create sqlite db
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dev-db.sqlite3",
        "ATOMIC_REQUESTS": True,
    }
}


# Use a dummy email backend during tests (optional)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Debugger configurations
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]

# Swagger configurations
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "basic": {"type": "basic"},
        "api_key": {"type": "apiKey", "in": "header", "name": "Authorization"},
    },
}


REDOC_SETTINGS = {
    "LAZY_RENDERING": False,
}

# ref: https://stackoverflow.com/questions/34360912/deploying-django-app-with-docker-allowed-hosts
# The domain should be added to ALLOWED_HOSTS to be accessible
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:80",
]
