import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.core.exceptions import ImproperlyConfigured

from config.environment import AppEnvironment, boolean, environment, origin_csv, url

BACKEND_DIR = Path(__file__).resolve().parents[1]


def deployed_environment_values(name: str):
    return {
        "PATH": os.environ["PATH"],
        "PYTHONPATH": str(BACKEND_DIR),
        "APP_ENV": name,
        "DJANGO_SETTINGS_MODULE": f"config.settings.{name}",
        "DJANGO_SECRET_KEY": "x" * 60,
        "DATABASE_URL": "postgresql://user:pass@db.example.test/barclimb",
        "REDIS_URL": "rediss://kvs.example.test:6380/0",
        "PUBLIC_BASE_URL": f"https://web-{name}.example.test",
        "ALLOWED_HOSTS": f"api-{name}.example.test",
        "CSRF_TRUSTED_ORIGINS": f"https://api-{name}.example.test",
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "DEFAULT_FROM_EMAIL": "BarClimb <no-reply@barclimb.example.test>",
    }


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


def test_staging_can_explicitly_apply_heroku_kvs_self_signed_tls_contract():
    env = deployed_environment_values("staging")
    env["REDIS_TLS_ALLOW_SELF_SIGNED"] = "true"
    script = (
        "import ssl; import django; django.setup(); "
        "from django.conf import settings; "
        "assert settings.CACHES['default']['OPTIONS']['ssl_cert_reqs'] is None; "
        "assert settings.CELERY_BROKER_USE_SSL['ssl_cert_reqs'] == ssl.CERT_NONE"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_deployed_origins_require_https(monkeypatch):
    monkeypatch.setenv("CSRF_TRUSTED_ORIGINS", "http://unsafe.example.test")
    with pytest.raises(ImproperlyConfigured, match="valid HTTPS origins"):
        origin_csv("CSRF_TRUSTED_ORIGINS")


def test_production_configuration_fails_closed_without_required_values():
    env = {
        "PATH": os.environ["PATH"],
        "PYTHONPATH": str(BACKEND_DIR),
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
        "PYTHONPATH": str(BACKEND_DIR),
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
        "PYTHONPATH": str(BACKEND_DIR),
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


def test_staging_sink_requires_explicit_opt_in():
    env = deployed_environment_values("staging")
    env["EMAIL_BACKEND"] = "config.email_backends.StagingAuthEmailSink"
    result = subprocess.run(
        [sys.executable, "-c", "import django; django.setup()"],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )
    assert result.returncode != 0
    assert "requires explicit opt-in" in result.stderr
    env["ALLOW_STAGING_AUTH_EMAIL_SINK"] = "true"
    accepted = subprocess.run(
        [sys.executable, "-c", "import django; django.setup()"],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )
    assert accepted.returncode == 0, accepted.stderr


def test_production_rejects_staging_email_sink():
    env = deployed_environment_values("production")
    env["EMAIL_BACKEND"] = "config.email_backends.StagingAuthEmailSink"
    env["ALLOW_STAGING_AUTH_EMAIL_SINK"] = "true"
    result = subprocess.run(
        [sys.executable, "-c", "import django; django.setup()"],
        capture_output=True,
        check=False,
        env=env,
        text=True,
    )
    assert result.returncode != 0
    assert "production requires a production-grade email backend" in result.stderr


@pytest.mark.parametrize("name", ["review", "staging", "production"])
def test_each_deployed_environment_uses_web_origin_and_https_proxy_contract(name):
    env = deployed_environment_values(name)
    script = (
        "import django; django.setup(); "
        "from django.conf import settings; "
        "from accounts.services import action_url; "
        f"assert settings.PUBLIC_BASE_URL == 'https://web-{name}.example.test'; "
        "assert settings.SECURE_SSL_REDIRECT; "
        "assert settings.SECURE_PROXY_SSL_HEADER == ('HTTP_X_FORWARDED_PROTO', 'https'); "
        "assert settings.SESSION_COOKIE_SECURE and settings.CSRF_COOKIE_SECURE; "
        "assert settings.TRUST_HEROKU_ROUTER_IP; "
        f"assert action_url('reset-password', 'secret') == "
        f"'https://web-{name}.example.test/reset-password#token=secret'"
    )
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, check=False, env=env, text=True
    )
    assert result.returncode == 0, result.stderr
