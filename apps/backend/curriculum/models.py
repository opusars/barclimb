import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from official_scope.models import OfficialScopeItem, OfficialScopeVersion


class AuthoritySource(models.Model):
    class AuthorityClass(models.TextChoices):
        SUBSTANTIVE_PRIMARY = "SUBSTANTIVE_PRIMARY", "Substantive primary"
        SECONDARY_RECONCILIATION = "SECONDARY_RECONCILIATION", "Secondary reconciliation"

    class SourceClass(models.TextChoices):
        PRODUCTION = "PRODUCTION", "Production"
        TEST_FIXTURE = "TEST_FIXTURE", "Test fixture"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stable_id = models.CharField(max_length=180)
    source_version = models.CharField(max_length=120)
    authority_class = models.CharField(max_length=32, choices=AuthorityClass.choices)
    authority_type = models.CharField(max_length=80)
    title = models.CharField(max_length=400)
    canonical_citation = models.CharField(max_length=300)
    source_uri = models.URLField(max_length=1000, blank=True)
    content_sha256 = models.CharField(max_length=64)
    issuing_authority = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    retrieved_at = models.DateTimeField(null=True, blank=True)
    media_type = models.CharField(max_length=120, blank=True)
    storage_disposition = models.CharField(max_length=80, blank=True)
    rights_basis = models.TextField(blank=True)
    source_class = models.CharField(max_length=16, choices=SourceClass.choices)
    is_national = models.BooleanField(default=True)
    jurisdiction = models.CharField(max_length=80, blank=True)
    supersedes = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="successors"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("stable_id", "source_version"), name="authority_source_identity_unique"
            ),
            models.CheckConstraint(
                condition=Q(content_sha256__regex=r"^[0-9a-f]{64}$"),
                name="authority_source_sha256_format",
            ),
        ]
        indexes = [models.Index(fields=("authority_class", "source_class"))]

    def __str__(self):
        return f"{self.stable_id}@{self.source_version}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Authority sources are immutable; register a new version.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Authority sources cannot be deleted.")

    def clean(self):
        if self.is_national and self.jurisdiction:
            raise ValidationError("National authority cannot carry a jurisdiction.")


class CoveragePolicy(models.Model):
    class CoverageClass(models.TextChoices):
        NATIONAL = "NATIONAL", "National completeness"
        PILOT_ONLY = "PILOT_ONLY", "Bounded pilot only"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stable_id = models.CharField(max_length=160)
    policy_version = models.CharField(max_length=80)
    minimum_obligations_per_leaf = models.PositiveSmallIntegerField(default=1)
    requires_primary_authority = models.BooleanField(default=True)
    allowed_obligation_kinds = models.JSONField(default=list)
    canonical_sha256 = models.CharField(max_length=64)
    source_class = models.CharField(max_length=16, choices=AuthoritySource.SourceClass.choices)
    coverage_class = models.CharField(
        max_length=16, choices=CoverageClass.choices, default=CoverageClass.NATIONAL
    )
    target_scope_item_ids = models.JSONField(default=list, blank=True)
    requires_human_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("stable_id", "policy_version"), name="coverage_policy_identity_unique"
            ),
            models.CheckConstraint(
                condition=Q(minimum_obligations_per_leaf__gte=1),
                name="coverage_policy_minimum_positive",
            ),
        ]

    def __str__(self):
        return f"{self.stable_id}@{self.policy_version}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Coverage policies are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Coverage policies cannot be deleted.")

    def clean(self):
        if not isinstance(self.allowed_obligation_kinds, list):
            raise ValidationError("Allowed obligation kinds must be a list.")
        if not isinstance(self.target_scope_item_ids, list):
            raise ValidationError("Target scope item identities must be a list.")
        if self.coverage_class == self.CoverageClass.PILOT_ONLY and not self.target_scope_item_ids:
            raise ValidationError("PILOT_ONLY policy requires an explicit target leaf subset.")


