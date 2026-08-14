from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit

import pytest
from django.contrib.auth import authenticate
from django.core import mail
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APIClient, APIRequestFactory

from accounts.models import EmailActionToken, NativeSession, User, hash_secret
from accounts.permissions import IsResourceOwner

PASSWORD = "Climb-ready-passphrase-47!"


@pytest.fixture(autouse=True)
def clear_rate_limits():
    cache.clear()


@pytest.fixture
def user(db):
    return User.objects.create_user("Learner@Example.COM", "Future_Lawyer", PASSWORD)


def token_from_email() -> str:
    url = next(part for part in mail.outbox[-1].body.split() if part.startswith("http"))
    parsed = urlsplit(url)
    assert "token" not in parse_qs(parsed.query)
    return parse_qs(parsed.fragment)["token"][0]


def csrf_client():
    client = APIClient(enforce_csrf_checks=True)
    token = client.get("/api/v1/auth/csrf/").json()["csrf_token"]
    return client, token


@pytest.mark.django_db
def test_user_identity_normalization_hashing_and_rules():
    user = User.objects.create_user(" Name@Example.COM ", "Climber_One", PASSWORD)
    assert user.email == "name@example.com"
    assert user.username == "climber_one"
    assert user.check_password(PASSWORD)
    assert user.password != PASSWORD
    assert authenticate(email="name@example.com", password=PASSWORD) == user
    with pytest.raises(ValidationError):
        User.objects.create_user("name@example.com", "different", PASSWORD)
    with pytest.raises(ValidationError):
        User.objects.create_user("other@example.com", "CLIMBER_ONE", PASSWORD)
    with pytest.raises(ValidationError):
        User.objects.create_user("reserved@example.com", "admin", PASSWORD)


@pytest.mark.django_db
def test_signup_requires_csrf_and_creates_rotated_session(
    django_capture_on_commit_callbacks,
):
    insecure = APIClient(enforce_csrf_checks=True)
    payload = {"email": "new@example.com", "username": "new_climber", "password": PASSWORD}
    assert insecure.post("/api/v1/auth/signup/", payload, format="json").status_code == 403
    client, csrf = csrf_client()
    old_key = client.session.session_key
    with django_capture_on_commit_callbacks(execute=True):
        response = client.post(
            "/api/v1/auth/signup/", payload, format="json", HTTP_X_CSRFTOKEN=csrf
        )
    assert response.status_code == 201
    assert response.json()["username"] == "new_climber"
    assert client.session.session_key != old_key
    assert len(mail.outbox) == 1
    assert client.get("/api/v1/auth/me/").status_code == 200


@pytest.mark.django_db
def test_web_login_session_rotation_csrf_and_logout_invalidation(user):
    client, csrf = csrf_client()
    before = client.session.session_key
    response = client.post(
        "/api/v1/auth/login/",
        {"email": user.email, "password": PASSWORD},
        format="json",
        HTTP_X_CSRFTOKEN=csrf,
    )
    assert response.status_code == 200
    assert client.session.session_key != before
    assert client.get("/api/v1/auth/session/").json()["authenticated"] is True
    assert client.post("/api/v1/auth/logout/", {}, format="json").status_code == 403
    csrf = client.get("/api/v1/auth/csrf/").json()["csrf_token"]
    assert (
        client.post("/api/v1/auth/logout/", {}, format="json", HTTP_X_CSRFTOKEN=csrf).status_code
        == 204
    )
    assert client.get("/api/v1/auth/me/").status_code in (401, 403)


@pytest.mark.django_db
def test_verification_token_is_hashed_rotated_expiring_and_single_use(
    user, django_capture_on_commit_callbacks
):
    client, csrf = csrf_client()
    with django_capture_on_commit_callbacks(execute=True):
        client.post(
            "/api/v1/auth/verification/request/",
            {"email": user.email},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        )
    first = token_from_email()
    with django_capture_on_commit_callbacks(execute=True):
        client.post(
            "/api/v1/auth/verification/request/",
            {"email": user.email},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        )
    second = token_from_email()
    assert first != second
    assert not EmailActionToken.objects.filter(token_hash=first).exists()
    assert EmailActionToken.objects.filter(
        token_hash=hash_secret(first), used_at__isnull=False
    ).exists()
    assert (
        client.post(
            "/api/v1/auth/verification/confirm/",
            {"token": first},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        ).status_code
        == 400
    )
    assert (
        client.post(
            "/api/v1/auth/verification/confirm/",
            {"token": second},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/auth/verification/confirm/",
            {"token": second},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        ).status_code
        == 400
    )
    user.refresh_from_db()
    assert user.is_email_verified


@pytest.mark.django_db
def test_expired_token_and_wrong_purpose_are_rejected(user):
    token, raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    token.expires_at = timezone.now()
    token.save(update_fields=["expires_at"])
    client, csrf = csrf_client()
    assert (
        client.post(
            "/api/v1/auth/password-reset/confirm/",
            {"token": raw, "new_password": "Different-passphrase-82!"},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        ).status_code
        == 400
    )
    _, raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    assert (
        client.post(
            "/api/v1/auth/verification/confirm/",
            {"token": raw},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        ).status_code
        == 400
    )


