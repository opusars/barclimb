from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail

from .models import EmailActionToken, User


def _action_url(path: str, token: str) -> str:
    base = settings.PUBLIC_BASE_URL.rstrip("/") or "http://localhost:5173"
    return f"{base}/{path}?{urlencode({'token': token})}"


def send_verification(user: User) -> None:
    _, raw = EmailActionToken.issue(user, EmailActionToken.Purpose.VERIFY_EMAIL)
    send_mail(
        "Verify your BarClimb email",
        f"Verify your email: {_action_url('verify-email', raw)}\n\nThis link expires in one hour.",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )


def send_password_reset(user: User) -> None:
    _, raw = EmailActionToken.issue(user, EmailActionToken.Purpose.RESET_PASSWORD)
    send_mail(
        "Reset your BarClimb password",
        (
            f"Reset your password: {_action_url('reset-password', raw)}\n\n"
            "This link expires in one hour."
        ),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
