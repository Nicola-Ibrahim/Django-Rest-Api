"""Email settings file
For overriding in .env: User DAUTH_ prefix before any variable and assign a new value to it
"""

# ref: https://docs.djangoproject.com/en/4.2/topics/email/#email-backends
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-host
EMAIL_HOST = "smtp.gmail.com"

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-port
EMAIL_PORT = 587

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-user
EMAIL_HOST_USER = NotImplemented

# ref: https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = NotImplemented


# The subject of the email sent to a new user when they register on the platform.
EMAIL_REGISTER_SUBJECT = "Welcome"


# The subject of the email sent to a user when they request to reset their password.
EMAIL_RESETPASSWORD_SUBJECT = "OTP number for resetting password"

# The subject of the email sent to a user when they verify their account
EMAIL_EMAIL_VERIFICATION_SUBJECT = "Verification email"