class CurriculumCompileVersion(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        COMPILED = "COMPILED", "Compiled"
        RECONCILED = "RECONCILED", "Reconciled"
        CERTIFIED = "CERTIFIED", "Certified"
        SUPERSEDED = "SUPERSEDED", "Superseded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version_identifier = models.CharField(max_length=180, unique=True)
    official_scope_version = models.ForeignKey(
        OfficialScopeVersion, on_delete=models.PROTECT, related_name="curriculum_compiles"
    )
    coverage_policy = models.ForeignKey(CoveragePolicy, on_delete=models.PROTECT)
    compiler_schema_version = models.CharField(max_length=80)
    input_sha256 = models.CharField(max_length=64)
    canonical_sha256 = models.CharField(max_length=64, blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    source_class = models.CharField(max_length=16, choices=AuthoritySource.SourceClass.choices)
    coverage_class = models.CharField(
        max_length=16,
        choices=CoveragePolicy.CoverageClass.choices,
        default=CoveragePolicy.CoverageClass.NATIONAL,
    )
    national_complete = models.BooleanField(default=False)
    compile_report = models.JSONField(default=dict, blank=True)
    reconciliation_report = models.JSONField(default=dict, blank=True)
    supersedes = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="successors"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    compiled_at = models.DateTimeField(null=True, blank=True)
    reconciled_at = models.DateTimeField(null=True, blank=True)
    certified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=("official_scope_version", "status"))]
        constraints = [
            models.UniqueConstraint(
                fields=("official_scope_version",),
                condition=Q(status="CERTIFIED", source_class="PRODUCTION"),
                name="one_certified_curriculum_per_scope",
            )
        ]

    def __str__(self):
        return self.version_identifier

    def save(self, *args, **kwargs):
        if self.pk:
            previous = type(self).objects.filter(pk=self.pk).first()
            if previous and previous.status in (self.Status.CERTIFIED, self.Status.SUPERSEDED):
                changed = {
                    field.name
                    for field in self._meta.fields
                    if field.name != "id"
                    and getattr(previous, field.name) != getattr(self, field.name)
                }
                if changed - {"status"} or previous.status == self.Status.SUPERSEDED:
                    raise ValidationError("Certified and superseded compiles are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Curriculum compile versions cannot be deleted.")

    def clean(self):
        fixture_scope = self.official_scope_version.is_test_fixture
        fixture_compile = self.source_class == AuthoritySource.SourceClass.TEST_FIXTURE
        if fixture_scope != fixture_compile:
            raise ValidationError("Scope and curriculum source classifications must match.")
        if (
            self.coverage_class == CoveragePolicy.CoverageClass.PILOT_ONLY
            and self.national_complete
        ):
            raise ValidationError("A PILOT_ONLY compile cannot claim national completeness.")


class RuleObligation(models.Model):
    class Kind(models.TextChoices):
        RULE = "RULE", "Rule"
        ELEMENT = "ELEMENT", "Element"
        FACTOR = "FACTOR", "Factor"
        EXCEPTION = "EXCEPTION", "Exception"
        LIMITATION = "LIMITATION", "Limitation"
        DEFENSE = "DEFENSE", "Defense"
        REMEDY = "REMEDY", "Remedy"
        PROCEDURAL_STEP = "PROCEDURAL_STEP", "Procedural step"
        DISTINCTION = "DISTINCTION", "Distinction"
        DEFINITION = "DEFINITION", "Definition"
        ETHICS_DUTY = "ETHICS_DUTY", "Ethics duty"

    class CompilerStatus(models.TextChoices):
        INCLUDED = "INCLUDED", "Included"
        EXCESS = "EXCESS", "Excess"
        BLOCKED = "BLOCKED", "Blocked"

    class Decision(models.TextChoices):
        AUTO_APPROVABLE = "AUTO_APPROVABLE", "Auto approvable"
        REVIEW_REQUIRED = "REVIEW_REQUIRED", "Review required"
        BLOCKED = "BLOCKED", "Blocked"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compile_version = models.ForeignKey(
        CurriculumCompileVersion, on_delete=models.PROTECT, related_name="obligations"
    )
    stable_id = models.CharField(max_length=200)
    kind = models.CharField(max_length=24, choices=Kind.choices)
    normalized_statement = models.TextField()
    statement = models.TextField()
    canonical_sha256 = models.CharField(max_length=64)
    compiler_status = models.CharField(
        max_length=16, choices=CompilerStatus.choices, default=CompilerStatus.INCLUDED
    )
    decision = models.CharField(max_length=24, choices=Decision.choices)
    reconciliation_status = models.CharField(max_length=40, default="UNRECONCILED")
    inclusion_rationale = models.TextField()
    is_core = models.BooleanField(default=True)
    jurisdiction = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    scope_items = models.ManyToManyField(
        OfficialScopeItem, through="ObligationScopeMapping", related_name="rule_obligations"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("compile_version", "stable_id"), name="obligation_identity_unique"
            ),
            models.UniqueConstraint(
                fields=("compile_version", "canonical_sha256"),
                condition=Q(compiler_status="INCLUDED"),
                name="included_obligation_canonical_unique",
            ),
        ]
        indexes = [models.Index(fields=("compile_version", "kind", "compiler_status"))]

    def __str__(self):
        return f"{self.compile_version}:{self.stable_id}"

    def save(self, *args, **kwargs):
        if self.compile_version_id and self.compile_version.status in (
            CurriculumCompileVersion.Status.CERTIFIED,
            CurriculumCompileVersion.Status.SUPERSEDED,
        ):
            raise ValidationError("Obligations in certified history are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Rule obligations cannot be deleted.")

    def clean(self):
        if self.jurisdiction and self.is_core:
            raise ValidationError("Jurisdiction-specific obligations cannot be core V1 truth.")


