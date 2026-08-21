from rest_framework import serializers

from .models import CoverageReleaseSnapshot, CurriculumCompileVersion, RuleObligation


class ObligationReadSerializer(serializers.ModelSerializer):
    scope_item_ids = serializers.SerializerMethodField()
    provenance = serializers.SerializerMethodField()

    class Meta:
        model = RuleObligation
        fields = (
            "stable_id",
            "kind",
            "statement",
            "canonical_sha256",
            "scope_item_ids",
            "provenance",
        )

    def get_scope_item_ids(self, obj):
        return sorted(obj.scope_items.values_list("stable_id", flat=True))

    def get_provenance(self, obj):
        return [
            {
                "authority_id": evidence.authority.stable_id,
                "authority_version": evidence.authority.source_version,
                "authority_class": evidence.authority.authority_class,
                "citation": evidence.authority.canonical_citation,
                "role": evidence.role,
                "locator": evidence.locator,
            }
            for evidence in obj.authority_evidence.select_related("authority").order_by(
                "authority__stable_id", "locator"
            )
        ]


class CertifiedCurriculumSerializer(serializers.ModelSerializer):
    scope_version = serializers.CharField(source="official_scope_version.version_identifier")
    obligations = serializers.SerializerMethodField()
    coverage = serializers.SerializerMethodField()

    class Meta:
        model = CurriculumCompileVersion
        fields = (
            "version_identifier",
            "scope_version",
            "compiler_schema_version",
            "canonical_sha256",
            "source_class",
            "coverage",
            "obligations",
        )

    def get_coverage(self, obj):
        snapshot: CoverageReleaseSnapshot = obj.coverage_snapshot
        return {
            "certification_sha256": snapshot.certification_sha256,
            "obligation_count": snapshot.obligation_count,
            "leaf_count": snapshot.leaf_count,
            "covered_leaf_count": snapshot.covered_leaf_count,
            "blocking_issue_count": snapshot.blocking_issue_count,
            "warning_issue_count": snapshot.warning_issue_count,
        }

    def get_obligations(self, obj):
        obligations = obj.obligations.filter(compiler_status="INCLUDED", is_core=True).order_by(
            "stable_id"
        )
        return ObligationReadSerializer(obligations, many=True).data
