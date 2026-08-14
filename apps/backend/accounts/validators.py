import re

from django.core.exceptions import ValidationError

USERNAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{2,29}$")
RESERVED_USERNAMES = frozenset(
    {
        "account",
        "admin",
        "api",
        "barclimb",
        "help",
        "moderator",
        "official",
        "root",
        "staff",
        "support",
    }
)


def normalize_username(value: str) -> str:
    return value.strip().lower()


def validate_username(value: str) -> None:
    if not USERNAME_PATTERN.fullmatch(value):
        raise ValidationError(
            "Use 3–30 lowercase letters, numbers, or underscores; begin with a letter."
        )
    if value in RESERVED_USERNAMES:
        raise ValidationError("This username is reserved.")