class ObligationScopeMapping(models.Model):
    obligation = models.ForeignKey(RuleObligation, on_delete=models.PROTECT)
    scope_item = models.ForeignKey(OfficialScopeItem, on_delete=models.PROTECT)
    mapping_rationale = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("obligation", "scope_item"), name="obligation_scope_mapping_unique"
            )
        ]
        indexes = [models.Index(fields=("scope_item", "obligation"))]

    def __str__(self):
        return f"{self.obligation} -> {self.scope_item}"

    def clean(self):
        if (
            self.obligation_id
            and self.scope_item_id
            and self.obligation.compile_version.official_scope_version_id
            != self.scope_item.scope_version_id
        ):
            raise ValidationError("Obligation mappings must target their compile's scope version.")


class ObligationRelationship(models.Model):
    class Kind(models.TextChoices):
        HAS_ELEMENT = "HAS_ELEMENT", "Has element"
        HAS_FACTOR = "HAS_FACTOR", "Has factor"
        HAS_EXCEPTION = "HAS_EXCEPTION", "Has exception"
        HAS_LIMITATION = "HAS_LIMITATION", "Has limitation"
        HAS_DEFENSE = "HAS_DEFENSE", "Has defense"
        HAS_REMEDY = "HAS_REMEDY", "Has remedy"
        HAS_PROCEDURAL_STEP = "HAS_PROCEDURAL_STEP", "Has procedural step"
        HAS_DISTINCTION = "HAS_DISTINCTION", "Has distinction"
        DEFINES = "DEFINES", "Defines"
        HAS_ETHICS_DUTY = "HAS_ETHICS_DUTY", "Has ethics duty"

    source = models.ForeignKey(
        RuleObligation, on_delete=models.PROTECT, related_name="outgoing_relationships"
    )
    target = models.ForeignKey(
        RuleObligation, on_delete=models.PROTECT, related_name="incoming_relationships"
    )
    kind = models.CharField(max_length=24, choices=Kind.choices)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("source", "target", "kind"), name="obligation_relationship_unique"
            ),
            models.CheckConstraint(
                condition=~Q(source=models.F("target")), name="obligation_relationship_not_self"
            ),
        ]

    def __str__(self):
        return f"{self.source} {self.kind} {self.target}"


class AuthorityEvidence(models.Model):
    class Role(models.TextChoices):
        SUBSTANTIVE_SUPPORT = "SUBSTANTIVE_SUPPORT", "Substantive support"
        SECONDARY_RECONCILIATION = "SECONDARY_RECONCILIATION", "Secondary reconciliation"

    obligation = models.ForeignKey(
        RuleObligation, on_delete=models.PROTECT, related_name="authority_evidence"
    )
    authority = models.ForeignKey(AuthoritySource, on_delete=models.PROTECT)
    role = models.CharField(max_length=32, choices=Role.choices)
    locator = models.CharField(max_length=300)
    proposition_sha256 = models.CharField(max_length=64)
    supports = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("obligation", "authority", "role", "locator"),
                name="authority_evidence_unique",
            )
        ]
        indexes = [models.Index(fields=("obligation", "role"))]

    def __str__(self):
        return f"{self.obligation} supported by {self.authority}"


class ReconciliationIssue(models.Model):
    class Category(models.TextChoices):
        OMISSION = "OMISSION", "Omission"
        EXCESS = "EXCESS", "Excess"
        CONFLICT = "CONFLICT", "Conflict"
        AMBIGUITY = "AMBIGUITY", "Ambiguity"
        DUPLICATE = "DUPLICATE", "Duplicate"
        UNSUPPORTED_PROVENANCE = "UNSUPPORTED_PROVENANCE", "Unsupported provenance"
        INVALID_STRUCTURE = "INVALID_STRUCTURE", "Invalid structure"
        UNSUPPORTED_JURISDICTION = "UNSUPPORTED_JURISDICTION", "Unsupported jurisdiction"

    class Severity(models.TextChoices):
        BLOCKING = "BLOCKING", "Blocking"
        WARNING = "WARNING", "Warning"
        INFO = "INFO", "Information"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        RESOLVED = "RESOLVED", "Resolved"

    compile_version = models.ForeignKey(
        CurriculumCompileVersion, on_delete=models.PROTECT, related_name="issues"
    )
    stable_id = models.CharField(max_length=220)
    category = models.CharField(max_length=32, choices=Category.choices)
    severity = models.CharField(max_length=16, choices=Severity.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.OPEN)
    scope_item = models.ForeignKey(
        OfficialScopeItem, null=True, blank=True, on_delete=models.PROTECT
    )
    obligation = models.ForeignKey(RuleObligation, null=True, blank=True, on_delete=models.PROTECT)
    message = models.TextField()
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("compile_version", "stable_id"), name="reconciliation_issue_unique"
            )
        ]
        indexes = [models.Index(fields=("compile_version", "severity", "status"))]

    def __str__(self):
        return f"{self.compile_version}:{self.category}:{self.stable_id}"


