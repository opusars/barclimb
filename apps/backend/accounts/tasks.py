import secrets

from celery import shared_task

from .models import User
from .services import send_password_reset, send_verification


def enqueue_verification(user_id: int | None) -> None:
    deliver_verification.apply_async(
        args=[user_id if user_id is not None else -secrets.randbelow(2**31) - 1],
        argsrepr="(<account>,)",
    )


def enqueue_password_reset(user_id: int | None) -> None:
    deliver_password_reset.apply_async(
        args=[user_id if user_id is not None else -secrets.randbelow(2**31) - 1],
        argsrepr="(<account>,)",
    )


@shared_task(name="identity.deliver_verification", ignore_result=True)
def deliver_verification(user_id: int) -> None:
    user = User.objects.filter(pk=user_id, is_active=True, is_email_verified=False).first()
    if user:
        send_verification(user)


@shared_task(name="identity.deliver_password_reset", ignore_result=True)
def deliver_password_reset(user_id: int) -> None:
    user = User.objects.filter(pk=user_id, is_active=True).first()
    if user:
        send_password_reset(user)
