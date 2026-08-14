import hashlib

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import Throttled


def _digest(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode()).hexdigest()[:24]


def enforce_rate_limit(operation: str, *, ip: str, identity: str = "") -> None:
    limit, window = settings.AUTH_RATE_LIMITS[operation]
    key = f"auth-rate:{operation}:{_digest(ip)}:{_digest(identity) if identity else '-'}"
    if cache.add(key, 1, timeout=window):
        return
    try:
        count = cache.incr(key)
    except ValueError:
        cache.set(key, 1, timeout=window)
        count = 1
    if count > limit:
        raise Throttled(wait=window)