class ReviewResolution(models.Model):
    class Resolution(models.TextChoices):
        ACCEPT = "ACCEPT", "Accept"
        REJECT = "REJECT", "Reject"
        DEFER = "DEFER", "Defer"

    issue = models.OneToOneField(
        ReconciliationIssue, on_delete=models.PROTECT, related_name="review_resolution"
    )
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    resolution = models.CharField(max_length=16, choices=Resolution.choices)
    rationale = models.TextField()
    changes_canonical_truth = models.BooleanField(default=False)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue}:{self.resolution}"


class ObligationHumanReview(models.Model):
    class Resolution(models.TextChoices):
        APPROVE = "APPROVE", "Approve"
        REJECT = "REJECT", "Reject"

    obligation = models.OneToOneField(
        RuleObligation, on_delete=models.PROTECT, related_name="human_review"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT
    )
    reviewer_name = models.CharField(max_length=200, default="")
    reviewer_role_qualification = models.TextField(default="")
    resolution = models.CharField(max_length=16, choices=Resolution.choices)
    rationale = models.TextField()
    attestation = models.TextField(default="")
    authority_reviewed = models.BooleanField(default=False)
    review_manifest_sha256 = models.CharField(max_length=64, default="")
    reviewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(review_manifest_sha256__regex=r"^[0-9a-f]{64}$"),
                name="obligation_review_manifest_sha256_format",
            )
        ]

    def __str__(self):
        return f"{self.obligation}:{self.resolution}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Human review attestations are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Human review attestations cannot be deleted.")

    def clean(self):
        if self.reviewer_id and not self.reviewer.is_staff:
            raise ValidationError("Production obligation review requires a staff reviewer.")
        if not self.reviewer_name.strip() or not self.reviewer_role_qualification.strip():
            raise ValidationError(
                "Human review requires the reviewer's supplied identity and role."
            )
        if not self.rationale.strip() or not self.attestation.strip():
            raise ValidationError("Human review requires rationale and the supplied attestation.")
        if self.obligation.compile_version.source_class != AuthoritySource.SourceClass.PRODUCTION:
            raise ValidationError("Production human review cannot attest fixture content.")


class CoverageReleaseSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compile_version = models.OneToOneField(
        CurriculumCompileVersion, on_delete=models.PROTECT, related_name="coverage_snapshot"
    )
    official_scope_version = models.ForeignKey(OfficialScopeVersion, on_delete=models.PROTECT)
    compiler_schema_version = models.CharField(max_length=80)
    source_class = models.CharField(max_length=16, choices=AuthoritySource.SourceClass.choices)
    coverage_class = models.CharField(
        max_length=16,
        choices=CoveragePolicy.CoverageClass.choices,
        default=CoveragePolicy.CoverageClass.NATIONAL,
    )
    national_complete = models.BooleanField(default=False)
    authority_provenance_sha256 = models.CharField(max_length=64, blank=True)
    human_review_sha256 = models.CharField(max_length=64, blank=True)
    human_review_evidence = models.JSONField(default=list, blank=True)
    human_review_status = models.CharField(max_length=32, default="NOT_REQUIRED")
    obligation_count = models.PositiveIntegerField()
    leaf_count = models.PositiveIntegerField()
    covered_leaf_count = models.PositiveIntegerField()
    blocking_issue_count = models.PositiveIntegerField()
    warning_issue_count = models.PositiveIntegerField()
    coverage_results = models.JSONField()
    certification_sha256 = models.CharField(max_length=64, unique=True)
    certified_at = models.DateTimeField()

    def __str__(self):
        return f"Coverage snapshot {self.compile_version}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Coverage release snapshots are immutable.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Coverage release snapshots cannot be deleted.")


class SubjectCoveragePolicy(models.Model):
    class ReviewStatus(models.TextChoices):
        REVIEW_PENDING = "REVIEW_PENDING", "Human review pending"
        APPROVED = "APPROVED", "Human approved"
        REJECTED = "REJECTED", "Human rejected"
        SUPERSEDED = "SUPERSEDED", "Superseded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stable_id = models.CharField(max_length=180)
    policy_version = models.CharField(max_length=80)
    official_scope_version = models.ForeignKey(OfficialScopeVersion, on_delete=models.PROTECT)
    administration_start = models.DateField()
    administration_end = models.DateField()
    requires_primary_authority = models.BooleanField(default=True)
    requires_human_review = models.BooleanField(default=True)
    certification_gate_version = models.CharField(max_length=80)
    canonical_sha256 = models.CharField(max_length=64)
    source_class = models.CharField(max_length=16, choices=AuthoritySource.SourceClass.choices)
    review_status = models.CharField(
        max_length=24, choices=ReviewStatus.choices, default=ReviewStatus.REVIEW_PENDING
    )
    supersedes = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="successors"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("stable_id", "policy_version"),
                name="subject_coverage_policy_identity_unique",
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="subject_policy_sha256_format",
            ),
        ]

    def __str__(self):
        return f"{self.stable_id}@{self.policy_version}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Subject coverage policies are immutable; create a new version.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Subject coverage policies cannot be deleted.")

    def clean(self):
        scope = self.official_scope_version
        if self.administration_start != scope.administration_start:
            raise ValidationError(
                "Policy start must match the official scope administration period."
            )
        if self.administration_end != scope.administration_end:
            raise ValidationError("Policy end must match the official scope administration period.")
        if self.source_class == AuthoritySource.SourceClass.PRODUCTION and scope.is_test_fixture:
            raise ValidationError("Production subject policy cannot target fixture scope truth.")
        if not self.requires_human_review:
            raise ValidationError("Production subject completeness policy requires human review.")
        if self.supersedes_id and self.supersedes.stable_id != self.stable_id:
            raise ValidationError("A subject policy may supersede only the same stable identity.")


