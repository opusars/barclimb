import copy
import hashlib
import json
from datetime import date, datetime, timezone
from io import StringIO
from pathlib import Path

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DatabaseError, connection, transaction

from curriculum.models import (
    AuthoritySource,
    CoveragePolicy,
    CoverageReleaseSnapshot,
    CurriculumCompileVersion,
    RequirementAuthorityPlan,
    RuleObligation,
    SubjectCurriculumManifest,
    SubjectManifestLeaf,
    SubjectPlanHumanReview,
)
from curriculum.subject_planning import (
    assert_subject_certification_ready,
    import_subject_plan,
    subject_coverage_report,
)
from official_scope.models import (
    OfficialScopeItem,
    OfficialScopeSource,
    OfficialScopeVersion,
    OfficialSourceArtifact,
)
from official_scope.services import canonical_sha256

pytestmark = pytest.mark.django_db

BACKEND_ROOT = Path(__file__).resolve().parents[1]
SCOPE_PATH = BACKEND_ROOT / "official_scope" / "manifests" / "ncbe-nextgen-2026-07.json"
PILOT_PATH = BACKEND_ROOT / "curriculum" / "manifests" / "frcp-rule4-service-pilot.json"
PLAN_PATH = BACKEND_ROOT / "curriculum" / "manifests" / "civil-procedure-subject-plan-2026-v1.json"
REVIEW_PACKET_PATH = BACKEND_ROOT.parents[1] / "docs" / "project" / "M2_2C_HUMAN_REVIEW_PACKET.md"

EXPECTED_LEAF_IDS = {
    "civil-procedure-jurisdiction",
    "civil-procedure-service-process-notice",
    "civil-procedure-venue-transfer",
    "civil-procedure-litigation",
    "civil-procedure-motions-judgments",
    "civil-procedure-appeals",
}


def _json(path):
    return json.loads(path.read_text())


def _rechecksum(payload):
    payload["canonical_sha256"] = canonical_sha256(
        {key: value for key, value in payload.items() if key != "canonical_sha256"}
    )
    return payload


def _install_scope_descriptor():
    descriptor = _json(SCOPE_PATH)
    artifact_models = {}
    for entry in descriptor["artifacts"]:
        artifact_models[entry["stable_id"]] = OfficialSourceArtifact.objects.create(
            stable_id=entry["stable_id"],
            source_authority=entry["source_authority"],
            artifact_type=entry["artifact_type"],
            official_title=entry["official_title"],
            source_uri=entry["source_uri"],
            publication_date=date.fromisoformat(entry["publication_date"]),
            effective_date=date.fromisoformat(entry["effective_date"]),
            effective_end_date=date.fromisoformat(entry["effective_end_date"]),
            retrieved_at=datetime.fromisoformat(entry["retrieved_at"].replace("Z", "+00:00")),
            content_sha256=entry["expected_sha256"],
            media_type=entry["media_type"],
            storage_disposition=entry["storage_disposition"],
            rights_basis=entry["rights_basis"],
            source_version=entry["source_version"],
            source_class=entry["source_class"],
            provenance_notes=entry["provenance_notes"],
        )
    scope_entry = descriptor["scope"]
    scope = OfficialScopeVersion.objects.create(
        version_identifier=scope_entry["version_identifier"],
        administration_start=date.fromisoformat(scope_entry["administration_start"]),
        administration_end=date.fromisoformat(scope_entry["administration_end"]),
        release_class=scope_entry["release_class"],
        normalization_report=scope_entry["normalization_report"],
        freshness_checked_at=datetime.fromisoformat(
            scope_entry["freshness_checked_at"].replace("Z", "+00:00")
        ),
    )
    for ordering, source in enumerate(scope_entry["sources"]):
        OfficialScopeSource.objects.create(
            scope_version=scope,
            artifact=artifact_models[source["artifact_id"]],
            role=source["role"],
            ordering=ordering,
        )
    items = {}
    for entry in scope_entry["items"]:
        items[entry["stable_id"]] = OfficialScopeItem.objects.create(
            scope_version=scope,
            stable_id=entry["stable_id"],
            parent=items.get(entry.get("parent_id")),
            official_label=entry["official_label"],
            ordering=entry.get("ordering", 0),
            perimeter=entry.get("perimeter", "UNSPECIFIED"),
            subject_group=entry.get("subject_group", ""),
            is_leaf=entry.get("is_leaf", False),
            source_artifact=artifact_models[entry["source_artifact_id"]],
            source_locator=entry["source_locator"],
            treatment_metadata=entry.get("treatment_metadata", {}),
            knowledge_treatment=entry.get("knowledge_treatment", "UNSPECIFIED"),
            normalization_notes=entry.get("normalization_notes", ""),
        )
    scope.normalized_sha256 = "2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f"
    scope.status = OfficialScopeVersion.Status.ACTIVE
    scope.save()
    return scope


