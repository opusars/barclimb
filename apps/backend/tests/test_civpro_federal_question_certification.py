import copy
import json
from io import StringIO
from pathlib import Path

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils.dateparse import parse_datetime
from test_civil_procedure_subject_plan import V3_REVIEW_RECORD_PATH
from test_civpro_federal_question_candidates import (
    REVIEW_PACKET_PATH,
    RULE4_CERTIFICATION,
    RULE4_COMPILE,
    RULE4_SNAPSHOT,
    TOPIC_ID,
    _compile,
    _review_payload,
)

from curriculum.models import (
    CoverageReleaseSnapshot,
    CoverageRequirementSatisfaction,
    ReconciliationIssue,
)
from curriculum.services import reconcile_curriculum, record_obligation_review
from curriculum.subject_planning import subject_coverage_report
from official_scope.services import canonical_sha256

pytestmark = pytest.mark.django_db

BACKEND_ROOT = Path(__file__).resolve().parents[1]
CERTIFICATION_PATH = (
    BACKEND_ROOT / "curriculum" / "manifests" / "civpro-federal-question-certification-2026-v1.json"
)


def _review(compile_version, tmp_path):
    payload = _review_payload(compile_version)
    path = tmp_path / "review.json"
    path.write_text(json.dumps(payload))
    call_command(
        "apply_obligation_reviews",
        path,
        "--packet",
        REVIEW_PACKET_PATH,
        stdout=StringIO(),
    )
    compile_version.refresh_from_db()
    return payload


def _certification_payload(compile_version):
    payload = json.loads(CERTIFICATION_PATH.read_text())
    payload["compile_sha256"] = compile_version.canonical_sha256
    payload["compile_input_sha256"] = compile_version.input_sha256
    payload["coverage_policy_sha256"] = compile_version.coverage_policy.canonical_sha256
    mappings = {
        mapping.obligation.stable_id: mapping
        for mapping in compile_version.obligations.select_related(
            "candidate_requirement_mapping__slot"
        )
        for mapping in [mapping.candidate_requirement_mapping]
    }
    for candidate in payload["candidates"]:
        mapping = mappings[candidate["stable_id"]]
        obligation = mapping.obligation
        review = getattr(obligation, "human_review", None)
        candidate["candidate_sha256"] = obligation.canonical_sha256
        candidate["mapping_sha256"] = mapping.canonical_sha256
        if review is not None:
            candidate["review_manifest_sha256"] = review.review_manifest_sha256
            candidate["reviewed_at"] = review.reviewed_at.isoformat()
        actual_evidence = list(
            obligation.authority_evidence.select_related("authority").order_by(
                "authority__stable_id", "locator"
            )
        )
        candidate["authority_evidence"] = [
            {
                "authority_id": item.authority.stable_id,
                "source_version": item.authority.source_version,
                "source_sha256": item.authority.content_sha256,
                "proposition_type": item.proposition_type,
                "proposition_sha256": item.proposition_sha256,
                "locator": item.locator,
            }
            for item in actual_evidence
        ]
    return payload


def _certify(compile_version, tmp_path, payload=None):
    payload = copy.deepcopy(payload or _certification_payload(compile_version))
    path = tmp_path / "certification.json"
    path.write_text(json.dumps(payload))
    output = StringIO()
    call_command(
        "certify_topic_coverage",
        path,
        "--subject-review-record",
        V3_REVIEW_RECORD_PATH,
        stdout=output,
    )
    return json.loads(output.getvalue()), payload


def test_exact_federal_question_topic_certifies_and_replays_idempotently(tmp_path):
    compile_version, _report, *_ = _compile()
    _review(compile_version, tmp_path)
    compile_version, _report = reconcile_curriculum(compile_version.pk)
    first, payload = _certify(compile_version, tmp_path)
    second, _ = _certify(compile_version, tmp_path, payload)

    assert first == second
    assert first["topic_id"] == TOPIC_ID
    assert first["slot_count"] == 3
    assert first["topic_certified"] is True
    assert first["subject_complete"] is False
    assert first["subject_certified"] is False
    assert first["national_complete"] is False
    assert CoverageReleaseSnapshot.objects.filter(compile_version=compile_version).count() == 1
    satisfactions = CoverageRequirementSatisfaction.objects.filter(
        coverage_snapshot_id=first["snapshot_id"]
    )
    assert satisfactions.count() == 3
    assert set(satisfactions.values_list("slot__stable_id", flat=True)) == {
        "civpro-federal-question-rule",
        "civpro-federal-question-element",
        "civpro-federal-question-limitation",
    }

    subject = subject_coverage_report(
        compile_version.obligations.first().candidate_requirement_mapping.official_topic.manifest
    )
    topic = next(
        item
        for item in subject["official_terminal_topic_results"]
        if item["official_topic_id"] == TOPIC_ID
    )
    assert topic["certified_slot_count"] == 3 and topic["structurally_complete"] is True
    assert topic["topic_certified"] is True
    assert subject["certified_slot_count"] == 3
    assert subject["unresolved_candidate_slot_count"] == 146
    assert subject["authority_status_counts"] == {
        "ACQUIRED": 1,
        "PARTIALLY_ACQUIRED": 2,
        "PLANNED": 19,
    }
    assert subject["subject_complete"] is False
    assert subject["subject_certified"] is False
    assert subject["national_complete"] is False

    rule4 = CoverageReleaseSnapshot.objects.get(pk=RULE4_SNAPSHOT)
    assert rule4.compile_version.canonical_sha256 == RULE4_COMPILE
    assert rule4.certification_sha256 == RULE4_CERTIFICATION


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("compile_input_sha256", "compile_input_sha256"),
        ("topic_sha256", "topic_sha256"),
        ("requirement_sha256", "requirement_sha256"),
        ("subject_plan_review_manifest_sha256", "subject_plan_review_manifest_sha256"),
    ],
)
def test_changed_certification_binding_is_rejected(tmp_path, field, expected):
    compile_version, *_ = _compile()
    _review(compile_version, tmp_path)
    compile_version, _ = reconcile_curriculum(compile_version.pk)
    payload = _certification_payload(compile_version)
    payload[field] = "0" * 64
    with pytest.raises(CommandError, match=expected):
        _certify(compile_version, tmp_path, payload)