class SubjectCurriculumManifest(models.Model):
    class Status(models.TextChoices):
        REVIEW_PENDING = "REVIEW_PENDING", "Human review pending"
        APPROVED = "APPROVED", "Human approved"
        REJECTED = "REJECTED", "Human rejected"
        SUPERSEDED = "SUPERSEDED", "Superseded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stable_id = models.CharField(max_length=180)
    manifest_version = models.CharField(max_length=80)
    subject_id = models.CharField(max_length=120)
    subject_label = models.CharField(max_length=240)
    official_scope_version = models.ForeignKey(OfficialScopeVersion, on_delete=models.PROTECT)
    coverage_policy = models.ForeignKey(SubjectCoveragePolicy, on_delete=models.PROTECT)
    canonical_sha256 = models.CharField(max_length=64)
    source_class = models.CharField(max_length=16, choices=AuthoritySource.SourceClass.choices)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.REVIEW_PENDING)
    supersedes = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, related_name="successors"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("stable_id", "manifest_version"),
                name="subject_manifest_identity_unique",
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="subject_manifest_sha256_format",
            ),
        ]

    def __str__(self):
        return f"{self.stable_id}@{self.manifest_version}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Subject manifests are immutable; create a new version.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Subject manifests cannot be deleted.")

    def clean(self):
        if self.coverage_policy.official_scope_version_id != self.official_scope_version_id:
            raise ValidationError(
                "Subject manifest and coverage policy must share one scope version."
            )
        fixture_manifest = self.source_class == AuthoritySource.SourceClass.TEST_FIXTURE
        if fixture_manifest != self.official_scope_version.is_test_fixture:
            raise ValidationError("Subject manifest classification must match its scope truth.")
        if self.supersedes_id and self.supersedes.stable_id != self.stable_id:
            raise ValidationError("A subject manifest may supersede only the same stable identity.")


class SubjectManifestLeaf(models.Model):
    class CoverageStatus(models.TextChoices):
        UNMAPPED = "UNMAPPED", "Unmapped"
        AUTHORITY_PLANNED = "AUTHORITY_PLANNED", "Authority planned"
        CANDIDATES_PENDING = "CANDIDATES_PENDING", "Candidates pending"
        PARTIALLY_COVERED = "PARTIALLY_COVERED", "Partially covered"
        LEAF_CERTIFIED = "LEAF_CERTIFIED", "Leaf certified"

    manifest = models.ForeignKey(
        SubjectCurriculumManifest, on_delete=models.PROTECT, related_name="manifest_leaves"
    )
    scope_item = models.ForeignKey(OfficialScopeItem, on_delete=models.PROTECT)
    hierarchy_path = models.JSONField(default=list)
    treatment = models.CharField(max_length=48)
    coverage_status = models.CharField(
        max_length=24, choices=CoverageStatus.choices, default=CoverageStatus.UNMAPPED
    )
    review_required = models.BooleanField(default=True)
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("manifest", "scope_item"), name="subject_manifest_leaf_unique"
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="subject_manifest_leaf_sha256_format",
            ),
        ]
        ordering = ("scope_item__ordering", "scope_item__stable_id")

    def __str__(self):
        return f"{self.manifest}:{self.scope_item.stable_id}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Subject manifest leaves are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Subject manifest leaves cannot be deleted.")

    def clean(self):
        if self.scope_item.scope_version_id != self.manifest.official_scope_version_id:
            raise ValidationError("Manifest leaves must belong to the manifest's scope version.")
        if not self.scope_item.is_leaf or self.scope_item.perimeter != "TESTABLE":
            raise ValidationError("Subject manifests may include only official testable leaves.")
        if self.scope_item.subject_group != self.manifest.subject_id:
            raise ValidationError("Manifest leaf does not belong to the declared subject.")
        if self.treatment != self.scope_item.knowledge_treatment:
            raise ValidationError("Manifest leaf treatment must preserve official scope truth.")


