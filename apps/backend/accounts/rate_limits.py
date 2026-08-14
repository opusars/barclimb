import hashlib
import ipaddress

from django.conf import settings
from django.core.cache import cache
from redis.exceptions import RedisError
from rest_framework.exceptions import APIException, Throttled


class AuthenticationRateLimitUnavailable(APIException):
    status_code = 503
    default_detail = "Authentication is temporarily unavailable."
    default_code = "authentication_rate_limit_unavailable"


def _digest(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode()).hexdigest()[:24]


def _normalized_ip(value: str) -> str | None:
    try:
        return ipaddress.ip_address(value.strip()).compressed
    except ValueError:
        return None


def client_ip(request) -> str:
    """Resolve the Heroku-router-observed address without trusting caller-prepended values."""

    remote = _normalized_ip(request.META.get("REMOTE_ADDR", ""))
    if settings.TRUST_HEROKU_ROUTER_IP:
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            router_observed = _normalized_ip(forwarded.rsplit(",", 1)[-1])
            if router_observed is not None:
                return router_observed
    return remote or "unknown"


def enforce_rate_limit(operation: str, *, ip: str, identity: str = "") -> None:
    limit, window = settings.AUTH_RATE_LIMITS[operation]
    key = f"auth-rate:{operation}:{_digest(ip)}:{_digest(identity) if identity else '-'}"
    try:
        if cache.add(key, 1, timeout=window):
            return
        try:
            count = cache.incr(key)
        except ValueError:
            cache.set(key, 1, timeout=window)
            count = 1
    except (RedisError, ConnectionError, TimeoutError, OSError) as error:
        raise AuthenticationRateLimitUnavailable() from error
    if count > limit:
        raise Throttled(wait=window)
