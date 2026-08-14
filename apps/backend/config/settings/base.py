import os
from pathlib import Path

import dj_database_url

from config.environment import boolean, csv, environment, url

BASE_DIR = Path(__file__).resolve().parents[2]
APP_ENV = environment()
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "")
DEBUG = boolean("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = csv("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = csv("CSRF_TRUSTED_ORIGINS")
PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "")
REDIS_URL = url(
    "REDIS_URL",
    default="redis://localhost:6379/0",
    schemes={"redis", "rediss"},
)
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "accounts",
    "health",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = []
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://localhost:5432/barclimb",
        conn_max_age=60,
        ssl_require=False,
    )
}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "KEY_PREFIX": f"barclimb:{APP_ENV.value}",
        "OPTIONS": {"socket_connect_timeout": 2, "socket_timeout": 2},
    }
}
READINESS_REQUIRE_KVS = boolean("READINESS_REQUIRE_KVS", default=True)
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = None
CELERY_TASK_IGNORE_RESULT = True
CELERY_TASK_STORE_EAGER_RESULT = False
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_ACKS_LATE = False
CELERY_TASK_REJECT_ON_WORKER_LOST = False
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BEAT_SCHEDULE = {
    "recover-auth-email-outbox": {
        "task": "identity.recover_auth_email_outbox",
        "schedule": 60.0,
    }
}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "accounts.authentication.NativeSessionAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_SAVE_EVERY_REQUEST = False
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "BarClimb <no-reply@localhost>")
AUTH_ACTION_TOKEN_TTL_SECONDS = 60 * 60
NATIVE_SESSION_TTL_SECONDS = 60 * 60 * 24 * 30
TRUST_HEROKU_ROUTER_IP = False
AUTH_EMAIL_MAX_ATTEMPTS = 4
AUTH_EMAIL_RETRY_BACKOFF_SECONDS = (30, 120, 600)
AUTH_EMAIL_PROCESSING_LEASE_SECONDS = 5 * 60
AUTH_EMAIL_PUBLISH_MAX_RETRIES = 3
AUTH_RATE_LIMITS = {
    "login": (5, 300),
    "signup": (5, 3600),
    "verification_resend": (3, 3600),
    "password_reset": (5, 3600),
    "native_session": (10, 300),
}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"structured": {"()": "config.logging.StructuredFormatter"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "structured"}},
    "root": {"handlers": ["console"], "level": os.environ.get("LOG_LEVEL", "INFO")},
}