class ScopeCoverageRequirement(models.Model):
    class RequirementType(models.TextChoices):
        GOVERNING_RULE = "GOVERNING_RULE", "Governing rule"
        TRIGGERING_CONDITIONS = "TRIGGERING_CONDITIONS", "Triggering conditions"
        ELEMENTS_FACTORS = "ELEMENTS_FACTORS", "Elements or factors"
        EXCEPTIONS_LIMITATIONS = "EXCEPTIONS_LIMITATIONS", "Exceptions or limitations"
        PROCEDURAL_BRANCHING = "PROCEDURAL_BRANCHING", "Procedural branching"
        CONSEQUENCES_REMEDIES = "CONSEQUENCES_REMEDIES", "Consequences or remedies"
        DISTINCTIONS_DEFINITIONS = "DISTINCTIONS_DEFINITIONS", "Distinctions or definitions"
        DEFENSES = "DEFENSES", "Defenses"

    class TreatmentRequirement(models.TextChoices):
        RECALL = "RECALL", "Recall"
        RECOGNITION = "RECOGNITION", "Issue recognition without resources"
        RESOURCE_APPLICATION = "RESOURCE_APPLICATION", "Application with supplied resources"
        MIXED = "MIXED", "Mixed official treatment"

    manifest_leaf = models.ForeignKey(
        SubjectManifestLeaf, on_delete=models.PROTECT, related_name="coverage_requirements"
    )
    stable_id = models.CharField(max_length=220)
    doctrinal_subarea = models.CharField(max_length=300)
    requirement_type = models.CharField(max_length=32, choices=RequirementType.choices)
    treatment_requirement = models.CharField(max_length=24, choices=TreatmentRequirement.choices)
    review_required = models.BooleanField(default=True)
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("manifest_leaf", "stable_id"),
                name="scope_coverage_requirement_identity_unique",
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="scope_requirement_sha256_format",
            ),
        ]
        ordering = ("manifest_leaf", "stable_id")

    def __str__(self):
        return f"{self.manifest_leaf}:{self.stable_id}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Coverage requirements are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Coverage requirements cannot be deleted.")


class CoverageRequirementSlot(models.Model):
    requirement = models.ForeignKey(
        ScopeCoverageRequirement, on_delete=models.PROTECT, related_name="slots"
    )
    stable_id = models.CharField(max_length=220)
    obligation_kind = models.CharField(max_length=24, choices=RuleObligation.Kind.choices)
    minimum_count = models.PositiveSmallIntegerField(default=1)
    relationship_expectations = models.JSONField(default=list, blank=True)
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("requirement", "stable_id"), name="coverage_requirement_slot_unique"
            ),
            models.CheckConstraint(
                condition=Q(minimum_count__gte=1), name="coverage_requirement_slot_min_positive"
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="coverage_requirement_slot_sha256_format",
            ),
        ]

    def __str__(self):
        return f"{self.requirement}:{self.stable_id}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Coverage requirement slots are immutable.")
        if not isinstance(self.relationship_expectations, list):
            raise ValidationError("Relationship expectations must be a list.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Coverage requirement slots cannot be deleted.")


class SubjectAuthorityPlan(models.Model):
    class AuthorityLevel(models.TextChoices):
        CONTROLLING_CONSTITUTION = "CONTROLLING_CONSTITUTION", "Controlling constitutional text"
        CONTROLLING_STATUTE = "CONTROLLING_STATUTE", "Controlling federal statute"
        CONTROLLING_RULE = "CONTROLLING_RULE", "Controlling federal rule"
        BINDING_SUPREME_COURT = "BINDING_SUPREME_COURT", "Binding Supreme Court authority"
        OTHER_PRIMARY = "OTHER_PRIMARY", "Other appropriate primary authority"
        OPTIONAL_SECONDARY = "OPTIONAL_SECONDARY", "Optional secondary reconciliation"

    class AcquisitionStatus(models.TextChoices):
        PLANNED = "PLANNED", "Acquisition planned"
        PARTIALLY_ACQUIRED = "PARTIALLY_ACQUIRED", "Partially acquired"
        ACQUIRED = "ACQUIRED", "Acquired"

    manifest = models.ForeignKey(
        SubjectCurriculumManifest, on_delete=models.PROTECT, related_name="authority_plans"
    )
    stable_id = models.CharField(max_length=220)
    source_family = models.CharField(max_length=120)
    authority_level = models.CharField(max_length=32, choices=AuthorityLevel.choices)
    planned_title = models.CharField(max_length=400)
    canonical_source_uri = models.URLField(max_length=1000, blank=True)
    version_requirement = models.TextField()
    freshness_requirement = models.TextField()
    drift_action = models.TextField()
    case_authority_required = models.BooleanField(default=False)
    acquisition_status = models.CharField(
        max_length=24, choices=AcquisitionStatus.choices, default=AcquisitionStatus.PLANNED
    )
    acquired_authority = models.ForeignKey(
        AuthoritySource, null=True, blank=True, on_delete=models.PROTECT
    )
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("manifest", "stable_id"), name="subject_authority_plan_unique"
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="subject_authority_plan_sha256_format",
            ),
        ]

    def __str__(self):
        return f"{self.manifest}:{self.stable_id}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Authority acquisition plans are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Authority acquisition plans cannot be deleted.")

    def clean(self):
        if (
            self.acquisition_status == self.AcquisitionStatus.ACQUIRED
            and not self.acquired_authority
        ):
            raise ValidationError(
                "Acquired authority plans must reference immutable authority truth."
            )
        if self.acquired_authority_id:
            if (
                self.acquired_authority.source_class != self.manifest.source_class
                or not self.acquired_authority.is_national
                or self.acquired_authority.jurisdiction
            ):
                raise ValidationError(
                    "Acquired authority classification must match national subject-plan truth."
                )
            if (
                self.authority_level != self.AuthorityLevel.OPTIONAL_SECONDARY
                and self.acquired_authority.authority_class
                != AuthoritySource.AuthorityClass.SUBSTANTIVE_PRIMARY
            ):
                raise ValidationError("Required authority plans must reference primary authority.")
        if (
            self.authority_level == self.AuthorityLevel.OPTIONAL_SECONDARY
            and self.case_authority_required
        ):
            raise ValidationError(
                "Optional secondary material cannot satisfy case-authority requirements."
            )


