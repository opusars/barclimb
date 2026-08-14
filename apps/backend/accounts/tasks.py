from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import AuthEmailDelivery
from .services import publish_due_auth_email_deliveries, send_auth_email


class AuthEmailDeliveryUnavailable(Exception):
    """Sanitized retry signal that never includes provider or recipient details."""


def _claim_delivery(delivery_id: str):
    with transaction.atomic():
        delivery = AuthEmailDelivery.objects.select_for_update().get(pk=delivery_id)
        now = timezone.now()
        if delivery.status in {
            AuthEmailDelivery.Status.SENT,
            AuthEmailDelivery.Status.FAILED,
            AuthEmailDelivery.Status.CANCELLED,
        }:
            return None
        if (
            delivery.status == AuthEmailDelivery.Status.PROCESSING
            and delivery.processing_expires_at
            and delivery.processing_expires_at > now
        ):
            return None
        if delivery.next_attempt_at > now:
            return None
        if delivery.is_decoy:
            delivery.status = AuthEmailDelivery.Status.SENT
            delivery.sent_at = now
            delivery.processing_expires_at = None
            delivery.save(
                update_fields=("status", "sent_at", "processing_expires_at", "updated_at")
            )
            return None
        token = delivery.action_token
        if (
            token is None
            or token.used_at is not None
            or token.expires_at <= now
            or token.purpose != delivery.purpose
            or delivery.user is None
            or not delivery.user.is_active
        ):
            delivery.status = AuthEmailDelivery.Status.CANCELLED
            delivery.processing_expires_at = None
            delivery.save(update_fields=("status", "processing_expires_at", "updated_at"))
            return None
        if delivery.attempts >= settings.AUTH_EMAIL_MAX_ATTEMPTS:
            delivery.status = AuthEmailDelivery.Status.FAILED
            delivery.last_error_kind = "attempt_limit"
            delivery.processing_expires_at = None
            delivery.save(
                update_fields=(
                    "status",
                    "last_error_kind",
                    "processing_expires_at",
                    "updated_at",
                )
            )
            return None
        raw_token = token.derive_raw()
        delivery.status = AuthEmailDelivery.Status.PROCESSING
        delivery.attempts += 1
        delivery.processing_expires_at = now + timedelta(
            seconds=settings.AUTH_EMAIL_PROCESSING_LEASE_SECONDS
        )
        delivery.last_error_kind = ""
        delivery.save(
            update_fields=(
                "status",
                "attempts",
                "processing_expires_at",
                "last_error_kind",
                "updated_at",
            )
        )
        return delivery, raw_token


def _record_success(delivery_id: str) -> None:
    with transaction.atomic():
        delivery = AuthEmailDelivery.objects.select_for_update().get(pk=delivery_id)
        if delivery.status != AuthEmailDelivery.Status.PROCESSING:
            return
        delivery.status = AuthEmailDelivery.Status.SENT
        delivery.sent_at = timezone.now()
        delivery.processing_expires_at = None
        delivery.save(update_fields=("status", "sent_at", "processing_expires_at", "updated_at"))


def _record_failure(delivery_id: str) -> int | None:
    with transaction.atomic():
        delivery = AuthEmailDelivery.objects.select_for_update().get(pk=delivery_id)
        if delivery.status != AuthEmailDelivery.Status.PROCESSING:
            return None
        if delivery.attempts >= settings.AUTH_EMAIL_MAX_ATTEMPTS:
            delivery.status = AuthEmailDelivery.Status.FAILED
            delivery.last_error_kind = "provider_unavailable"
            delivery.processing_expires_at = None
            delivery.save(
                update_fields=(
                    "status",
                    "last_error_kind",
                    "processing_expires_at",
                    "updated_at",
                )
            )
            return None
        backoff = settings.AUTH_EMAIL_RETRY_BACKOFF_SECONDS[
            min(delivery.attempts - 1, len(settings.AUTH_EMAIL_RETRY_BACKOFF_SECONDS) - 1)
        ]
        delivery.status = AuthEmailDelivery.Status.PENDING
        delivery.last_error_kind = "provider_unavailable"
        delivery.processing_expires_at = None
        delivery.next_attempt_at = timezone.now() + timedelta(seconds=backoff)
        delivery.save(
            update_fields=(
                "status",
                "last_error_kind",
                "processing_expires_at",
                "next_attempt_at",
                "updated_at",
            )
        )
        return backoff


@shared_task(
    bind=True,
    name="identity.deliver_auth_email",
    ignore_result=True,
    max_retries=3,
)
def deliver_auth_email(self, delivery_id: str) -> None:
    claimed = _claim_delivery(delivery_id)
    if claimed is None:
        return
    delivery, raw_token = claimed
    try:
        send_auth_email(delivery, raw_token)
    except Exception:
        backoff = _record_failure(delivery_id)
        if backoff is not None:
            raise self.retry(
                exc=AuthEmailDeliveryUnavailable("authentication email delivery unavailable"),
                countdown=backoff,
                max_retries=settings.AUTH_EMAIL_MAX_ATTEMPTS - 1,
            ) from None
        return
    _record_success(delivery_id)


@shared_task(
    name="identity.recover_auth_email_outbox",
    ignore_result=True,
)
def recover_auth_email_outbox() -> None:
    publish_due_auth_email_deliveries()
