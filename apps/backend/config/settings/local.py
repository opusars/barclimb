import os

from config.environment import AppEnvironment

from .base import *  # noqa: F403

APP_ENV = AppEnvironment.LOCAL  # noqa: F405
DEBUG = boolean("DJANGO_DEBUG", default=True)  # noqa: F405
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "local-development-only")
ALLOWED_HOSTS = csv("ALLOWED_HOSTS", default="localhost,127.0.0.1")  # noqa: F405
