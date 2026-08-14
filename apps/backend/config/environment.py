import os
from enum import StrEnum
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured


class AppEnvironment(StrEnum):
    LOCAL = "local"
    TEST = "test"
    REVIEW = "review"
    STAGING = "staging"
    PRODUCTION = "production"


def environment(default: AppEnvironment = AppEnvironment.LOCAL) -> AppEnvironment:
    raw_value = os.environ.get("APP_ENV", default.value)
    try:
        return AppEnvironment(raw_value)
    except ValueError as error:
        choices = ", ".join(item.value for item in AppEnvironment)
        raise ImproperlyConfigured(f"APP_ENV must be one of: {choices}") from error


def boolean(name: str, *, default: bool) -> bool:
    raw_value = os.environ.get(name)
    if raw_value is None:
        return default
    normalized = raw_value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ImproperlyConfigured(f"{name} must be a boolean")


def csv(name: str, *, default: str = "") -> list[str]:
    return [item.strip() for item in os.environ.get(name, default).split(",") if item.strip()]


def origin_csv(name: str) -> list[str]:
    values = csv(name)
    for value in values:
        parsed = urlparse(value)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ImproperlyConfigured(f"{name} entries must be valid HTTPS origins")
    return values


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ImproperlyConfigured(f"{name} is required")
    return value


def url(name: str, *, default: str | None = None, schemes: set[str]) -> str:
    value = os.environ.get(name, default or "").strip()
    if not value:
        raise ImproperlyConfigured(f"{name} is required")
    parsed = urlparse(value)
    if parsed.scheme not in schemes or not parsed.hostname:
        allowed = ", ".join(sorted(schemes))
        raise ImproperlyConfigured(f"{name} must be a valid URL using: {allowed}")
    return value


def validate_deployed_environment(expected: AppEnvironment) -> None:
    actual = environment()
    if actual is not expected:
        raise ImproperlyConfigured(
            f"APP_ENV={actual.value} does not match settings for {expected.value}"
        )