def _install_accepted_pilot_snapshot(scope):
    authority = AuthoritySource.objects.create(
        stable_id="USCOURTS_FRCP",
        source_version="2025-12-01",
        authority_class="SUBSTANTIVE_PRIMARY",
        authority_type="FEDERAL_RULES_OF_CIVIL_PROCEDURE",
        title="Federal Rules of Civil Procedure",
        canonical_citation="Fed. R. Civ. P. (Dec. 1, 2025)",
        source_uri="https://www.uscourts.gov/",
        content_sha256="bd8705fc038d87e4fe222a7ea2e4324222c9430e2373fce56826bd2dfa2f8baf",
        source_class="PRODUCTION",
        is_national=True,
    )
    policy = CoveragePolicy.objects.create(
        stable_id="BARCLIMB_FRCP_RULE4_SERVICE_PILOT",
        policy_version="2025_V2",
        minimum_obligations_per_leaf=1,
        requires_primary_authority=True,
        allowed_obligation_kinds=["RULE", "LIMITATION", "PROCEDURAL_STEP", "REMEDY"],
        canonical_sha256="a" * 64,
        source_class="PRODUCTION",
        coverage_class="PILOT_ONLY",
        target_scope_item_ids=["civil-procedure-service-process-notice"],
        requires_human_review=True,
    )
    compile_version = CurriculumCompileVersion.objects.create(
        version_identifier="BARCLIMB_PILOT_FRCP_RULE4_2025_V2",
        official_scope_version=scope,
        coverage_policy=policy,
        compiler_schema_version="BARCLIMB_RULE_COMPILER_V2",
        input_sha256="b" * 64,
        canonical_sha256="0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec",
        status="CERTIFIED",
        source_class="PRODUCTION",
        coverage_class="PILOT_ONLY",
        national_complete=False,
        certified_at=datetime(2026, 8, 21, 20, 2, 43, tzinfo=timezone.utc),
    )
    snapshot = CoverageReleaseSnapshot.objects.create(
        id="8ffc025a-ddac-5765-b7b2-130c84282c83",
        compile_version=compile_version,
        official_scope_version=scope,
        compiler_schema_version="BARCLIMB_RULE_COMPILER_V2",
        source_class="PRODUCTION",
        coverage_class="PILOT_ONLY",
        national_complete=False,
        authority_provenance_sha256="fa2a1355e70676f95fff5f02bc8c4ad03ce7594fc64be98dbf87c4cf5a0ce46c",
        human_review_sha256="903ab69e9171969b826060943e25d8e40fcf84d4968525663197b43165c74e44",
        human_review_status="APPROVED",
        obligation_count=8,
        leaf_count=1,
        covered_leaf_count=1,
        blocking_issue_count=0,
        warning_issue_count=0,
        coverage_results={"coverage_class": "PILOT_ONLY", "national_complete": False},
        certification_sha256="60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0",
        certified_at=datetime(2026, 8, 21, 20, 2, 43, tzinfo=timezone.utc),
    )
    return authority, snapshot


def _import_plan():
    scope = _install_scope_descriptor()
    _install_accepted_pilot_snapshot(scope)
    return import_subject_plan(_json(PLAN_PATH))[0]


def test_plan_is_hash_exact_body_free_and_contains_all_real_civil_procedure_leaves():
    payload = _json(PLAN_PATH)
    assert payload["canonical_sha256"] == canonical_sha256(
        {key: value for key, value in payload.items() if key != "canonical_sha256"}
    )
    assert {leaf["scope_item_id"] for leaf in payload["leaves"]} == EXPECTED_LEAF_IDS
    encoded = PLAN_PATH.read_text()
    assert '"statement"' not in encoded and '"obligations"' not in encoded
    assert "California" not in encoded and "New York" not in encoded


def test_import_creates_versioned_manifest_complete_requirement_map_and_authority_plan():
    manifest = _import_plan()
    same, created = import_subject_plan(_json(PLAN_PATH))
    assert same.pk == manifest.pk and not created
    report = subject_coverage_report(manifest)
    assert manifest.canonical_sha256 == (
        "8fd6506bfc4cfda72e1ee6aaad6d62f8ab233fb1c48ff45c308e01b12b60ebd8"
    )
    assert report["official_scope_sha256"] == (
        "2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f"
    )
    assert report["official_leaf_count"] == 6
    assert report["coverage_requirement_count"] == 18
    assert report["required_slot_count"] == 75
    assert report["authority_plan_count"] == 16
    assert set(report["uncovered_leaf_ids"]) == EXPECTED_LEAF_IDS
    assert all(leaf.coverage_requirements.exists() for leaf in manifest.manifest_leaves.all())
    assert not manifest.authority_plans.filter(freshness_requirement="", drift_action="").exists()
    assert not RuleObligation.objects.exists()
    with pytest.raises(ValidationError):
        manifest.save()


