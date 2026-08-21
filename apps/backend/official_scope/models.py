import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class OfficialSourceArtifact(models.Model):
    class SourceClass(models.TextChoices):
        OFFICIAL = "OFFICIAL", "Official"
        TEST_FIXTURE = "TEST_FIXTURE", "Test fixture"

    class Status(models.TextChoices):
        PUBLISHED = "PUBLISHED", "Published"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stable_id = models.CharField(max_length=160)
    source_authority = models.CharField(max_length=160)
    artifact_type = models.CharField(max_length=80)
    official_title = models.CharField(max_length=300)
    source_uri = models.URLField(max_length=1000, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    effective_end_date = models.DateField(null=True, blank=True)
    retrieved_at = models.DateTimeField(null=True, blank=True)
    content_sha256 = models.CharField(max_length=64)
    byte_length = models.PositiveBigIntegerField(null=True, blank=True)
    media_type = models.CharField(max_length=120, blank=True)
    storage_disposition = models.CharField(max_length=80, blank=True)
    rights_basis = models.TextField(blank=True)
    source_version = models.CharField(max_length=160)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PUBLISHED)
    supersedes = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="successors"
    )
    source_class = models.CharField(
        max_length=16, choices=SourceClass.choices, default=SourceClass.OFFICIAL
    )
    provenance_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("stable_id", "source_version"), name="official_artifact_identity_unique"
            ),
            models.CheckConstraint(
                condition=Q(content_sha256__regex=r"^[0-9a-f]{64}$"),
                name="official_artifact_sha256_format",
            ),
        ]
        indexes = [models.Index(fields=("source_authority", "artifact_type"))]

    def __str__(self):
        return f"{self.stable_id}@{self.source_version}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError(
                "Official source artifacts are immutable; register a new version."
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Official source artifacts cannot be deleted.")

    @property
    def has_been_superseded(self):
        return self.successors.exists()


class OfficialScopeVersion(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        VALIDATED = "VALIDATED", "Validated"
        ACTIVE = "ACTIVE", "Active"
        SUPERSEDED = "SUPERSEDED", "Superseded"

    class ReleaseClass(models.TextChoices):
        CURRENT = "CURRENT", "Current administration period"
        FUTURE = "FUTURE", "Known future administration period"
        TEST_FIXTURE = "TEST_FIXTURE", "Test fixture"

    EXAM_PROGRAM = "NEXTGEN_UBE"
    EXAM_COMPONENT = "NEXTGEN_CORE"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version_identifier = models.CharField(max_length=160, unique=True)
    exam_program = models.CharField(max_length=40, default=EXAM_PROGRAM)
    exam_component = models.CharField(max_length=40, default=EXAM_COMPONENT)
    is_national = models.BooleanField(default=True)
    jurisdiction = models.CharField(max_length=80, blank=True)
    normalized_sha256 = models.CharField(max_length=64, blank=True)
    administration_start = models.DateField(null=True, blank=True)
    administration_end = models.DateField(null=True, blank=True)
    release_class = models.CharField(
        max_length=16, choices=ReleaseClass.choices, default=ReleaseClass.CURRENT
    )
    normalization_report = models.JSONField(default=dict, blank=True)
    freshness_checked_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    source_artifacts = models.ManyToManyField(
        OfficialSourceArtifact, through="OfficialScopeSource", related_name="scope_versions"
    )
    validation_report = models.JSONField(default=dict, blank=True)
    is_test_fixture = models.BooleanField(default=False)
    supersedes = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="successors"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(exam_program="NEXTGEN_UBE"), name="scope_program_nextgen_ube"
            ),
            models.CheckConstraint(
                condition=Q(exam_component="NEXTGEN_CORE"), name="scope_component_nextgen_core"
            ),
            models.CheckConstraint(
                condition=Q(is_national=True, jurisdiction=""), name="scope_national_only"
            ),
            models.UniqueConstraint(
                fields=("exam_program", "exam_component"),
                condition=Q(status="ACTIVE", is_test_fixture=False),
                name="one_active_official_scope",
            ),
        ]
        indexes = [models.Index(fields=("exam_program", "exam_component", "status"))]

    def __str__(self):
        return self.version_identifier

    def save(self, *args, **kwargs):
        if self.pk:
            previous = type(self).objects.filter(pk=self.pk).first()
            if previous and previous.status in (self.Status.ACTIVE, self.Status.SUPERSEDED):
                allowed = {"status"}
                changed = {
                    field.name
                    for field in self._meta.fields
                    if field.name != "id"
                    and getattr(previous, field.name) != getattr(self, field.name)
                }
                if changed - allowed or previous.status == self.Status.SUPERSEDED:
                    raise ValidationError("Active and superseded scope versions are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Official scope versions cannot be deleted.")

    def clean(self):
        if (
            self.exam_program != self.EXAM_PROGRAM
            or self.exam_component != self.EXAM_COMPONENT
            or not self.is_national
            or self.jurisdiction
        ):
            raise ValidationError("V1 official scope must be national NEXTGEN_UBE/NEXTGEN_CORE.")
        if bool(self.administration_start) != bool(self.administration_end):
            raise ValidationError("Administration periods require both start and end dates.")
        if (
            self.administration_start
            and self.administration_end
            and self.administration_start > self.administration_end
        ):
            raise ValidationError("Administration period start must not follow its end.")
        if self.is_test_fixture != (self.release_class == self.ReleaseClass.TEST_FIXTURE):
            raise ValidationError("Fixture classification must agree with release_class.")


