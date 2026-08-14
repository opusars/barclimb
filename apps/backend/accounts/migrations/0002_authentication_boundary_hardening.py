import uuid

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def populate_derivation_ids(apps, schema_editor):
    token_model = apps.get_model("accounts", "EmailActionToken")
    for token in token_model.objects.filter(derivation_id__isnull=True).iterator():
        token.derivation_id = uuid.uuid4()
        token.save(update_fields=("derivation_id",))


class Migration(migrations.Migration):
    dependencies = [("accounts", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="auth_generation",
            field=models.PositiveBigIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="nativesession",
            name="auth_generation",
            field=models.PositiveBigIntegerField(default=1),
        ),
        migrations.AddField(
            model_name="emailactiontoken",
            name="derivation_id",
            field=models.UUIDField(null=True),
        ),
        migrations.RunPython(populate_derivation_ids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="emailactiontoken",
            name="derivation_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.CreateModel(
            name="AuthEmailDelivery",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "purpose",
                    models.CharField(
                        choices=[
                            ("VERIFY_EMAIL", "Verify email"),
                            ("RESET_PASSWORD", "Reset password"),
                        ],
                        max_length=32,
                    ),
                ),
                ("is_decoy", models.BooleanField(default=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "Pending"),
                            ("PROCESSING", "Processing"),
                            ("SENT", "Sent"),
                            ("FAILED", "Failed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="PENDING",
                        max_length=16,
                    ),
                ),
                ("attempts", models.PositiveSmallIntegerField(default=0)),
                ("next_attempt_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("processing_expires_at", models.DateTimeField(blank=True, null=True)),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("last_error_kind", models.CharField(blank=True, max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "action_token",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.emailactiontoken",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["status", "next_attempt_at"], name="auth_email_due_idx")
                ],
                "constraints": [
                    models.CheckConstraint(
                        condition=(
                            models.Q(
                                ("action_token__isnull", True),
                                ("is_decoy", True),
                                ("user__isnull", True),
                            )
                            | models.Q(
                                ("action_token__isnull", False),
                                ("is_decoy", False),
                                ("user__isnull", False),
                            )
                        ),
                        name="auth_email_decoy_or_action",
                    )
                ],
            },
        ),
    ]
