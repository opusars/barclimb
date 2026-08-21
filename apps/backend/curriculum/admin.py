from django.contrib import admin

from official_scope.admin import ImmutableAdmin

from .models import (
    AuthorityEvidence,
    AuthoritySource,
    CoveragePolicy,
    CoverageReleaseSnapshot,
    CurriculumCompileVersion,
    ObligationHumanReview,
    ObligationRelationship,
    ObligationScopeMapping,
    ReconciliationIssue,
    ReviewResolution,
    RuleObligation,
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


for model in (
    ObligationScopeMapping,
    ObligationRelationship,
    AuthorityEvidence,
    ReviewResolution,
    ObligationHumanReview,
    CoverageReleaseSnapshot,
):
    admin.site.register(model, ImmutableAdmin)
