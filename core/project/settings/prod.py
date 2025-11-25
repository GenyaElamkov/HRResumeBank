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


# HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# SECURE_HSTS_SECONDS = 31536000    # noqa
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True # noqa
# SECURE_HSTS_PRELOAD = True    # noqa

if not DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
