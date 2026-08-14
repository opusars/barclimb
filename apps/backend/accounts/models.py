import base64
import hashlib
import hmac
import secrets
import uuid
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
    auth_generation = models.PositiveBigIntegerField(default=1)
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
    derivation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
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

    def _raw_for_secret(self, secret: str) -> str:
        message = (
            f"barclimb-auth-action-v1:{self.derivation_id}:{self.user_id}:{self.purpose}"
        ).encode()
        digest = hmac.new(secret.encode(), message, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()

    def derive_raw(self) -> str:
        for secret in (settings.SECRET_KEY, *settings.SECRET_KEY_FALLBACKS):
            raw = self._raw_for_secret(secret)
            if hmac.compare_digest(self.token_hash, hash_secret(raw)):
                return raw
        raise ValueError("Email action token cannot be derived with an active signing key")

    @classmethod
    def _issue_locked(cls, user: User, purpose: str) -> tuple["EmailActionToken", str]:
        now = timezone.now()
        cls.objects.filter(user=user, purpose=purpose, used_at__isnull=True).update(used_at=now)
        AuthEmailDelivery.objects.filter(
            user=user,
            purpose=purpose,
            status__in=(
                AuthEmailDelivery.Status.PENDING,
                AuthEmailDelivery.Status.PROCESSING,
            ),
        ).update(status=AuthEmailDelivery.Status.CANCELLED, updated_at=now)
        token = cls(
            user=user,
            purpose=purpose,
            token_hash="",
            expires_at=now + timedelta(seconds=settings.AUTH_ACTION_TOKEN_TTL_SECONDS),
        )
        raw = token._raw_for_secret(settings.SECRET_KEY)
        token.token_hash = hash_secret(raw)
        token.save()
        return token, raw

    @classmethod
    def issue(cls, user: User, purpose: str) -> tuple["EmailActionToken", str]:
        with transaction.atomic():
            locked_user = User.objects.select_for_update().get(pk=user.pk)
            return cls._issue_locked(locked_user, purpose)

    @classmethod
    def consume(cls, raw: str, purpose: str) -> "EmailActionToken | None":
        token_hash = hash_secret(raw)
        user_id = (
            cls.objects.filter(token_hash=token_hash, purpose=purpose)
            .values_list("user_id", flat=True)
            .first()
        )
        if user_id is None:
            return None
        User.objects.select_for_update().get(pk=user_id)
        try:
            token = (
                cls.objects.select_for_update()
                .select_related("user")
                .get(token_hash=token_hash, purpose=purpose)
            )
        except cls.DoesNotExist:
            return None
        now = timezone.now()
        if token.used_at or token.expires_at <= now:
            return None
        token.used_at = now
        token.save(update_fields=["used_at"])
        return token


class AuthEmailDelivery(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSING = "PROCESSING", "Processing"
        SENT = "SENT", "Sent"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    action_token = models.OneToOneField(
        EmailActionToken, on_delete=models.CASCADE, null=True, blank=True
    )
    purpose = models.CharField(max_length=32, choices=EmailActionToken.Purpose.choices)
    is_decoy = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    attempts = models.PositiveSmallIntegerField(default=0)
    next_attempt_at = models.DateTimeField(default=timezone.now)
    processing_expires_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    last_error_kind = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=("status", "next_attempt_at"), name="auth_email_due_idx")]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(is_decoy=True, user__isnull=True, action_token__isnull=True)
                    | Q(is_decoy=False, user__isnull=False, action_token__isnull=False)
                ),
                name="auth_email_decoy_or_action",
            )
        ]

    def __str__(self) -> str:
        return f"{self.purpose} delivery {self.id} ({self.status})"


class NativeSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)
    auth_generation = models.PositiveBigIntegerField(default=1)
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
            auth_generation=user.auth_generation,
        )
        return session, raw

    @property
    def is_valid(self) -> bool:
        return (
            self.revoked_at is None
            and self.expires_at > timezone.now()
            and self.user.is_active
            and self.auth_generation == self.user.auth_generation
        )

    def revoke(self) -> None:
        if self.revoked_at is None:
            self.revoked_at = timezone.now()
            self.save(update_fields=["revoked_at"])