class OfficialScopeSource(models.Model):
    scope_version = models.ForeignKey(OfficialScopeVersion, on_delete=models.PROTECT)
    artifact = models.ForeignKey(OfficialSourceArtifact, on_delete=models.PROTECT)
    role = models.CharField(max_length=80)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("scope_version", "artifact"), name="scope_artifact_unique"
            )
        ]
        ordering = ("ordering", "id")

    def __str__(self):
        return f"{self.scope_version}:{self.artifact}"

    def save(self, *args, **kwargs):
        if self.scope_version_id and self.scope_version.status in (
            OfficialScopeVersion.Status.ACTIVE,
            OfficialScopeVersion.Status.SUPERSEDED,
        ):
            raise ValidationError("Sources in active or superseded scopes are immutable.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.scope_version.status in (
            OfficialScopeVersion.Status.ACTIVE,
            OfficialScopeVersion.Status.SUPERSEDED,
        ):
            raise ValidationError("Sources in active or superseded scopes are immutable.")
        super().delete(*args, **kwargs)


class OfficialScopeItem(models.Model):
    class Perimeter(models.TextChoices):
        TESTABLE = "TESTABLE", "Testable"
        CONTEXT = "CONTEXT", "Context"
        EXCLUDED = "EXCLUDED", "Excluded"
        UNSPECIFIED = "UNSPECIFIED", "Unspecified"

    class KnowledgeTreatment(models.TextChoices):
        RECALLED_REQUIRED = "RECALLED_REQUIRED", "Recalled knowledge required"
        RECOGNITION_WITH_OR_WITHOUT_RESOURCES = (
            "RECOGNITION_WITH_OR_WITHOUT_RESOURCES",
            "May be tested with or without resources",
        )
        RESOURCES_ALWAYS_PROVIDED = (
            "RESOURCES_ALWAYS_PROVIDED",
            "Legal resources always provided",
        )
        FOUNDATIONAL_SKILL = "FOUNDATIONAL_SKILL", "Foundational skill"
        EXAM_DESIGN_METADATA = "EXAM_DESIGN_METADATA", "Exam design metadata"
        MIXED_OFFICIAL_MARKERS = (
            "MIXED_OFFICIAL_MARKERS",
            "Contains both recalled-only and with-or-without-resource topics",
        )
        UNSPECIFIED = "UNSPECIFIED", "Unspecified"

    class NormalizationStatus(models.TextChoices):
        AUTO_ACCEPTED = "AUTO_ACCEPTED", "Deterministically accepted"
        REVIEW_REQUIRED = "REVIEW_REQUIRED", "Review required"
        BLOCKED = "BLOCKED", "Blocked"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scope_version = models.ForeignKey(
        OfficialScopeVersion, on_delete=models.PROTECT, related_name="items"
    )
    stable_id = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="children"
    )
    official_label = models.CharField(max_length=500)
    official_text = models.TextField(blank=True)
    ordering = models.PositiveIntegerField(default=0)
    perimeter = models.CharField(
        max_length=16, choices=Perimeter.choices, default=Perimeter.UNSPECIFIED
    )
    subject_group = models.CharField(max_length=200, blank=True)
    is_leaf = models.BooleanField(default=False)
    source_artifact = models.ForeignKey(OfficialSourceArtifact, on_delete=models.PROTECT)
    source_locator = models.CharField(max_length=300)
    treatment_metadata = models.JSONField(default=dict, blank=True)
    knowledge_treatment = models.CharField(
        max_length=48,
        choices=KnowledgeTreatment.choices,
        default=KnowledgeTreatment.UNSPECIFIED,
    )
    normalization_status = models.CharField(
        max_length=24,
        choices=NormalizationStatus.choices,
        default=NormalizationStatus.AUTO_ACCEPTED,
    )
    normalization_notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("scope_version", "stable_id"), name="scope_item_identity_unique"
            )
        ]
        indexes = [
            models.Index(fields=("scope_version", "parent", "ordering")),
            models.Index(fields=("scope_version", "is_leaf")),
        ]
        ordering = ("ordering", "stable_id")

    def __str__(self):
        return f"{self.scope_version}:{self.stable_id}"

    def save(self, *args, **kwargs):
        if self.scope_version_id and self.scope_version.status in (
            OfficialScopeVersion.Status.ACTIVE,
            OfficialScopeVersion.Status.SUPERSEDED,
        ):
            raise ValidationError("Items in active or superseded scopes are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Official scope items cannot be deleted.")

    def clean(self):
        if self.parent_id and self.parent.scope_version_id != self.scope_version_id:
            raise ValidationError("Parent must belong to the same scope version.")
        if not isinstance(self.treatment_metadata, dict):
            raise ValidationError("Treatment metadata must be an object.")
        forbidden = {
            "learner_mastery",
            "readiness",
            "difficulty",
            "ai_generation_frequency",
            "guessed_question_count",
        }
        if forbidden.intersection(self.treatment_metadata):
            raise ValidationError(
                "Treatment metadata may contain official exam-design evidence only."
            )
        allowed = {
            "weight",
            "weighting",
            "emphasis",
            "skills",
            "assessment_forms",
            "source",
            "notes",
            "administration_period",
            "resource_treatment",
        }
        unsupported = set(self.treatment_metadata) - allowed
        if unsupported:
            raise ValidationError(f"Unsupported treatment metadata keys: {sorted(unsupported)}")
        source = self.treatment_metadata.get("source")
        if source is not None and (
            not isinstance(source, dict)
            or set(source) != {"stable_id", "source_version"}
            or not all(isinstance(value, str) and value for value in source.values())
        ):
            raise ValidationError(
                "Treatment source must identify exact stable_id and source_version."
            )
