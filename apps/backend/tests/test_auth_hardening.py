from unittest.mock import Mock
from urllib.parse import parse_qs, urlsplit

import pytest
from django.core import mail
from django.core.cache import cache
from django.test import override_settings
from django.utils import timezone
from redis.exceptions import RedisError
from rest_framework.exceptions import Throttled
from rest_framework.test import APIClient, APIRequestFactory

from accounts.models import AuthEmailDelivery, EmailActionToken, NativeSession, User
from accounts.rate_limits import AuthenticationRateLimitUnavailable, client_ip, enforce_rate_limit
from accounts.services import action_url, queue_password_reset, queue_verification
from accounts.tasks import (
    AuthEmailDeliveryUnavailable,
    deliver_auth_email,
    recover_auth_email_outbox,
)

PASSWORD = "Climb-ready-passphrase-47!"
REPLACEMENT = "Different-passphrase-82!"


@pytest.fixture(autouse=True)
def clear_rate_limits():
    cache.clear()


@pytest.fixture
def user(db):
    return User.objects.create_user("learner@example.com", "future_lawyer", PASSWORD)


def csrf_client():
    client = APIClient(enforce_csrf_checks=True)
    token = client.get("/api/v1/auth/csrf/").json()["csrf_token"]
    return client, token


@pytest.mark.django_db
def test_action_links_use_canonical_web_fragment_and_supported_routes(settings):
    settings.PUBLIC_BASE_URL = "https://web.example.test"
    for route in ("reset-password", "verify-email"):
        parsed = urlsplit(action_url(route, "secret-action-token"))
        assert parsed.scheme == "https"
        assert parsed.netloc == "web.example.test"
        assert parsed.path == f"/{route}"
        assert parsed.query == ""
        assert parse_qs(parsed.fragment) == {"token": ["secret-action-token"]}


@override_settings(PUBLIC_BASE_URL="")
def test_local_action_link_defaults_to_vite_completion_surface():
    assert (
        action_url("reset-password", "secret")
        == "http://localhost:5173/reset-password#token=secret"
    )


@pytest.mark.django_db
def test_action_credentials_are_post_body_only_and_never_accepted_from_get(user):
    _, raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    client = APIClient()
    response = client.get(f"/api/v1/auth/password-reset/confirm/?token={raw}")
    assert response.status_code == 405
    assert EmailActionToken.objects.get(user=user).used_at is None


@pytest.mark.django_db
def test_outbox_publication_contains_only_durable_identifier(
    user, monkeypatch, django_capture_on_commit_callbacks
):
    published = {}

    def capture_publish(**kwargs):
        published.update(kwargs)

    monkeypatch.setattr(deliver_auth_email, "apply_async", capture_publish)
    with django_capture_on_commit_callbacks(execute=True):
        delivery = queue_verification(user)
    raw = delivery.action_token.derive_raw()
    assert published["args"] == [str(delivery.id)]
    assert published["argsrepr"] == "(<auth-email-delivery>,)"
    assert raw not in repr(published)
    assert raw not in repr(delivery.__dict__)


@pytest.mark.django_db
def test_broker_outage_leaves_delivery_durably_pending(
    user, monkeypatch, django_capture_on_commit_callbacks
):
    def unavailable(**_kwargs):
        raise ConnectionError("broker unavailable")

    monkeypatch.setattr(deliver_auth_email, "apply_async", unavailable)
    with django_capture_on_commit_callbacks(execute=True):
        delivery = queue_password_reset(user)
    delivery.refresh_from_db()
    assert delivery.status == AuthEmailDelivery.Status.PENDING
    assert delivery.attempts == 0


def test_scheduled_outbox_recovery_publishes_due_deliveries(monkeypatch):
    recover = Mock(return_value=3)
    monkeypatch.setattr("accounts.tasks.publish_due_auth_email_deliveries", recover)
    recover_auth_email_outbox.run()
    recover.assert_called_once_with()


@pytest.mark.django_db
def test_duplicate_delivery_is_idempotent(user, django_capture_on_commit_callbacks):
    with django_capture_on_commit_callbacks(execute=False):
        delivery = queue_verification(user)
    deliver_auth_email.run(str(delivery.id))
    deliver_auth_email.run(str(delivery.id))
    delivery.refresh_from_db()
    assert delivery.status == AuthEmailDelivery.Status.SENT
    assert delivery.attempts == 1
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_provider_failure_has_bounded_durable_retries(
    user, settings, monkeypatch, django_capture_on_commit_callbacks
):
    settings.AUTH_EMAIL_MAX_ATTEMPTS = 2
    settings.AUTH_EMAIL_RETRY_BACKOFF_SECONDS = (0,)
    with django_capture_on_commit_callbacks(execute=False):
        delivery = queue_password_reset(user)

    def unavailable(*_args, **_kwargs):
        raise RuntimeError("provider internals must be sanitized")

    monkeypatch.setattr("accounts.tasks.send_auth_email", unavailable)
    with pytest.raises(
        AuthEmailDeliveryUnavailable,
        match="authentication email delivery unavailable",
    ):
        deliver_auth_email.run(str(delivery.id))
    delivery.refresh_from_db()
    assert delivery.status == AuthEmailDelivery.Status.PENDING
    assert delivery.attempts == 1
    assert delivery.last_error_kind == "provider_unavailable"

    deliver_auth_email.run(str(delivery.id))
    delivery.refresh_from_db()
    assert delivery.status == AuthEmailDelivery.Status.FAILED
    assert delivery.attempts == 2
    assert delivery.last_error_kind == "provider_unavailable"


