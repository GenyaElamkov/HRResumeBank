import environ

from .main import *  # noqa


env = environ.Env()

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")
# Для тестирования
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# HTTPS
# SESSION_COOKIE_SECURE = True  # noqa
# CSRF_COOKIE_SECURE = True  # noqa
# SECURE_SSL_REDIRECT = True        # noqa
# SECURE_HSTS_SECONDS = 31536000    # noqa
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True # noqa
# SECURE_HSTS_PRELOAD = True    # noqa
