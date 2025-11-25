import environ

from .main import *  # noqa


env = environ.Env()

DEBUG = env.bool('DEBUG')

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
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True  # noqa
CSRF_COOKIE_SECURE = True  # noqa
SECURE_SSL_REDIRECT = True        # noqa
# SECURE_HSTS_SECONDS = 31536000    # noqa
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True # noqa
# SECURE_HSTS_PRELOAD = True    # noqa

if DEBUG:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
