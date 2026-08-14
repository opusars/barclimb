from functools import partial
from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from .models import AuthEmailDelivery, EmailActionToken, NativeSession, User


def action_url(path: str, token: str) -> str:
    base = settings.PUBLIC_BASE_URL.rstrip("/") or "http://localhost:5173"
    return f"{base}/{path}#{urlencode({'token': token})}"


def send_auth_email(delivery: AuthEmailDelivery, raw_token: str) -> None:
    if delivery.user is None:
        return
    if delivery.purpose == EmailActionToken.Purpose.VERIFY_EMAIL:
        subject = "Verify your BarClimb email"
        body = (
            f"Verify your email: {action_url('verify-email', raw_token)}\n\n"
            "This link expires in one hour."
        )
    elif delivery.purpose == EmailActionToken.Purpose.RESET_PASSWORD:
        subject = "Reset your BarClimb password"
        body = (
            f"Reset your password: {action_url('reset-password', raw_token)}\n\n"
            "This link expires in one hour."
        )
    else:
        raise ValueError("Unsupported authentication email purpose")
    if send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [delivery.user.email]) != 1:
        raise RuntimeError("authentication email provider accepted no message")


def _publish_delivery(delivery_id) -> bool:
    from .tasks import deliver_auth_email

    try:
        deliver_auth_email.apply_async(
            args=[str(delivery_id)],
            argsrepr="(<auth-email-delivery>,)",
            retry=True,
            retry_policy={
                "max_retries": settings.AUTH_EMAIL_PUBLISH_MAX_RETRIES,
                "interval_start": 0,
                "interval_step": 0.2,
                "interval_max": 1,
            },
        )
    except Exception:  # Broker errors must not roll back an already-committed account/request.
        return False
    return True


def queue_auth_email(user: User | None, purpose: str) -> AuthEmailDelivery:
    with transaction.atomic():
        if user is None:
            delivery = AuthEmailDelivery.objects.create(
                purpose=purpose,
                is_decoy=True,
            )
        else:
            locked_user = User.objects.select_for_update().get(pk=user.pk)
            token, _ = EmailActionToken._issue_locked(locked_user, purpose)
            delivery = AuthEmailDelivery.objects.create(
                user=locked_user,
                action_token=token,
                purpose=purpose,
            )
        transaction.on_commit(partial(_publish_delivery, delivery.id), robust=True)
    return delivery


def queue_verification(user: User | None) -> AuthEmailDelivery:
    return queue_auth_email(user, EmailActionToken.Purpose.VERIFY_EMAIL)


def queue_password_reset(user: User | None) -> AuthEmailDelivery:
    return queue_auth_email(user, EmailActionToken.Purpose.RESET_PASSWORD)


def issue_native_session_after_revalidation(
    user: User, raw_password: str
) -> tuple[NativeSession, str, User] | None:
    with transaction.atomic():
        locked_user = User.objects.select_for_update().get(pk=user.pk)
        if not locked_user.is_active or not locked_user.check_password(raw_password):
            return None
        session, raw = NativeSession.issue(locked_user)
        return session, raw, locked_user


def publish_due_auth_email_deliveries(*, limit: int = 100) -> int:
    now = timezone.now()
    ids = list(
        AuthEmailDelivery.objects.filter(
            Q(status=AuthEmailDelivery.Status.PENDING, next_attempt_at__lte=now)
            | Q(
                status=AuthEmailDelivery.Status.PROCESSING,
                processing_expires_at__lte=now,
            )
        )
        .order_by("next_attempt_at")
        .values_list("id", flat=True)[:limit]
    )
    return sum(1 for delivery_id in ids if _publish_delivery(delivery_id))
