import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import validate_email
from django.db import models, transaction
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils import timezone

from .validators import normalize_username, validate_username


def normalize_email(value: str) -> str:
    return BaseUserManager.normalize_email(value).strip().lower()


def hash_secret(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email: str, username: str, password: str | None = None, **extra):
        if not email or not username:
            raise ValueError("Email and username are required")
        email = normalize_email(email)
        username = normalize_username(username)
        validate_email(email)
        validate_username(username)
        user = self.model(email=email, username=username, **extra)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, username: str, password: str, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        extra.setdefault("is_email_verified", True)
        if not extra["is_staff"] or not extra["is_superuser"]:
            raise ValueError("Superuser requires staff and superuser status")
        return self.create_user(email, username, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[validate_email])
    username = models.CharField(max_length=30, unique=True, validators=[validate_username])
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower("email"), name="unique_normalized_user_email"),
            models.UniqueConstraint(Lower("username"), name="unique_normalized_username"),
        ]

    def save(self, *args, **kwargs):
        self.email = normalize_email(self.email)
        self.username = normalize_username(self.username)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.username


class EmailActionToken(models.Model):
    class Purpose(models.TextChoices):
        VERIFY_EMAIL = "VERIFY_EMAIL", "Verify email"
        RESET_PASSWORD = "RESET_PASSWORD", "Reset password"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=32, choices=Purpose.choices)
    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "purpose"),
                condition=Q(used_at__isnull=True),
                name="one_active_email_action_per_purpose",
            )
        ]

    def __str__(self) -> str:
        return f"{self.purpose} token for user {self.user_id}"

    @classmethod
    def issue(cls, user: User, purpose: str) -> tuple["EmailActionToken", str]:
        with transaction.atomic():
            User.objects.select_for_update().get(pk=user.pk)
            now = timezone.now()
            cls.objects.filter(user=user, purpose=purpose, used_at__isnull=True).update(used_at=now)
            raw = secrets.token_urlsafe(32)
            token = cls.objects.create(
                user=user,
                purpose=purpose,
                token_hash=hash_secret(raw),
                expires_at=now + timedelta(seconds=settings.AUTH_ACTION_TOKEN_TTL_SECONDS),
            )
        return token, raw

    @classmethod
    def consume(cls, raw: str, purpose: str) -> "EmailActionToken | None":
        try:
            token = (
                cls.objects.select_for_update()
                .select_related("user")
                .get(token_hash=hash_secret(raw), purpose=purpose)
            )
        except cls.DoesNotExist:
            return None
        now = timezone.now()
        if token.used_at or token.expires_at <= now:
            return None
        token.used_at = now
        token.save(update_fields=["used_at"])
        return token


class NativeSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Native session for user {self.user_id}"

    @classmethod
    def issue(cls, user: User) -> tuple["NativeSession", str]:
        raw = secrets.token_urlsafe(32)
        session = cls.objects.create(
            user=user,
            token_hash=hash_secret(raw),
            expires_at=timezone.now() + timedelta(seconds=settings.NATIVE_SESSION_TTL_SECONDS),
        )
        return session, raw

    @property
    def is_valid(self) -> bool:
        return self.revoked_at is None and self.expires_at > timezone.now() and self.user.is_active

    def revoke(self) -> None:
        if self.revoked_at is None:
            self.revoked_at = timezone.now()
            self.save(update_fields=["revoked_at"])
