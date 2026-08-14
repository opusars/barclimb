from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Event

import pytest
from django.db import IntegrityError, close_old_connections, connection, connections, transaction

from accounts.models import EmailActionToken, NativeSession, User
from accounts.services import issue_native_session_after_revalidation

PASSWORD = "Climb-ready-passphrase-47!"
REPLACEMENT = "Different-passphrase-82!"


def _postgres_only():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL row-lock semantics are authoritative for this test")


def _thread_call(function, *args):
    close_old_connections()
    try:
        return function(*args)
    finally:
        connections.close_all()


@pytest.mark.django_db(transaction=True)
def test_concurrent_reset_blocks_stale_password_native_issuance():
    _postgres_only()
    user = User.objects.create_user("race@example.com", "race_climber", PASSWORD)
    _, reset_raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    reset_has_lock = Event()
    allow_reset_commit = Event()
    login_started = Event()

    def reset_password():
        with transaction.atomic():
            token = EmailActionToken.consume(reset_raw, EmailActionToken.Purpose.RESET_PASSWORD)
            assert token is not None
            token.user.set_password(REPLACEMENT)
            token.user.auth_generation += 1
            token.user.save(update_fields=("password", "auth_generation"))
            NativeSession.objects.filter(user=token.user, revoked_at__isnull=True).update(
                revoked_at=token.used_at
            )
            reset_has_lock.set()
            assert allow_reset_commit.wait(timeout=5)

    def stale_login():
        stale_user = User.objects.get(pk=user.pk)
        login_started.set()
        return issue_native_session_after_revalidation(stale_user, PASSWORD)

    with ThreadPoolExecutor(max_workers=2) as pool:
        reset_future = pool.submit(_thread_call, reset_password)
        assert reset_has_lock.wait(timeout=5)
        login_future = pool.submit(_thread_call, stale_login)
        assert login_started.wait(timeout=5)
        assert not login_future.done()
        allow_reset_commit.set()
        reset_future.result(timeout=5)
        assert login_future.result(timeout=5) is None
    assert NativeSession.objects.filter(user=user).count() == 0


@pytest.mark.django_db(transaction=True)
def test_session_issued_before_concurrent_reset_is_deterministically_invalidated():
    _postgres_only()
    user = User.objects.create_user("devices@example.com", "device_climber", PASSWORD)
    _, reset_raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    login_has_lock = Event()
    allow_login_commit = Event()
    reset_started = Event()

    def issue_while_locked():
        with transaction.atomic():
            locked = User.objects.select_for_update().get(pk=user.pk)
            assert locked.check_password(PASSWORD)
            session, _ = NativeSession.issue(locked)
            login_has_lock.set()
            assert allow_login_commit.wait(timeout=5)
            return session.pk

    def reset_password():
        reset_started.set()
        with transaction.atomic():
            token = EmailActionToken.consume(reset_raw, EmailActionToken.Purpose.RESET_PASSWORD)
            assert token is not None
            token.user.set_password(REPLACEMENT)
            token.user.auth_generation += 1
            token.user.save(update_fields=("password", "auth_generation"))
            NativeSession.objects.filter(user=token.user, revoked_at__isnull=True).update(
                revoked_at=token.used_at
            )

    with ThreadPoolExecutor(max_workers=2) as pool:
        login_future = pool.submit(_thread_call, issue_while_locked)
        assert login_has_lock.wait(timeout=5)
        reset_future = pool.submit(_thread_call, reset_password)
        assert reset_started.wait(timeout=5)
        assert not reset_future.done()
        allow_login_commit.set()
        session_id = login_future.result(timeout=5)
        reset_future.result(timeout=5)
    session = NativeSession.objects.select_related("user").get(pk=session_id)
    assert session.revoked_at is not None
    assert not session.is_valid


@pytest.mark.django_db(transaction=True)
def test_concurrent_token_consume_and_reissue_serialize_on_user():
    _postgres_only()
    user = User.objects.create_user("token@example.com", "token_climber", PASSWORD)
    old_token, old_raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    consume_has_lock = Event()
    allow_consume_commit = Event()
    reissue_started = Event()

    def consume():
        with transaction.atomic():
            token = EmailActionToken.consume(old_raw, EmailActionToken.Purpose.RESET_PASSWORD)
            assert token is not None
            consume_has_lock.set()
            assert allow_consume_commit.wait(timeout=5)

    def reissue():
        current = User.objects.get(pk=user.pk)
        reissue_started.set()
        return EmailActionToken.issue(current, EmailActionToken.Purpose.RESET_PASSWORD)[0].pk

    with ThreadPoolExecutor(max_workers=2) as pool:
        consume_future = pool.submit(_thread_call, consume)
        assert consume_has_lock.wait(timeout=5)
        reissue_future = pool.submit(_thread_call, reissue)
        assert reissue_started.wait(timeout=5)
        assert not reissue_future.done()
        allow_consume_commit.set()
        consume_future.result(timeout=5)
        new_token_id = reissue_future.result(timeout=5)
    old_token.refresh_from_db()
    assert old_token.used_at is not None
    assert (
        EmailActionToken.objects.filter(
            user=user,
            purpose=EmailActionToken.Purpose.RESET_PASSWORD,
            used_at__isnull=True,
            pk=new_token_id,
        ).count()
        == 1
    )


@pytest.mark.django_db(transaction=True)
def test_duplicate_signup_race_creates_one_identity():
    _postgres_only()
    barrier = Barrier(2)

    def create_identity(username):
        barrier.wait(timeout=5)
        try:
            with transaction.atomic():
                User.objects.create_user("same@example.com", username, PASSWORD)
            return "created"
        except IntegrityError:
            return "conflict"

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(_thread_call, create_identity, "climber_one")
        second = pool.submit(_thread_call, create_identity, "climber_two")
        outcomes = {
            first.result(timeout=5),
            second.result(timeout=5),
        }
    assert outcomes == {"created", "conflict"}
    assert User.objects.filter(email="same@example.com").count() == 1