def test_multi_authority_erie_case_plan_and_secondary_non_substitution_are_explicit():
    manifest = _import_plan()
    requirement = manifest.manifest_leaves.get(
        scope_item__stable_id="civil-procedure-litigation"
    ).coverage_requirements.get(stable_id="civpro-erie-hanna-cluster")
    required = set(
        requirement.authority_mappings.filter(role="REQUIRED").values_list(
            "authority_plan__stable_id", flat=True
        )
    )
    assert required == {
        "authority-us-constitution-article-iii",
        "authority-28-usc-law-applied",
        "authority-rules-enabling-act",
        "authority-frcp-current",
        "authority-scotus-erie",
    }
    case_plan = manifest.authority_plans.get(stable_id="authority-scotus-erie")
    case_requirement = case_plan.case_requirements.get()
    assert case_requirement.exact_case_identity_required
    assert case_requirement.proposition_locator_required
    assert case_requirement.later_treatment_review_required
    secondary = requirement.authority_mappings.get(
        authority_plan__stable_id="authority-optional-secondary-reconciliation"
    )
    assert secondary.role == "OPTIONAL_RECONCILIATION"
    with pytest.raises(ValidationError, match="Secondary evidence cannot replace"):
        RequirementAuthorityPlan(
            requirement=requirement,
            authority_plan=secondary.authority_plan,
            role="REQUIRED",
            proposition_types=["GOVERNING_RULE"],
            canonical_sha256="c" * 64,
        ).full_clean()


def test_treatment_procedural_branching_and_federal_state_distinction_are_preserved():
    manifest = _import_plan()
    service = manifest.manifest_leaves.get(
        scope_item__stable_id="civil-procedure-service-process-notice"
    )
    assert service.treatment == "RECOGNITION_WITH_OR_WITHOUT_RESOURCES"
    treatments = set(service.coverage_requirements.values_list("treatment_requirement", flat=True))
    assert treatments == {"RECOGNITION", "RESOURCE_APPLICATION", "MIXED"}
    erie = manifest.manifest_leaves.get(
        scope_item__stable_id="civil-procedure-litigation"
    ).coverage_requirements.get(stable_id="civpro-erie-hanna-cluster")
    assert erie.slots.filter(obligation_kind="DISTINCTION").exists()
    erie_distinction = erie.slots.get(obligation_kind="DISTINCTION")
    assert erie_distinction.relationship_expectations == [
        {
            "source_slot_id": "civpro-erie-hanna-cluster-rule",
            "relationship_kind": "HAS_DISTINCTION",
        }
    ]
    procedural = manifest.manifest_leaves.get(
        scope_item__stable_id="civil-procedure-appeals"
    ).coverage_requirements.get(stable_id="civpro-appellate-procedure-review")
    assert set(procedural.slots.values_list("obligation_kind", flat=True)) >= {
        "RULE",
        "PROCEDURAL_STEP",
        "LIMITATION",
        "DISTINCTION",
        "REMEDY",
    }
    assert procedural.slots.get(obligation_kind="PROCEDURAL_STEP").relationship_expectations


def test_rule4_snapshot_is_linked_as_partial_without_mutating_pilot_truth():
    before = hashlib.sha256(PILOT_PATH.read_bytes()).hexdigest()
    manifest = _import_plan()
    service = manifest.manifest_leaves.get(
        scope_item__stable_id="civil-procedure-service-process-notice"
    )
    subset = service.certified_subsets.select_related("coverage_snapshot__compile_version").get()
    assert str(subset.coverage_snapshot_id) == "8ffc025a-ddac-5765-b7b2-130c84282c83"
    assert subset.coverage_snapshot.compile_version.canonical_sha256 == (
        "0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec"
    )
    assert subset.coverage_snapshot.certification_sha256 == (
        "60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0"
    )
    assert subset.contribution_class == "PARTIAL_LEAF_COVERAGE"
    assert service.coverage_status == "PARTIALLY_COVERED"
    assert hashlib.sha256(PILOT_PATH.read_bytes()).hexdigest() == before


