import environ

from .main import *  # noqa


env = environ.Env()

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")


SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
