"""
Django settings for ferozfaiz project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# The key must be safe if being deployed to kubernetes
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ["true", "1"]

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "corsheaders",
    "django_celery_results",
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "blogs.apps.BlogsConfig",
    "oauth.apps.OauthConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middlewares.SessionMiddleware",
    "core.middlewares.TimezoneMiddleware",
]

ROOT_URLCONF = "ferozfaiz.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ferozfaiz.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PG_MASTER_DATABASE"),
        "USER": os.environ.get("PG_MASTER_USER", "postgres"),
        "PASSWORD": os.environ.get("PG_MASTER_PASSWORD"),
        "HOST": os.environ.get("PG_MASTER_HOST"),
        "PORT": os.environ.get("PG_MASTER_PORT", "5432"),
        "OPTIONS": {
            "sslmode": "verify-ca",
            "sslrootcert": os.environ.get("PG_SSL_ROOT_CERT"),
        },
    },
    "replica_1": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PG_MASTER_DATABASE"),
        "USER": os.environ.get("PG_MASTER_USER", "postgres"),
        "PASSWORD": os.environ.get("PG_MASTER_PASSWORD"),
        "HOST": os.environ.get("PG_REPLICA_HOST_1"),
        "PORT": os.environ.get("PG_MASTER_PORT", "5432"),
        "OPTIONS": {
            "sslmode": "verify-ca",
            "sslrootcert": os.environ.get("PG_SSL_ROOT_CERT"),
        },
    }
}

DATABASE_ROUTERS = ["core.routers.database_routers.PrimaryReplicaRouter"]


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# feroz
# added by me below

# default PBKDF2PasswordHasher password hashing algorithm
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Custom user model
AUTH_USER_MODEL = "users.User"

# Custom session store
SESSION_ENGINE = "core.sessions.session_store"

# only if you want to store static files in app directories
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

LANGUAGES = [
    ("en", _("English")),
]

AUTHENTICATION_BACKENDS = ["core.backends.CaseInsensitiveModelBackend"]

KAFKA_SERVERS = [os.environ.get(
    "KAFKA_SERVER_1"), os.environ.get("KAFKA_SERVER_2")]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message} {pathname} {lineno} {funcName}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "kafka": {
            "level": "DEBUG",  # Capture all log levels
            "class": "core.logging.KafkaLoggingHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {  # This is the root logger
            "handlers": ["console", "kafka"],
            "level": "DEBUG",
            "propagate": True,
        },
        "core": {  # This is the app logger
            "handlers": ["console", "kafka"],
            "level": "INFO",
            "propagate": False,
        },
        "django": {  # For Django's default logger
            "handlers": ["console", "kafka"],
            "level": "INFO",
            "propagate": False,  # Prevents duplicate logging
        },
        "test": {  # For test logger
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_SENDER_ADDRESS = os.environ.get("EMAIL_SENDER_ADDRESS")

# Celery settings
CELERY_BROKER_URL = [os.environ.get("CELERY_BROKER_URL_1")]
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
# CELERY_TASK_TRACK_STARTED = True
# CELERYD_HIJACK_ROOT_LOGGER = False
# worker_hijack_root_logger = False

# pip install "redis[hiredis]"
# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": [
            os.environ.get("REDIS_LOCATION_1"),
            os.environ.get("REDIS_LOCATION_2"),
        ],
    }
}

OAUTH_PROVIDERS = {
    "google": {
        "client_id": os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
        "client_secret": os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
        "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI_PROD") if not DEBUG else os.environ.get("GOOGLE_REDIRECT_URI"),
        "auth_url": os.environ.get("GOOGLE_AUTH_URI"),
        "token_url": os.environ.get("GOOGLE_TOKEN_URI"),
    },
    "microsoft": {
        "client_id": os.environ.get("MICROSOFT_OAUTH_CLIENT_ID"),
        "client_secret": os.environ.get("MICROSOFT_OAUTH_CLIENT_SECRET"),
        "auth_url": os.environ.get("MICROSOFT_AUTH_URI"),
        "token_url": os.environ.get("MICROSOFT_TOKEN_URI"),
        "user_info_url": os.environ.get("MICROSOFT_USER_INFO_URI"),
        "redirect_uri": os.environ.get("MICROSOFT_REDIRECT_URI_PROD") if not DEBUG else os.environ.get("MICROSOFT_REDIRECT_URI"),
    },
    # Add other providers here
}

APPDATA = {
    "ANGULAR_GIT_URL": os.environ.get('ANGULAR_GIT_URL'),
    "ANGULAR_URL": os.environ.get('ANGULAR_URL'),
    "ANSIBLE_GIT_URL": os.environ.get('ANSIBLE_GIT_URL'),
    "DJANGO_POSTGRESQL_DATABASE": os.environ.get('DJANGO_POSTGRESQL_DATABASE'),
    "DJANGO_REST_FRAMEWORK_GIT_URL": os.environ.get('DJANGO_REST_FRAMEWORK_GIT_URL'),
    "DJANGO_REST_FRAMEWORK_URL": os.environ.get('DJANGO_REST_FRAMEWORK_URL'),
    "EXPRESSJS_GIT_URL": os.environ.get('EXPRESSJS_GIT_URL'),
    "EXPRESSJS_URL": os.environ.get('EXPRESSJS_URL'),
    "FEROZ_EMAIL": os.environ.get('FEROZ_EMAIL'),
    "GIT_URL": os.environ.get('GIT_URL'),
    "LINKEDIN_URL": os.environ.get('LINKEDIN_URL'),
    "REACTJS_GIT_URL": os.environ.get('REACTJS_GIT_URL'),
    "REACTJS_URL": os.environ.get('REACTJS_URL'),
    "SITE_NAME": os.environ.get('SITE_NAME'),
    "TIPTAP_INLINE_CODE_HIGHLIGHT_URL": os.environ.get('TIPTAP_INLINE_CODE_HIGHLIGHT_URL'),
    "TIPTAP_INLINE_CODE_HIGHLIGHT_GIT_URL": os.environ.get('TIPTAP_INLINE_CODE_HIGHLIGHT_GIT_URL'),
    "DJANGO_BLOG_URL": os.environ.get('DJANGO_BLOG_URL'),
    "DJANGO_BLOG_GIT_URL": os.environ.get('DJANGO_BLOG_GIT_URL'),
}

# only if you have django-cors-headers installed and added to INSTALLED_APPS
# cors headers settings are needed if you are going to make api calls from browser or mobile app
# CORS_ALLOWED_ORIGINS = [
#     "https://devops.dala-ling.ts.net",
# ]

CSRF_TRUSTED_ORIGINS = [
    "https://djangotest.ferozfaiz.com",
    "https://ferozfaiz.com",
]

# Elasticsearch settings
ELASTICSEARCH_SERVER_1 = os.environ.get("ELASTICSEARCH_SERVER_1")
ELASTICSEARCH_SERVER_2 = os.environ.get("ELASTICSEARCH_SERVER_2")
ELASTICSEARCH_CLIENT_ID = os.environ.get("ELASTICSEARCH_CLIENT_ID")
ELASTICSEARCH_CLIENT_SECRET = os.environ.get("ELASTICSEARCH_CLIENT_SECRET")


if DEBUG:
    DATABASES["default"]["OPTIONS"]["sslrootcert"] = os.environ.get(
        "POSTGRESQL_SSL_ROOT_CERT_DJANGO_DEV")
    DATABASES["replica_1"]["OPTIONS"]["sslrootcert"] = os.environ.get(
        "POSTGRESQL_SSL_ROOT_CERT_DJANGO_DEV")
    # LOGGING["handlers"]["file"] = {
    #     "level": "DEBUG",
    #     "class": "logging.FileHandler",
    #     "filename": "/home/feroz/app/ferozfaiz/ferozfaiz/logs.log",
    #     "formatter": "verbose",
    # }
    # for logger in LOGGING["loggers"].values():
    #     logger["handlers"].append("file")

    # https://stackoverflow.com/questions/70285834/forbidden-403-csrf-verification-failed-request-aborted-reason-given-for-fail
    # when using Tailscale serve or funnel, you'll get cross origin error becuase of the proxy.
    # below settings are needed to fix the issue
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # https://stackoverflow.com/questions/70285834/forbidden-403-csrf-verification-failed-request-aborted-reason-given-for-fail
    # For Tailscale serve or funnel, you'll get cross origin error if you don't add the origin to CSRF_TRUSTED_ORIGINS
    # or enable CORS_ALLOWED_ORIGINS from django-cors-headers, django-cors-headers is a better solution
    # setting SECURE_PROXY_SSL_HEADER fixed the issue, but it's not a good solution
    # CSRF_TRUSTED_ORIGINS = [
    #     "https://devops.dala-ling.ts.net",
    # ]

    INSTALLED_APPS += [
        "debug_toolbar",
    ]

    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]

    # adding remote ip (ISP ip) address to INTERNAL_IPS fixed the issue, but it's not a good solution
    # below is a better solution
    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
