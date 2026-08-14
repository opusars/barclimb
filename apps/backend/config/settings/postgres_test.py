import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from .test import *  # noqa: F403

if not os.environ.get("DATABASE_URL"):
    raise ImproperlyConfigured("DATABASE_URL is required for PostgreSQL tests")

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=0,
        conn_health_checks=True,
        ssl_require=False,
    )
}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,  # noqa: F405
        "KEY_PREFIX": "barclimb:test",
        "OPTIONS": {"socket_connect_timeout": 2, "socket_timeout": 2},
    }
}
READINESS_REQUIRE_KVS = True
