import copy
import hashlib
import json
from io import StringIO
from pathlib import Path

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import DatabaseError, connection, transaction
from rest_framework.test import APIClient

from accounts.models import User
from curriculum.models import ObligationHumanReview
from curriculum.services import (
    certify_curriculum,
    compile_manifest,
    reconcile_curriculum,
    record_obligation_review,
)
from official_scope.importer import import_manifest
from official_scope.models import OfficialScopeVersion, OfficialSourceArtifact
from official_scope.services import validate_and_activate

pytestmark = pytest.mark.django_db

BACKEND_ROOT = Path(__file__).resolve().parents[1]
SCOPE_PATH = BACKEND_ROOT / "official_scope" / "manifests" / "ncbe-nextgen-2026-07.json"
PILOT_PATH = BACKEND_ROOT / "curriculum" / "manifests" / "frcp-rule4-service-pilot.json"
REVIEW_PATH = BACKEND_ROOT / "curriculum" / "manifests" / "frcp-rule4-service-pilot-review-v2.json"


def _json(path):
    return json.loads(path.read_text())


def _production_scope():
    payload = _json(SCOPE_PATH)
    acquired = {
        "NCBE_NEXTGEN_CONTENT_SCOPE": b"DETERMINISTIC_CI_REPRESENTATION_CONTENT_SCOPE",
        "NCBE_NEXTGEN_BLUEPRINT": b"DETERMINISTIC_CI_REPRESENTATION_BLUEPRINT",
    }
    for artifact in payload["artifacts"]:
        artifact["expected_sha256"] = hashlib.sha256(acquired[artifact["stable_id"]]).hexdigest()
        artifact["retrieved_at"] = "2026-08-21T19:06:49Z"
        artifact["provenance_notes"] += " CI uses deterministic non-source bytes."
    result = import_manifest(payload, artifact_contents=acquired)
    scope = OfficialScopeVersion.objects.get(version_identifier=result["scope_version"])
    validate_and_activate(scope.pk)
    scope.refresh_from_db()
    return scope


def _pilot_payload(*, version="BARCLIMB_PILOT_FRCP_RULE4_TEST"):
    payload = _json(PILOT_PATH)
    payload["compile"]["version_identifier"] = version
    authority = b"DETERMINISTIC_CI_REPRESENTATION_FRCP_RULE_4"
    payload["authorities"][0]["expected_sha256"] = hashlib.sha256(authority).hexdigest()
    return payload, {"USCOURTS_FRCP": authority}


def test_committed_real_descriptors_are_hash_exact_body_free_and_conservative():
    scope = _json(SCOPE_PATH)
    artifacts = {entry["stable_id"]: entry for entry in scope["artifacts"]}
    assert artifacts["NCBE_NEXTGEN_CONTENT_SCOPE"]["expected_sha256"] == (
        "22aa277048c04fdd887db66284c28bade9989b9f8a654fab05781bafa5b19b1a"
    )
    assert artifacts["NCBE_NEXTGEN_BLUEPRINT"]["expected_sha256"] == (
        "358f2e77c22d588b6a5f5ca3422b5c14a6c1fea46c7d4c640ff218be847846ad"
    )
    assert all("content_base64" not in entry for entry in scope["artifacts"])
    assert all(
        entry["storage_disposition"] == "TRANSIENT_HASH_ONLY" for entry in artifacts.values()
    )
    pilot = _json(PILOT_PATH)
    assert pilot["authorities"][0]["expected_sha256"] == (
        "bd8705fc038d87e4fe222a7ea2e4324222c9430e2373fce56826bd2dfa2f8baf"
    )
    assert "content_base64" not in pilot["authorities"][0]