class RequirementAuthorityPlan(models.Model):
    class Role(models.TextChoices):
        REQUIRED = "REQUIRED", "Required primary authority"
        CONDITIONAL = "CONDITIONAL", "Conditionally required primary authority"
        OPTIONAL_RECONCILIATION = "OPTIONAL_RECONCILIATION", "Optional reconciliation evidence"

    requirement = models.ForeignKey(
        ScopeCoverageRequirement, on_delete=models.PROTECT, related_name="authority_mappings"
    )
    authority_plan = models.ForeignKey(
        SubjectAuthorityPlan, on_delete=models.PROTECT, related_name="requirement_mappings"
    )
    role = models.CharField(max_length=32, choices=Role.choices)
    proposition_types = models.JSONField(default=list)
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("requirement", "authority_plan"),
                name="requirement_authority_plan_unique",
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="requirement_authority_plan_sha256_format",
            ),
        ]

    def __str__(self):
        return f"{self.requirement} -> {self.authority_plan}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Requirement authority mappings are immutable.")
        if not isinstance(self.proposition_types, list) or not self.proposition_types:
            raise ValidationError("Authority mappings require proposition-type classifications.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Requirement authority mappings cannot be deleted.")

    def clean(self):
        if self.requirement.manifest_leaf.manifest_id != self.authority_plan.manifest_id:
            raise ValidationError("Requirement and authority plan must belong to one manifest.")
        if (
            self.role == self.Role.REQUIRED
            and self.authority_plan.authority_level
            == SubjectAuthorityPlan.AuthorityLevel.OPTIONAL_SECONDARY
        ):
            raise ValidationError("Secondary evidence cannot replace required primary authority.")


class CaseAuthorityRequirement(models.Model):
    authority_plan = models.ForeignKey(
        SubjectAuthorityPlan, on_delete=models.PROTECT, related_name="case_requirements"
    )
    stable_id = models.CharField(max_length=220)
    proposition_type = models.CharField(max_length=120)
    required_court = models.CharField(max_length=160, default="Supreme Court of the United States")
    exact_case_identity_required = models.BooleanField(default=True)
    decision_date_required = models.BooleanField(default=True)
    reliable_source_uri_required = models.BooleanField(default=True)
    proposition_locator_required = models.BooleanField(default=True)
    authority_status_required = models.BooleanField(default=True)
    later_treatment_review_required = models.BooleanField(default=True)
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("authority_plan", "stable_id"), name="case_authority_requirement_unique"
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="case_authority_requirement_sha256_format",
            ),
        ]

    def __str__(self):
        return f"{self.authority_plan}:{self.stable_id}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Case-authority requirements are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Case-authority requirements cannot be deleted.")

    def clean(self):
        if not self.authority_plan.case_authority_required:
            raise ValidationError("Case requirements require a case-authority acquisition plan.")