def test_missing_candidate_approval_and_reconciliation_blocker_prevent_certification(tmp_path):
    compile_version, *_ = _compile()
    review_payload = _review_payload(compile_version)
    manifest_sha256 = canonical_sha256(review_payload)
    reviewed_at = parse_datetime(review_payload["reviewed_at"])
    for decision in review_payload["decisions"][:2]:
        record_obligation_review(
            compile_version.obligations.get(stable_id=decision["obligation"]).pk,
            reviewer=None,
            reviewer_name=review_payload["reviewer"]["name"],
            reviewer_role_qualification=review_payload["reviewer"]["role_qualification"],
            resolution=decision["resolution"],
            rationale=review_payload["rationale"],
            attestation=review_payload["attestation"],
            authority_reviewed=True,
            review_manifest_sha256=manifest_sha256,
            reviewed_at=reviewed_at,
            operator_manifest=True,
        )
    compile_version, _ = reconcile_curriculum(compile_version.pk)
    with pytest.raises(CommandError, match="lacks clean reconciliation and approval"):
        _certify(compile_version, tmp_path)


def test_open_reconciliation_blocker_prevents_topic_certification(tmp_path):
    compile_version, *_ = _compile()
    _review(compile_version, tmp_path)
    compile_version, _ = reconcile_curriculum(compile_version.pk)
    ReconciliationIssue.objects.create(
        compile_version=compile_version,
        stable_id="topic-certification-test-blocker",
        category="CONFLICT",
        severity="BLOCKING",
        status="OPEN",
        message="Deterministic test blocker.",
        canonical_sha256=canonical_sha256({"test": "blocker"}),
    )
    with pytest.raises(CommandError, match="blocking_issues"):
        _certify(compile_version, tmp_path)


def test_changed_candidate_truth_cannot_inherit_certification(tmp_path):
    compile_version, *_ = _compile()
    _review(compile_version, tmp_path)
    compile_version, _ = reconcile_curriculum(compile_version.pk)
    payload = _certification_payload(compile_version)
    payload["candidates"][0]["candidate_sha256"] = "0" * 64
    with pytest.raises(CommandError, match="candidate/review/authority truth changed"):
        _certify(compile_version, tmp_path, payload)


def test_certification_descriptor_is_bounded_and_preserves_review_identity():
    payload = json.loads(CERTIFICATION_PATH.read_text())
    assert payload["topic_id"] == TOPIC_ID
    assert payload["requirement_id"] == "civpro-federal-question"
    assert payload["national_complete"] is False
    assert (
        payload["compile_sha256"]
        == "a46fbd51a441ec54fa74f2826a50241ff94e4fd3eefa49e24e568174d15b606d"
    )
    assert (
        payload["compile_input_sha256"]
        == "238b15e7b5bfc492ebb5dde77a88c09b09a4bafd463f772c3cbe24277fb03f4f"
    )
    assert {item["review_manifest_sha256"] for item in payload["candidates"]} == {
        "9bc7dd30872b6b36126f2c1a1771bdde2d33ac58a029c8fdfe5d5e6092c355d7"
    }
    authority_ids = {
        evidence["authority_id"]
        for item in payload["candidates"]
        for evidence in item["authority_evidence"]
    }
    assert authority_ids == {
        "USCODE_28_USC_1331",
        "SCOTUS_US_REPORTS_MOTTLEY_211_US_149",
    }
    encoded = CERTIFICATION_PATH.read_text().lower()
    for excluded in ("diversity jurisdiction", "supplemental jurisdiction", "removal procedure"):
        assert excluded not in encoded
