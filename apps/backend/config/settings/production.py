import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

if not SECRET_KEY:  # noqa: F405
    raise ImproperlyConfigured("DJANGO_SECRET_KEY is required")
if not os.environ.get("DATABASE_URL"):
    raise ImproperlyConfigured("DATABASE_URL is required")
DATABASES = {"default": dj_database_url.config(conn_max_age=60, ssl_require=True)}
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
