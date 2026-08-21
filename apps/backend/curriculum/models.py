import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stable_id = models.CharField(max_length=160)
    policy_version = models.CharField(max_length=80)
    minimum_obligations_per_leaf = models.PositiveSmallIntegerField(default=1)
    requires_primary_authority = models.BooleanField(default=True)
    allowed_obligation_kinds = models.JSONField(default=list)
    canonical_sha256 = models.CharField(max_length=64)
    source_class = models.CharField(max_length=16, choices=AuthoritySource.SourceClass.choices)
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


class CoverageReleaseSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compile_version = models.OneToOneField(
        CurriculumCompileVersion, on_delete=models.PROTECT, related_name="coverage_snapshot"
    )
    official_scope_version = models.ForeignKey(OfficialScopeVersion, on_delete=models.PROTECT)
    compiler_schema_version = models.CharField(max_length=80)
    source_class = models.CharField(max_length=16, choices=AuthoritySource.SourceClass.choices)
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
