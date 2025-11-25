import os
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")

INSTALLED_APPS = [
    # app
    "admin_interface",
    "colorfield",
    # standart
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # first party
    "core.apps.accounts.apps.AccountsConfig",
    "core.apps.authentication.apps.AuthenticationConfig",
    "core.apps.resumes.apps.ResumesConfig",
    "core.apps.audit.apps.AuditConfig",
    "core.apps.help.apps.HelpConfig",
    # app
    'django_extensions',
    'tinymce',
    'easyaudit',
    'axes',
]
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
AUTH_USER_MODEL = "accounts.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Customs middleware для авторизации
    "core.apps.authentication.middleware.LoginRequiredMiddleware",
    "axes.middleware.AxesMiddleware",
]

AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]


ROOT_URLCONF = "core.project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'core.apps.help.context_processors.help_system_context',
            ],
        },
    },
]


WSGI_APPLICATION = "core.project.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "static"                 # noqa
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'authentication:login'

LOGIN_URL = 'authentication:login'
SESSION_COOKIE_AGE = 86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True

# Настройки django-axes
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 60
AXES_RESET_ON_SUCCESS = True
AXES_LOCKOUT_URL = 'authentication:locked'
AXES_LOCKOUT_TEMPLATE = 'authentication/locked.html'

AXES_SUPERUSER = True
# Включать логирование запросов
AXES_DISABLE_ACCESS_LOG = False

AXES_LOCKOUT_PARAMETERS = ['ip_address', 'username']
AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = True

# Настройка tinymce
TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',

    'branding': False,      # Отключает брендинг
    'promotion': False,     # Отключает промо-ссылки


    'elementpath': False,

    'plugins': '''
        textcolor save link image media preview codesample
        contextmenu table lists fullscreen insertdatetime
        nonbreaking directionality searchreplace wordcount
        visualblocks visualchars autolink charmap print
        hr anchor pagebreak help
    ''',

    'toolbar': '''
        fullscreen preview | bold italic underline |
        fontselect fontsizeselect | forecolor backcolor |
        alignleft alignright aligncenter alignjustify |
        indent outdent | bullist numlist table |
        link image media codesample |
        visualblocks visualchars charmap hr pagebreak |
        nonbreaking anchor code
    ''',

    'help_tabs': [
        'shortcuts',
        'keyboardnav',
    ],
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,

}
