from django.contrib import admin

from official_scope.admin import ImmutableAdmin

from .models import (
    AuthorityEvidence,
    AuthoritySource,
    CaseAuthorityRequirement,
    CoveragePolicy,
    CoverageReleaseSnapshot,
    CoverageRequirementSatisfaction,
    CoverageRequirementSlot,
    CurriculumCompileVersion,
    ObligationHumanReview,
    ObligationRelationship,
    ObligationScopeMapping,
    ReconciliationIssue,
    RequirementAuthorityPlan,
    ReviewResolution,
    RuleObligation,
    ScopeCoverageRequirement,
    SubjectAuthorityPlan,
    SubjectCertifiedSubset,
    SubjectCoveragePolicy,
    SubjectCurriculumManifest,
    SubjectManifestLeaf,
    SubjectPlanHumanReview,
)


@admin.register(AuthoritySource)
class AuthoritySourceAdmin(ImmutableAdmin):
    list_display = (
        "stable_id",
        "source_version",
        "authority_class",
        "canonical_citation",
        "source_class",
    )


@admin.register(CoveragePolicy)
class CoveragePolicyAdmin(ImmutableAdmin):
    list_display = ("stable_id", "policy_version", "source_class", "canonical_sha256")


@admin.register(CurriculumCompileVersion)
class CurriculumCompileVersionAdmin(ImmutableAdmin):
    list_display = (
        "version_identifier",
        "official_scope_version",
        "compiler_schema_version",
        "status",
        "source_class",
    )


@admin.register(RuleObligation)
class RuleObligationAdmin(ImmutableAdmin):
    list_display = ("stable_id", "compile_version", "kind", "compiler_status", "decision")
    list_filter = ("compile_version", "kind", "compiler_status", "decision")


@admin.register(ReconciliationIssue)
class ReconciliationIssueAdmin(ImmutableAdmin):
    list_display = ("stable_id", "compile_version", "category", "severity", "status")
    list_filter = ("compile_version", "category", "severity", "status")


@admin.register(SubjectCurriculumManifest)
class SubjectCurriculumManifestAdmin(ImmutableAdmin):
    list_display = (
        "stable_id",
        "manifest_version",
        "subject_id",
        "official_scope_version",
        "status",
    )


@admin.register(SubjectManifestLeaf)
class SubjectManifestLeafAdmin(ImmutableAdmin):
    list_display = ("manifest", "scope_item", "treatment", "coverage_status", "review_required")
    list_filter = ("manifest", "coverage_status", "treatment")


@admin.register(ScopeCoverageRequirement)
class ScopeCoverageRequirementAdmin(ImmutableAdmin):
    list_display = (
        "stable_id",
        "manifest_leaf",
        "requirement_type",
        "treatment_requirement",
        "review_required",
    )
    list_filter = ("manifest_leaf__manifest", "requirement_type", "treatment_requirement")


@admin.register(SubjectAuthorityPlan)
class SubjectAuthorityPlanAdmin(ImmutableAdmin):
    list_display = (
        "stable_id",
        "manifest",
        "authority_level",
        "acquisition_status",
        "case_authority_required",
    )
    list_filter = ("manifest", "authority_level", "acquisition_status")


@admin.register(SubjectCoveragePolicy)
class SubjectCoveragePolicyAdmin(ImmutableAdmin):
    list_display = (
        "stable_id",
        "policy_version",
        "official_scope_version",
        "review_status",
        "canonical_sha256",
    )


for model in (
    ObligationScopeMapping,
    ObligationRelationship,
    AuthorityEvidence,
    ReviewResolution,
    ObligationHumanReview,
    CoverageReleaseSnapshot,
    CoverageRequirementSlot,
    RequirementAuthorityPlan,
    CaseAuthorityRequirement,
    CoverageRequirementSatisfaction,
    SubjectCertifiedSubset,
    SubjectPlanHumanReview,
):
    admin.site.register(model, ImmutableAdmin)
