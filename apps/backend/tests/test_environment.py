import os
import subprocess
import sys

import pytest
from django.core.exceptions import ImproperlyConfigured

from config.environment import AppEnvironment, boolean, environment, origin_csv, url


def test_environment_rejects_unknown_value(monkeypatch):
    monkeypatch.setenv("APP_ENV", "preview")
    with pytest.raises(ImproperlyConfigured, match="APP_ENV must be one of"):
        environment()


def test_boolean_rejects_malformed_value(monkeypatch):
    monkeypatch.setenv("RUNTIME_FLAG", "sometimes")
    with pytest.raises(ImproperlyConfigured, match="RUNTIME_FLAG must be a boolean"):
        boolean("RUNTIME_FLAG", default=False)


def test_kvs_url_accepts_redis_and_rediss(monkeypatch):
    for value in ("redis://localhost:6379/0", "rediss://kvs.example.test:6380/0"):
        monkeypatch.setenv("REDIS_URL", value)
        assert url("REDIS_URL", schemes={"redis", "rediss"}) == value


def test_deployed_origins_require_https(monkeypatch):
    monkeypatch.setenv("CSRF_TRUSTED_ORIGINS", "http://unsafe.example.test")
    with pytest.raises(ImproperlyConfigured, match="valid HTTPS origins"):
        origin_csv("CSRF_TRUSTED_ORIGINS")


def test_production_configuration_fails_closed_without_required_values():
    env = {
        "PATH": os.environ["PATH"],
        "PYTHONPATH": os.getcwd(),
        "APP_ENV": AppEnvironment.PRODUCTION.value,
        "DJANGO_SETTINGS_MODULE": "config.settings.production",
    }
    result = subprocess.run(
        [sys.executable, "-c", "import django; django.setup()"],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )

    assert result.returncode != 0
    assert "DJANGO_SECRET_KEY is required" in result.stderr


def test_production_cookie_and_transport_security_configuration():
    env = {
        "PATH": os.environ["PATH"],
        "PYTHONPATH": os.getcwd(),
        "APP_ENV": AppEnvironment.PRODUCTION.value,
        "DJANGO_SETTINGS_MODULE": "config.settings.production",
        "DJANGO_SECRET_KEY": "x" * 60,
        "DATABASE_URL": "postgresql://user:pass@db.example.test/barclimb",
        "REDIS_URL": "rediss://kvs.example.test:6380/0",
        "PUBLIC_BASE_URL": "https://barclimb.example.test",
        "ALLOWED_HOSTS": "barclimb.example.test",
        "CSRF_TRUSTED_ORIGINS": "https://barclimb.example.test",
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "DEFAULT_FROM_EMAIL": "BarClimb <no-reply@barclimb.example.test>",
    }
    script = (
        "from django.conf import settings; import django; django.setup(); "
        "assert settings.SESSION_COOKIE_SECURE and settings.SESSION_COOKIE_HTTPONLY; "
        "assert settings.CSRF_COOKIE_SECURE and settings.CSRF_COOKIE_HTTPONLY; "
        "assert settings.SECURE_SSL_REDIRECT and settings.SECURE_HSTS_SECONDS == 31536000"
    )
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, check=False, env=env, text=True
    )
    assert result.returncode == 0, result.stderr


def test_production_rejects_local_only_email_delivery():
    env = {
        "PATH": os.environ["PATH"],
        "PYTHONPATH": os.getcwd(),
        "APP_ENV": AppEnvironment.PRODUCTION.value,
        "DJANGO_SETTINGS_MODULE": "config.settings.production",
        "DJANGO_SECRET_KEY": "x" * 60,
        "DATABASE_URL": "postgresql://user:pass@db.example.test/barclimb",
        "REDIS_URL": "rediss://kvs.example.test:6380/0",
        "PUBLIC_BASE_URL": "https://barclimb.example.test",
        "ALLOWED_HOSTS": "barclimb.example.test",
        "CSRF_TRUSTED_ORIGINS": "https://barclimb.example.test",
        "EMAIL_BACKEND": "django.core.mail.backends.console.EmailBackend",
        "DEFAULT_FROM_EMAIL": "BarClimb <no-reply@barclimb.example.test>",
    }
    result = subprocess.run(
        [sys.executable, "-c", "import django; django.setup()"],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )
    assert result.returncode != 0
    assert "production requires a production-grade email backend" in result.stderr
