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
