from .main import *  # noqa


DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'main-app'] # noqa
# ALLOWED_HOSTS = ['217.26.27.239']                               # noqa

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
