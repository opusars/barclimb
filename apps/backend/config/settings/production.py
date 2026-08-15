import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from config.environment import (
    AppEnvironment,
    csv,
    origin_csv,
    required,
    url,
    validate_deployed_environment,
)

from .base import *  # noqa: F403

validate_deployed_environment(AppEnvironment.PRODUCTION)  # noqa: F405
SECRET_KEY = required("DJANGO_SECRET_KEY")  # noqa: F405
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be at least 50 characters")
DATABASE_URL = url("DATABASE_URL", schemes={"postgres", "postgresql"})  # noqa: F405
REDIS_URL = url("REDIS_URL", schemes={"redis", "rediss"})  # noqa: F405
PUBLIC_BASE_URL = url("PUBLIC_BASE_URL", schemes={"https"})  # noqa: F405
ALLOWED_HOSTS = csv("ALLOWED_HOSTS")  # noqa: F405
CSRF_TRUSTED_ORIGINS = origin_csv("CSRF_TRUSTED_ORIGINS")
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS is required")
if "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS may not contain '*' in production")
if not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured("CSRF_TRUSTED_ORIGINS is required")
if DEBUG:  # noqa: F405
    raise ImproperlyConfigured("DJANGO_DEBUG must be false")
DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=60, ssl_require=True)}
CACHES["default"]["LOCATION"] = REDIS_URL  # noqa: F405
CELERY_BROKER_URL = REDIS_URL
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
TRUST_HEROKU_ROUTER_IP = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
EMAIL_BACKEND = required("EMAIL_BACKEND")  # noqa: F405
DEFAULT_FROM_EMAIL = required("DEFAULT_FROM_EMAIL")  # noqa: F405
if EMAIL_BACKEND in {
    "django.core.mail.backends.console.EmailBackend",
    "django.core.mail.backends.locmem.EmailBackend",
    "config.email_backends.StagingAuthEmailSink",
}:
    raise ImproperlyConfigured("production requires a production-grade email backend")