def test_second_review_corrections_are_preserved_in_candidate_manifest():
    pilot = _json(PILOT_PATH)
    obligations = {entry["stable_id"]: entry for entry in pilot["obligations"]}
    assert pilot["compile"]["version_identifier"] == "BARCLIMB_PILOT_FRCP_RULE4_2025_V2"
    assert pilot["coverage_policy"]["policy_version"] == "2025_V2"
    assert obligations["frcp4-service-server-qualification"]["kind"] == "LIMITATION"

    relationships = {
        (entry["source_id"], entry["kind"], entry["target_id"]) for entry in pilot["relationships"]
    }
    assert not any(
        source == "frcp4-service-plaintiff-responsibility" for source, _, _ in relationships
    )
    assert relationships == {
        (
            "frcp4-service-time-limit",
            "HAS_EXCEPTION",
            "frcp4-good-cause-extension",
        ),
        (
            "frcp4-service-time-limit",
            "HAS_REMEDY",
            "frcp4-untimely-service-response",
        ),
    }

    waiver = obligations["frcp4-waiver-request"]
    assert "for a defendant subject to Rule 4(h)" in waiver["statement"]
    assert "officer, managing or general agent" in waiver["statement"]
    assert "generic authorized representative" not in waiver["statement"]
    assert "Rule 4(d)(1)(A)–(G)" in waiver["evidence"][0]["locator"]

    expense = obligations["frcp4-waiver-expense-consequence"]["statement"]
    assert "defendant located within the United States" in expense
    assert "plaintiff located within the United States" in expense
    assert "including attorney’s fees" in expense

    domestic = obligations["frcp4-domestic-individual-service"]["statement"]
    assert "state where the district court sits" in domestic
    assert "state where service is made" in domestic
    assert "methods listed in Rule 4(e)(2)" in domestic
    assert "federal delivery methods" not in domestic

    unchanged = {
        "frcp4-service-time-limit": (
            "Rule 4(m) generally requires service within 90 days after the complaint is filed, "
            "subject to the rule's extension and inapplicability provisions."
        ),
        "frcp4-good-cause-extension": (
            "If the plaintiff shows good cause for failure to serve within Rule 4(m)'s period, "
            "the court must extend the time for service for an appropriate period."
        ),
        "frcp4-untimely-service-response": (
            "After notice to the plaintiff, the court must dismiss without prejudice against an "
            "unserved defendant or order service within a specified time when Rule 4(m)'s period "
            "expires."
        ),
    }
    assert all(
        obligations[stable_id]["statement"] == statement
        for stable_id, statement in unchanged.items()
    )


def test_real_scope_registration_activation_treatment_and_api_body_isolation():
    scope = _production_scope()
    assert scope.status == "ACTIVE" and scope.release_class == "CURRENT"
    assert scope.administration_start.isoformat() == "2026-07-01"
    assert scope.source_artifacts.count() == 2
    assert scope.items.count() == 32 and scope.items.filter(is_leaf=True).count() == 26
    service = scope.items.get(stable_id="civil-procedure-service-process-notice")
    assert service.knowledge_treatment == "RECOGNITION_WITH_OR_WITHOUT_RESOURCES"
    assert service.treatment_metadata["resource_treatment"].startswith("MAY_BE_TESTED")
    assert scope.items.get(stable_id="context-family-law").knowledge_treatment == (
        "RESOURCES_ALWAYS_PROVIDED"
    )
    assert scope.items.get(stable_id="context-trusts-estates").perimeter == "CONTEXT"
    user = User.objects.create_user("reader@example.com", "reader", "strong-password-1")
    client = APIClient()
    client.force_authenticate(user)
    response = client.get("/api/v1/official-scope/active/")
    assert response.status_code == 200
    encoded = json.dumps(response.data)
    assert "content_base64" not in encoded and "rights_basis" not in encoded
    assert response.data["release_class"] == "CURRENT"


def test_reacquisition_is_idempotent_changed_bytes_refused_and_new_version_retained():
    scope = _production_scope()
    artifact = scope.source_artifacts.get(stable_id="NCBE_NEXTGEN_CONTENT_SCOPE")
    payload = _json(SCOPE_PATH)
    acquired = {
        "NCBE_NEXTGEN_CONTENT_SCOPE": b"DETERMINISTIC_CI_REPRESENTATION_CONTENT_SCOPE",
        "NCBE_NEXTGEN_BLUEPRINT": b"DETERMINISTIC_CI_REPRESENTATION_BLUEPRINT",
    }
    for entry in payload["artifacts"]:
        entry["expected_sha256"] = hashlib.sha256(acquired[entry["stable_id"]]).hexdigest()
        entry["provenance_notes"] += " CI uses deterministic non-source bytes."
    result = import_manifest(payload, artifact_contents=acquired)
    assert result["artifacts_created"] == 0
    acquired["NCBE_NEXTGEN_CONTENT_SCOPE"] = b"changed official bytes"
    with pytest.raises(ValidationError, match="expected_sha256"):
        import_manifest(payload, artifact_contents=acquired)
    successor = OfficialSourceArtifact(
        stable_id=artifact.stable_id,
        source_version="TEST_NEW_VERSION",
        source_authority=artifact.source_authority,
        artifact_type=artifact.artifact_type,
        official_title="New official version",
        content_sha256=hashlib.sha256(acquired["NCBE_NEXTGEN_CONTENT_SCOPE"]).hexdigest(),
        source_class="OFFICIAL",
        supersedes=artifact,
    )
    successor.save()
    assert successor.supersedes == artifact and artifact.has_been_superseded


