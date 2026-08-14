from config.environment import AppEnvironment

from .base import *  # noqa: F403

APP_ENV = AppEnvironment.TEST  # noqa: F405
SECRET_KEY = "test-only"
ALLOWED_HOSTS = ["testserver"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
READINESS_REQUIRE_KVS = False
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
