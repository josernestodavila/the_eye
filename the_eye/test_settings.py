from .settings import (
    AUTH_USER_MODEL,
    DATABASES,
    INSTALLED_APPS,
    MIDDLEWARE,
    TEMPLATES,
    TIME_ZONE,
    USE_TZ,
)


SECRET_KEY = 'fake-key'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