def test_future_period_can_coexist_but_cannot_activate_early():
    _production_scope()
    payload = _json(SCOPE_PATH)
    payload["scope"]["version_identifier"] = "NCBE_NEXTGEN_SCOPE_2028_07_FUTURE_TEST"
    payload["scope"]["release_class"] = "FUTURE"
    payload["scope"]["administration_start"] = "2028-07-01"
    payload["scope"]["administration_end"] = "2029-02-28"
    for entry in payload["artifacts"]:
        entry["stable_id"] += "_FUTURE_TEST"
        entry["source_version"] += "_FUTURE_TEST"
        entry["source_uri"] = "https://www.ncbex.org/test-future-source"
    for source in payload["scope"]["sources"]:
        source["artifact_id"] += "_FUTURE_TEST"
    for item in payload["scope"]["items"]:
        item["source_artifact_id"] += "_FUTURE_TEST"
        if item.get("treatment_metadata", {}).get("source"):
            item["treatment_metadata"]["source"]["stable_id"] += "_FUTURE_TEST"
            item["treatment_metadata"]["source"]["source_version"] += "_FUTURE_TEST"
    acquired = {entry["stable_id"]: entry["stable_id"].encode() for entry in payload["artifacts"]}
    for entry in payload["artifacts"]:
        entry["expected_sha256"] = hashlib.sha256(acquired[entry["stable_id"]]).hexdigest()
    result = import_manifest(payload, artifact_contents=acquired)
    future = OfficialScopeVersion.objects.get(version_identifier=result["scope_version"])
    assert future.status == "VALIDATED"
    with pytest.raises(ValidationError, match="Future official scope"):
        validate_and_activate(future.pk)


def test_real_pilot_is_bounded_requires_human_review_and_certifies_only_after_attestation():
    _production_scope()
    payload, authorities = _pilot_payload()
    compile_version, created = compile_manifest(payload, authority_contents=authorities)
    assert created and set(compile_version.obligations.values_list("decision", flat=True)) == {
        "REVIEW_REQUIRED"
    }
    assert (
        compile_version.obligations.get(stable_id="frcp4-service-server-qualification").kind
        == "LIMITATION"
    )
    assert compile_version.obligations.get(
        stable_id="frcp4-waiver-request"
    ).normalized_statement.startswith(
        "a plaintiff requesting waiver of service must make the request in writing"
    )
    assert (
        compile_version.obligations.get(
            stable_id="frcp4-waiver-expense-consequence"
        ).normalized_statement.count("located within the united states")
        == 2
    )
    _, report = reconcile_curriculum(compile_version.pk)
    assert report["coverage_class"] == "PILOT_ONLY"
    assert report["target_scope_item_ids"] == ["civil-procedure-service-process-notice"]
    assert report["total_official_leaves"] == 1
    assert report["total_active_scope_leaves"] == 20
    assert report["national_complete"] is False and report["blocking_issue_count"] == 0
    with pytest.raises(ValidationError, match="human_review_required"):
        certify_curriculum(compile_version.pk)
    reviewer = User.objects.create_user(
        "legal-reviewer@example.com",
        "legal_reviewer",
        "strong-password-1",
        is_staff=True,
    )
    for obligation in compile_version.obligations.all():
        review, created = record_obligation_review(
            obligation.pk,
            reviewer=reviewer,
            reviewer_name="TEST_FIXTURE legal reviewer",
            reviewer_role_qualification="TEST_FIXTURE authenticated staff review proof",
            resolution="APPROVE",
            rationale="Deterministic CI review-boundary proof; not real legal-content approval.",
            attestation="TEST_FIXTURE authority review only; not a real substantive approval.",
            authority_reviewed=True,
            review_manifest_sha256="a" * 64,
        )
        assert created and review.resolution == "APPROVE"
    snapshot = certify_curriculum(compile_version.pk)
    assert snapshot.coverage_class == "PILOT_ONLY"
    assert snapshot.national_complete is False
    assert snapshot.human_review_status == "APPROVED"
    assert snapshot.obligation_count == 8 and snapshot.covered_leaf_count == 1
    assert len(snapshot.authority_provenance_sha256) == 64
    assert ObligationHumanReview.objects.count() == 8
    assert len(snapshot.human_review_sha256) == 64
    assert len(snapshot.human_review_evidence) == 8
    with pytest.raises(ValidationError):
        snapshot.save()


