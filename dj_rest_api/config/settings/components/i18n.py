from django.utils.translation import gettext_lazy as _

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR / "locale"]

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en", _("English")),
]


USE_L10N = False

DATE_FORMAT = "d N, Y"
