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

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
