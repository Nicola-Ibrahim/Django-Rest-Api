from corsheaders.defaults import default_headers

SECRET_KEY = NotImplemented  # In production mode, override DREST_SETTINGS_SECRET_KEY and assign value to it
SIMPLE_JWT[
    "SIGNING_KEY"
] = NotImplemented  # In production mode, override DREST_SETTINGS_SIMPLE_JWT['SECRET_KEY'] and assign value to it

DEBUG = False

# ref: https://stackoverflow.com/questions/34360912/deploying-django-app-with-docker-allowed-hosts
# The domain should be added to ALLOWED_HOSTS to be accessible
ALLOWED_HOSTS = []

CORS_ALLOW_HEADERS = (*default_headers,)

CORS_ALLOWED_ORIGINS = []
