import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from config.environment import (
    AppEnvironment,
    boolean,
    csv,
    origin_csv,
    required,
    url,
    validate_deployed_environment,
)

from .base import *  # noqa: F403

validate_deployed_environment(AppEnvironment.STAGING)  # noqa: F405
SECRET_KEY = required("DJANGO_SECRET_KEY")  # noqa: F405
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be at least 50 characters")
DATABASE_URL = url("DATABASE_URL", schemes={"postgres", "postgresql"})  # noqa: F405
REDIS_URL = url("REDIS_URL", schemes={"redis", "rediss"})  # noqa: F405
PUBLIC_BASE_URL = url("PUBLIC_BASE_URL", schemes={"https"})  # noqa: F405
ALLOWED_HOSTS = csv("ALLOWED_HOSTS")  # noqa: F405
CSRF_TRUSTED_ORIGINS = origin_csv("CSRF_TRUSTED_ORIGINS")
if not ALLOWED_HOSTS or not CSRF_TRUSTED_ORIGINS:
    raise ImproperlyConfigured("hosts and CSRF origins are required")
if "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS may not contain '*' in staging")
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
EMAIL_BACKEND = required("EMAIL_BACKEND")  # noqa: F405
DEFAULT_FROM_EMAIL = required("DEFAULT_FROM_EMAIL")  # noqa: F405
if EMAIL_BACKEND in {
    "django.core.mail.backends.console.EmailBackend",
    "django.core.mail.backends.locmem.EmailBackend",
}:
    raise ImproperlyConfigured("staging requires a production-grade email backend")
if EMAIL_BACKEND == "config.email_backends.StagingAuthEmailSink" and not boolean(
    "ALLOW_STAGING_AUTH_EMAIL_SINK", default=False
):
    raise ImproperlyConfigured("the staging auth email sink requires explicit opt-in")
if MOBILE_LINKS_ENABLED and (  # noqa: F405
    not APPLE_TEAM_ID  # noqa: F405
    or not IOS_BUNDLE_IDENTIFIER  # noqa: F405
    or not ANDROID_PACKAGE_NAME  # noqa: F405
    or not ANDROID_SHA256_CERT_FINGERPRINTS  # noqa: F405
):
    raise ImproperlyConfigured("mobile association identifiers are required when links are enabled")