def test_named_external_review_manifest_records_exact_identity_and_certifies_bounded_pilot(
    tmp_path,
):
    scope = _production_scope()
    payload, authorities = _pilot_payload(version="BARCLIMB_PILOT_EXTERNAL_REVIEW_TEST")
    compile_version, _ = compile_manifest(payload, authority_contents=authorities)
    review = _json(REVIEW_PATH)
    review["compile_version"] = compile_version.version_identifier
    review["compile_checksum"] = compile_version.canonical_sha256
    review["scope_checksum"] = scope.normalized_sha256
    review["authority"]["sha256"] = hashlib.sha256(authorities["USCOURTS_FRCP"]).hexdigest()
    review_path = tmp_path / "review.json"
    review_path.write_text(json.dumps(review))
    stdout = StringIO()

    call_command("apply_obligation_reviews", review_path, "--certify", stdout=stdout)

    result = json.loads(stdout.getvalue())
    compile_version.refresh_from_db()
    snapshot = compile_version.coverage_snapshot
    assert result["certified"] is True and compile_version.status == "CERTIFIED"
    assert result["review_count"] == 8 and result["reviews_created"] == 8
    assert snapshot.coverage_class == "PILOT_ONLY" and snapshot.national_complete is False
    assert snapshot.leaf_count == 1 and snapshot.covered_leaf_count == 1
    assert snapshot.obligation_count == 8
    assert len(snapshot.human_review_evidence) == 8
    assert {entry["reviewer_name"] for entry in snapshot.human_review_evidence} == {"Leo Rayos"}
    assert {entry["reviewer_role_qualification"] for entry in snapshot.human_review_evidence} == {
        "JD; California bar exam passer; reviewer for BarClimb curriculum quality control."
    }
    assert not ObligationHumanReview.objects.exclude(reviewer__isnull=True).exists()
    assert set(result["resolutions"].values()) == {"APPROVE"}

    changed_review = copy.deepcopy(review)
    changed_review["decisions"][0]["resolution"] = "REJECT"
    review_path.write_text(json.dumps(changed_review))
    with pytest.raises(CommandError, match="differs from immutable input"):
        call_command("apply_obligation_reviews", review_path, "--certify", stdout=StringIO())


@pytest.mark.postgres
def test_postgres_external_human_review_is_database_immutable():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL-specific human-review trigger")
    _production_scope()
    payload, authorities = _pilot_payload(version="BARCLIMB_PILOT_REVIEW_TRIGGER_TEST")
    compile_version, _ = compile_manifest(payload, authority_contents=authorities)
    obligation = compile_version.obligations.order_by("stable_id").first()
    review, _ = record_obligation_review(
        obligation.pk,
        reviewer=None,
        reviewer_name="TEST_FIXTURE external reviewer",
        reviewer_role_qualification="TEST_FIXTURE PostgreSQL immutability proof",
        resolution="APPROVE",
        rationale="TEST_FIXTURE rationale",
        attestation="TEST_FIXTURE attestation",
        authority_reviewed=True,
        review_manifest_sha256="b" * 64,
        operator_manifest=True,
    )
    with pytest.raises(DatabaseError), transaction.atomic():
        ObligationHumanReview.objects.filter(pk=review.pk).update(rationale="changed")
    with pytest.raises(DatabaseError), transaction.atomic():
        ObligationHumanReview.objects.filter(pk=review.pk).delete()


@pytest.mark.parametrize(
    "case",
    ["missing-primary", "jurisdiction", "outside-pilot", "conflict", "secondary-only"],
)
def test_real_pilot_negative_candidates_are_rejected(case):
    _production_scope()
    payload, authorities = _pilot_payload(version=f"BARCLIMB_PILOT_NEGATIVE_{case}")
    if case == "missing-primary":
        payload["obligations"][0]["evidence"] = []
    elif case == "jurisdiction":
        payload["obligations"][0]["jurisdiction"] = "California"
    elif case == "outside-pilot":
        payload["obligations"][0]["scope_item_ids"] = ["subject-torts"]
    elif case == "conflict":
        payload["obligations"][0]["conflict_group"] = "service-rule"
        conflicting = copy.deepcopy(payload["obligations"][0])
        conflicting["stable_id"] = "frcp4-conflicting-proposition"
        conflicting["statement"] = "The plaintiff never has responsibility for service."
        payload["obligations"].append(conflicting)
    else:
        payload["authorities"][0]["authority_class"] = "SECONDARY_RECONCILIATION"
        for obligation in payload["obligations"]:
            for evidence in obligation["evidence"]:
                evidence["role"] = "SECONDARY_RECONCILIATION"
    compile_version, _ = compile_manifest(payload, authority_contents=authorities)
    reconcile_curriculum(compile_version.pk)
    assert compile_version.issues.filter(severity="BLOCKING", status="OPEN").exists()
    with pytest.raises(ValidationError):
        certify_curriculum(compile_version.pk)


def test_normalization_report_is_auditable_for_every_item():
    scope = _production_scope()
    assert scope.normalization_report["blocking_issues"] == []
    for item in scope.items.all():
        assert item.source_artifact_id and item.source_locator
        assert item.normalization_status == "AUTO_ACCEPTED"
        if item.is_leaf:
            assert item.knowledge_treatment != "UNSPECIFIED"
