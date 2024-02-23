# ref: https://docs.djangoproject.com/en/4.2/topics/email/#email-backends
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # this value should be set according to environment

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-host
EMAIL_HOST = "smtp.gmail.com"  # this value should be set according to environment

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-port
EMAIL_PORT = 587

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-user
EMAIL_HOST_USER = NotImplemented

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = NotImplemented