@pytest.mark.django_db
def test_password_reset_is_non_enumerating_single_use_and_revokes_sessions(
    user, django_capture_on_commit_callbacks
):
    native, _ = NativeSession.issue(user)
    client = APIClient()
    client, csrf = csrf_client()
    with django_capture_on_commit_callbacks(execute=True):
        existing = client.post(
            "/api/v1/auth/password-reset/request/",
            {"email": user.email},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        )
    raw = token_from_email()
    assert (
        client.post(
            "/api/v1/auth/password-reset/confirm/",
            {"token": raw, "new_password": "Different-passphrase-82!"},
            format="json",
        ).status_code
        == 403
    )
    missing = client.post(
        "/api/v1/auth/password-reset/request/",
        {"email": "missing@example.com"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf,
    )
    assert existing.status_code == missing.status_code == 200
    assert existing.json() == missing.json()
    replacement = "Different-passphrase-82!"
    assert (
        client.post(
            "/api/v1/auth/password-reset/confirm/",
            {"token": raw, "new_password": replacement},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/auth/password-reset/confirm/",
            {"token": raw, "new_password": replacement},
            format="json",
            HTTP_X_CSRFTOKEN=csrf,
        ).status_code
        == 400
    )
    user.refresh_from_db()
    native.refresh_from_db()
    assert user.check_password(replacement)
    assert native.revoked_at is not None


@pytest.mark.django_db
def test_weak_password_does_not_consume_reset_token(user):
    _, raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    client, csrf = csrf_client()
    response = client.post(
        "/api/v1/auth/password-reset/confirm/",
        {"token": raw, "new_password": "password"},
        format="json",
        HTTP_X_CSRFTOKEN=csrf,
    )
    assert response.status_code == 400
    assert EmailActionToken.objects.get(token_hash=hash_secret(raw)).used_at is None


@pytest.mark.django_db
def test_native_session_issuance_authentication_and_revocation(user):
    client = APIClient()
    response = client.post(
        "/api/v1/auth/native/session/", {"email": user.email, "password": PASSWORD}, format="json"
    )
    assert response.status_code == 200
    assert response["Cache-Control"] == "no-store"
    raw = response.json()["token"]
    assert NativeSession.objects.filter(token_hash=hash_secret(raw)).exists()
    assert not NativeSession.objects.filter(token_hash=raw).exists()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {raw}")
    assert client.get("/api/v1/auth/me/").json()["username"] == user.username
    assert client.post("/api/v1/auth/native/session/revoke/").status_code == 204
    assert client.get("/api/v1/auth/me/").status_code in (401, 403)


@pytest.mark.django_db
def test_expired_native_session_is_rejected(user):
    session, raw = NativeSession.issue(user)
    session.expires_at = timezone.now()
    session.save(update_fields=["expires_at"])
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {raw}")
    assert client.get("/api/v1/auth/me/").status_code == 401


@pytest.mark.django_db
def test_native_signup_uses_same_identity_and_issues_secure_session(
    django_capture_on_commit_callbacks,
):
    client = APIClient()
    with django_capture_on_commit_callbacks(execute=True):
        response = client.post(
            "/api/v1/auth/native/signup/",
            {
                "email": "native@example.com",
                "username": "native_climber",
                "password": PASSWORD,
            },
            format="json",
        )
    assert response.status_code == 201
    assert response.json()["user"]["username"] == "native_climber"
    assert NativeSession.objects.filter(token_hash=hash_secret(response.json()["token"])).exists()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_native_reset_request_is_non_enumerating(user):
    client = APIClient()
    existing = client.post(
        "/api/v1/auth/native/password-reset/request/", {"email": user.email}, format="json"
    )
    missing = client.post(
        "/api/v1/auth/native/password-reset/request/",
        {"email": "missing@example.com"},
        format="json",
    )
    assert existing.status_code == missing.status_code == 200
    assert existing.json() == missing.json()


@pytest.mark.django_db
def test_auth_rate_limit_and_generic_invalid_login(user, settings):
    settings.AUTH_RATE_LIMITS["native_session"] = (2, 60)
    client = APIClient()
    payload = {"email": user.email, "password": "wrong"}
    assert client.post("/api/v1/auth/native/session/", payload, format="json").status_code == 400
    assert client.post("/api/v1/auth/native/session/", payload, format="json").status_code == 400
    assert client.post("/api/v1/auth/native/session/", payload, format="json").status_code == 429


@pytest.mark.django_db
def test_anonymous_me_private_email_and_cross_user_boundary(user):
    client = APIClient()
    assert client.get("/api/v1/auth/me/").status_code in (401, 403)
    other = User.objects.create_user("other@example.com", "other_climber", PASSWORD)
    request = APIRequestFactory().get("/")
    request.user = user
    permission = IsResourceOwner()
    assert permission.has_object_permission(request, None, SimpleNamespace(owner=user))
    assert not permission.has_object_permission(request, None, SimpleNamespace(owner=other))


@pytest.mark.django_db
def test_authenticated_private_email_response_is_not_cacheable(user):
    client = APIClient()
    client.force_authenticate(user)
    response = client.get("/api/v1/auth/me/")
    assert response.json()["email"] == user.email
    assert response["Cache-Control"] == "no-store"
