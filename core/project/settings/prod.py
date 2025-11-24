import environ

from .main import *  # noqa


env = environ.Env()

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    },
}

# Для тестирования
# SESSION_COOKIE_SECURE = False # noqa
# CSRF_COOKIE_SECURE = False    # noqa
# SECURE_SSL_REDIRECT = False   # noqa

# HTTPS
SESSION_COOKIE_SECURE = True  # noqa
CSRF_COOKIE_SECURE = True  # noqa
SECURE_SSL_REDIRECT = True        # noqa
SECURE_HSTS_SECONDS = 31536000    # noqa
SECURE_HSTS_INCLUDE_SUBDOMAINS = True # noqa
SECURE_HSTS_PRELOAD = True    # noqa
