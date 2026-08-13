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
