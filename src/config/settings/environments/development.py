DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Logger configurations
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
        # "file": {
        #     "level": "DEBUG",
        #     "class": "logging.FileHandler",
        #     "filename": "/logging/django.log",
        #     "formatter": "colored",
        # },
    },
    "loggers": {
        logger_name: {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": True,
        }
        for logger_name in (
            "django",
            "django.request",
            "django.db.backends",
            "django.template",
            "core",
            "urllib3",
            "asyncio",
        )
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}


# Model graph configurations
GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}

# Debugger configurations
INSTALLED_APPS += (
    "drf_yasg",
    "debug_toolbar",
    "django_extensions",
)

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


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "dauth.sqlite3",
    }
}