def test_report_cannot_infer_certification_from_counts_and_lists_every_gap():
    manifest = _import_plan()
    report = subject_coverage_report(manifest)
    assert report["certified_slot_count"] == 0
    assert report["unresolved_candidate_slot_count"] == 75
    assert report["unresolved_authority_gap_count"] == 15
    assert report["unresolved_human_review_count"] == 1
    assert report["structurally_eligible"] is False
    assert report["subject_certified"] is False
    assert report["subject_complete"] is False
    assert report["national_complete"] is False
    with pytest.raises(ValidationError, match="subject_certification_blocked"):
        assert_subject_certification_ready(manifest)


def test_external_human_review_is_explicit_immutable_and_does_not_certify_subject(tmp_path):
    manifest = _import_plan()
    payload = {
        "subject_manifest": {
            "stable_id": manifest.stable_id,
            "manifest_version": manifest.manifest_version,
        },
        "reviewer_name": "TEST REVIEWER",
        "reviewer_role_qualification": "TEST QUALIFICATION",
        "resolution": "APPROVE",
        "rationale": "TEST review of the coverage plan only.",
        "attestation": "TEST attestation; no substantive obligations approved.",
        "review_packet_sha256": hashlib.sha256(REVIEW_PACKET_PATH.read_bytes()).hexdigest(),
        "reviewed_at": "2026-08-21T00:00:00+00:00",
    }
    review_manifest = tmp_path / "subject-review.json"
    review_manifest.write_text(json.dumps(payload))
    stdout = StringIO()
    call_command(
        "record_subject_plan_review",
        review_manifest,
        "--packet",
        REVIEW_PACKET_PATH,
        stdout=stdout,
    )
    result = json.loads(stdout.getvalue())
    assert result["created"] and result["resolution"] == "APPROVE"
    review = SubjectPlanHumanReview.objects.get(manifest=manifest)
    stdout = StringIO()
    call_command(
        "record_subject_plan_review",
        review_manifest,
        "--packet",
        REVIEW_PACKET_PATH,
        stdout=stdout,
    )
    assert json.loads(stdout.getvalue())["created"] is False
    assert subject_coverage_report(manifest)["human_review_status"] == "APPROVE"
    assert subject_coverage_report(manifest)["subject_complete"] is False
    with pytest.raises(ValidationError):
        review.save()
    wrong_packet = tmp_path / "wrong-packet.md"
    wrong_packet.write_text("different")
    with pytest.raises(CommandError, match="does not match"):
        call_command(
            "record_subject_plan_review",
            review_manifest,
            "--packet",
            wrong_packet,
            stdout=StringIO(),
        )


def test_new_policy_manifest_version_preserves_historical_v1():
    original = _import_plan()
    payload = copy.deepcopy(_json(PLAN_PATH))
    payload["manifest"]["manifest_version"] = "2026_V2_TEST"
    payload["manifest"]["supersedes"] = {
        "stable_id": original.stable_id,
        "manifest_version": original.manifest_version,
    }
    payload["coverage_policy"]["policy_version"] = "2026_V2_TEST"
    payload["coverage_policy"]["supersedes"] = {
        "stable_id": original.coverage_policy.stable_id,
        "policy_version": original.coverage_policy.policy_version,
    }
    _rechecksum(payload)
    successor, created = import_subject_plan(payload)
    assert created and successor.supersedes == original
    assert successor.coverage_policy.supersedes == original.coverage_policy
    original.refresh_from_db()
    assert original.manifest_version == "2026_V1"
    assert original.canonical_sha256 == (
        "8fd6506bfc4cfda72e1ee6aaad6d62f8ab233fb1c48ff45c308e01b12b60ebd8"
    )


def test_operator_report_answers_remaining_work_without_hidden_certification():
    manifest = _import_plan()
    stdout = StringIO()
    call_command(
        "report_subject_coverage",
        f"{manifest.stable_id}@{manifest.manifest_version}",
        stdout=stdout,
    )
    report = json.loads(stdout.getvalue())
    assert report["official_leaf_count"] == 6
    assert report["uncovered_leaf_ids"]
    assert report["unresolved_authority_gap_count"] == 15
    assert report["unresolved_candidate_slot_count"] == 75
    assert report["subject_complete"] is False


@pytest.mark.postgres
def test_postgres_subject_plan_records_are_database_immutable():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL-specific subject-plan trigger")
    manifest = _import_plan()
    leaf = manifest.manifest_leaves.first()
    with pytest.raises(DatabaseError), transaction.atomic():
        SubjectManifestLeaf.objects.filter(pk=leaf.pk).update(coverage_status="LEAF_CERTIFIED")
    with pytest.raises(DatabaseError), transaction.atomic():
        SubjectCurriculumManifest.objects.filter(pk=manifest.pk).delete()
    assert not SubjectPlanHumanReview.objects.exists()