class CoverageRequirementSatisfaction(models.Model):
    class Status(models.TextChoices):
        CERTIFIED = "CERTIFIED", "Certified"

    slot = models.ForeignKey(
        CoverageRequirementSlot, on_delete=models.PROTECT, related_name="satisfactions"
    )
    obligation = models.ForeignKey(RuleObligation, on_delete=models.PROTECT)
    coverage_snapshot = models.ForeignKey(
        CoverageReleaseSnapshot, null=True, blank=True, on_delete=models.PROTECT
    )
    status = models.CharField(max_length=16, choices=Status.choices)
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("slot", "obligation"), name="coverage_requirement_satisfaction_unique"
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="coverage_satisfaction_sha256_format",
            ),
            models.CheckConstraint(
                condition=Q(status="CERTIFIED", coverage_snapshot__isnull=False),
                name="coverage_satisfaction_certified_snapshot",
            ),
        ]

    def __str__(self):
        return f"{self.slot} <- {self.obligation}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Coverage requirement satisfactions are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Coverage requirement satisfactions cannot be deleted.")

    def clean(self):
        requirement = self.slot.requirement
        manifest = requirement.manifest_leaf.manifest
        if (
            self.obligation.compile_version.official_scope_version_id
            != manifest.official_scope_version_id
        ):
            raise ValidationError("Requirement satisfaction must use the manifest's scope truth.")
        if self.obligation.kind != self.slot.obligation_kind:
            raise ValidationError("Obligation kind does not satisfy the required structural slot.")
        if not self.obligation.scope_items.filter(
            pk=requirement.manifest_leaf.scope_item_id
        ).exists():
            raise ValidationError("Obligation must map to the requirement's official scope leaf.")
        if self.status != self.Status.CERTIFIED or self.coverage_snapshot is None:
            raise ValidationError("Requirement satisfaction records only certified evidence.")
        if self.coverage_snapshot.compile_version_id != self.obligation.compile_version_id:
            raise ValidationError("Certified satisfaction snapshot must contain the obligation.")
        if (
            self.coverage_snapshot.blocking_issue_count
            or self.obligation.compiler_status != RuleObligation.CompilerStatus.INCLUDED
            or not self.obligation.is_core
            or self.obligation.jurisdiction
        ):
            raise ValidationError(
                "Certified satisfaction requires clean included national-core obligation truth."
            )
        if requirement.review_required:
            review = getattr(self.obligation, "human_review", None)
            if review is None or review.resolution != ObligationHumanReview.Resolution.APPROVE:
                raise ValidationError(
                    "Coverage requirement satisfaction needs approved human review."
                )


class SubjectCertifiedSubset(models.Model):
    manifest_leaf = models.ForeignKey(
        SubjectManifestLeaf, on_delete=models.PROTECT, related_name="certified_subsets"
    )
    coverage_snapshot = models.ForeignKey(CoverageReleaseSnapshot, on_delete=models.PROTECT)
    contribution_class = models.CharField(max_length=24, default="PARTIAL_LEAF_COVERAGE")
    canonical_sha256 = models.CharField(max_length=64)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("manifest_leaf", "coverage_snapshot"),
                name="subject_certified_subset_unique",
            ),
            models.CheckConstraint(
                condition=Q(canonical_sha256__regex=r"^[0-9a-f]{64}$"),
                name="subject_certified_subset_sha256_format",
            ),
        ]

    def __str__(self):
        return f"{self.manifest_leaf} <- {self.coverage_snapshot}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Certified subject subsets are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Certified subject subsets cannot be deleted.")

    def clean(self):
        snapshot = self.coverage_snapshot
        manifest = self.manifest_leaf.manifest
        if snapshot.official_scope_version_id != manifest.official_scope_version_id:
            raise ValidationError("Certified subset and subject manifest must share scope truth.")
        if snapshot.coverage_class != CoveragePolicy.CoverageClass.PILOT_ONLY:
            raise ValidationError(
                "Subject planning may only import bounded historical subsets here."
            )
        if snapshot.national_complete:
            raise ValidationError("A bounded subject subset cannot claim national completeness.")


class SubjectPlanHumanReview(models.Model):
    class Resolution(models.TextChoices):
        APPROVE = "APPROVE", "Approve"
        REJECT = "REJECT", "Reject"

    manifest = models.OneToOneField(
        SubjectCurriculumManifest, on_delete=models.PROTECT, related_name="human_review"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT
    )
    reviewer_name = models.CharField(max_length=200)
    reviewer_role_qualification = models.TextField()
    resolution = models.CharField(max_length=16, choices=Resolution.choices)
    rationale = models.TextField()
    attestation = models.TextField()
    review_packet_sha256 = models.CharField(max_length=64)
    reviewed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(review_packet_sha256__regex=r"^[0-9a-f]{64}$"),
                name="subject_plan_review_packet_sha256_format",
            )
        ]

    def __str__(self):
        return f"{self.manifest}:{self.resolution}"

    def save(self, *args, **kwargs):
        if self.pk and type(self).objects.filter(pk=self.pk).exists():
            raise ValidationError("Subject-plan human reviews are immutable.")
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Subject-plan human reviews cannot be deleted.")

    def clean(self):
        if self.reviewer_id and not self.reviewer.is_staff:
            raise ValidationError("Subject-plan review requires a staff reviewer.")
        if not all(
            value.strip()
            for value in (
                self.reviewer_name,
                self.reviewer_role_qualification,
                self.rationale,
                self.attestation,
            )
        ):
            raise ValidationError(
                "Subject-plan review requires identity, qualification, and rationale."
            )
        if self.manifest.source_class != AuthoritySource.SourceClass.PRODUCTION:
            raise ValidationError("Production subject-plan review cannot attest fixture truth.")