@pytest.mark.django_db
def test_crash_lease_replay_reuses_same_action_credential(user, django_capture_on_commit_callbacks):
    from accounts.tasks import _claim_delivery

    with django_capture_on_commit_callbacks(execute=False):
        delivery = queue_password_reset(user)
    first_delivery, first_raw = _claim_delivery(str(delivery.id))
    first_delivery.processing_expires_at = timezone.now()
    first_delivery.save(update_fields=("processing_expires_at", "updated_at"))
    second_delivery, second_raw = _claim_delivery(str(delivery.id))
    assert first_raw == second_raw
    assert second_delivery.attempts == 2
    assert EmailActionToken.objects.filter(user=user, used_at__isnull=True).count() == 1


@pytest.mark.django_db
def test_secret_key_fallback_keeps_pending_delivery_recoverable(
    user, settings, django_capture_on_commit_callbacks
):
    with django_capture_on_commit_callbacks(execute=False):
        delivery = queue_verification(user)
    original = delivery.action_token.derive_raw()
    old_secret = settings.SECRET_KEY
    settings.SECRET_KEY = "rotated-test-secret"
    settings.SECRET_KEY_FALLBACKS = [old_secret]
    assert delivery.action_token.derive_raw() == original


@pytest.mark.django_db
def test_reset_revokes_all_native_devices_and_web_session(user):
    first, first_raw = NativeSession.issue(user)
    second, second_raw = NativeSession.issue(user)
    web = APIClient()
    web.force_login(user)
    _, reset_raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    response = web.post(
        "/api/v1/auth/password-reset/confirm/",
        {"token": reset_raw, "new_password": REPLACEMENT},
        format="json",
    )
    assert response.status_code == 200
    assert web.get("/api/v1/auth/me/").status_code in (401, 403)
    first.refresh_from_db()
    second.refresh_from_db()
    assert first.revoked_at is not None
    assert second.revoked_at is not None
    for raw in (first_raw, second_raw):
        native = APIClient()
        native.credentials(HTTP_AUTHORIZATION=f"Bearer {raw}")
        assert native.get("/api/v1/auth/me/").status_code == 401


@pytest.mark.django_db
def test_bearer_scheme_is_case_insensitive_and_malformed_values_fail(user):
    _, raw = NativeSession.issue(user)
    for scheme in ("Bearer", "bearer", "BEARER"):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"{scheme} {raw}")
        assert client.get("/api/v1/auth/me/").status_code == 200
    for value in ("Bearer", "Bearer too many fields", "Basic credential"):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=value)
        assert client.get("/api/v1/auth/me/").status_code in (401, 403)


@override_settings(TRUST_HEROKU_ROUTER_IP=True)
def test_heroku_ip_contract_uses_rightmost_router_appended_address():
    factory = APIRequestFactory()
    request = factory.get(
        "/",
        HTTP_X_FORWARDED_FOR="198.51.100.99, 203.0.113.7",
        REMOTE_ADDR="10.0.0.1",
    )
    assert client_ip(request) == "203.0.113.7"


@override_settings(TRUST_HEROKU_ROUTER_IP=True)
@pytest.mark.parametrize(
    ("forwarded", "remote", "expected"),
    [
        ("2001:0DB8:0:0::1", "10.0.0.1", "2001:db8::1"),
        ("forged, invalid", "192.0.2.8", "192.0.2.8"),
        ("", "192.0.2.9", "192.0.2.9"),
        ("198.51.100.1, 198.51.100.2, 198.51.100.3", "10.0.0.1", "198.51.100.3"),
    ],
)
def test_heroku_ip_contract_handles_ipv6_missing_and_shared_proxies(forwarded, remote, expected):
    request = APIRequestFactory().get("/", HTTP_X_FORWARDED_FOR=forwarded, REMOTE_ADDR=remote)
    assert client_ip(request) == expected


def test_identifier_casing_cannot_bypass_throttle(settings):
    settings.AUTH_RATE_LIMITS["native_session"] = (1, 60)
    enforce_rate_limit("native_session", ip="identity", identity="Learner@Example.COM")
    with pytest.raises(Throttled):
        enforce_rate_limit("native_session", ip="identity", identity="learner@example.com")


def test_kvs_outage_fails_authentication_rate_limit_closed(monkeypatch):
    def unavailable(*_args, **_kwargs):
        raise RedisError

    monkeypatch.setattr(cache, "add", unavailable)
    with pytest.raises(AuthenticationRateLimitUnavailable):
        enforce_rate_limit("login", ip="192.0.2.10")
    response = APIClient().post(
        "/api/v1/auth/native/session/",
        {"email": "learner@example.com", "password": PASSWORD},
        format="json",
    )
    assert response.status_code == 503
    assert response.json() == {"detail": "Authentication is temporarily unavailable."}


@override_settings(
    SECURE_SSL_REDIRECT=True,
    SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO", "https"),
    SESSION_COOKIE_SECURE=True,
    CSRF_COOKIE_SECURE=True,
)
def test_deployed_https_redirect_and_forwarded_https_no_loop():
    client = APIClient()
    redirected = client.get("/api/v1/auth/csrf/")
    assert redirected.status_code in (301, 302)
    assert redirected["Location"].startswith("https://")
    forwarded = client.get("/api/v1/auth/csrf/", HTTP_X_FORWARDED_PROTO="https")
    assert forwarded.status_code == 200
    assert forwarded.cookies["csrftoken"]["secure"] is True
