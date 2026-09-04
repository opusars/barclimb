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
from test_civil_procedure_subject_plan import (
    EXPECTED_TERMINAL_TOPIC_IDS,
    REVIEW_PACKET_V3_REVIEWED_PATH,
    V3_REVIEW_RECORD_PATH,
    _import_v3_plan,
)

from curriculum.models import (
    AuthoritySource,
    CandidateRequirementMapping,
    CoverageReleaseSnapshot,
    ObligationHumanReview,
    ScopeCoverageRequirement,
    SubjectAuthorityAcquisition,
)
from curriculum.services import compile_manifest, compile_result, reconcile_curriculum
from curriculum.subject_planning import subject_coverage_report

pytestmark = pytest.mark.django_db

BACKEND_ROOT = Path(__file__).resolve().parents[1]
CANDIDATE_PATH = (
    BACKEND_ROOT / "curriculum" / "manifests" / "civpro-federal-question-candidates-2026-v1.json"
)
REVIEW_PATH = (
    BACKEND_ROOT / "curriculum" / "manifests" / "civpro-federal-question-review-2026-v1.json"
)
REVIEW_PACKET_PATH = (
    BACKEND_ROOT.parent.parent
    / "docs"
    / "project"
    / "M2_2D_CIVPRO_FEDERAL_QUESTION_HUMAN_REVIEW_PACKET_REVIEWED.md"
)
TOPIC_ID = "civpro-topic-federal-question-jurisdiction"
REQUIREMENT_ID = "civpro-federal-question"
EXPECTED_SLOTS = {
    "civpro-federal-question-rule": "RULE",
    "civpro-federal-question-element": "ELEMENT",
    "civpro-federal-question-limitation": "LIMITATION",
}
RULE4_COMPILE = "0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec"
RULE4_SNAPSHOT = "8ffc025a-ddac-5765-b7b2-130c84282c83"
RULE4_CERTIFICATION = "60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0"


def _json(path=CANDIDATE_PATH):
    return json.loads(path.read_text())


def _approved_v3_plan():
    manifest = _import_v3_plan()
    call_command(
        "record_subject_plan_review",
        V3_REVIEW_RECORD_PATH,
        "--packet",
        REVIEW_PACKET_V3_REVIEWED_PATH,
        stdout=StringIO(),
    )
    manifest.refresh_from_db()
    return manifest


def _authority_bytes(payload):
    contents = {
        "USCODE_28_USC_1331": b"DETERMINISTIC_TEST_28_USC_1331",
        "SCOTUS_US_REPORTS_MOTTLEY_211_US_149": b"DETERMINISTIC_TEST_MOTTLEY_211_US_149",
    }
    for authority in payload["authorities"]:
        authority["expected_sha256"] = hashlib.sha256(contents[authority["stable_id"]]).hexdigest()
    return contents


def _compile(payload=None):
    _approved_v3_plan()
    payload = copy.deepcopy(payload or _json())
    contents = _authority_bytes(payload)
    compile_version, created = compile_manifest(payload, authority_contents=contents)
    compile_version, report = reconcile_curriculum(compile_version.pk)
    return compile_version, report, created, payload, contents


def _review_payload(compile_version):
    review = _json(REVIEW_PATH)
    review["input_checksum"] = compile_version.input_sha256
    review["scope_checksum"] = compile_version.official_scope_version.normalized_sha256
    authorities = {
        authority.stable_id: authority
        for authority in AuthoritySource.objects.filter(
            authorityevidence__obligation__compile_version=compile_version
        ).distinct()
    }
    for authority in review["authorities"]:
        authority["sha256"] = authorities[authority["stable_id"]].content_sha256
    for candidate in review["candidates"]:
        obligation = compile_version.obligations.get(stable_id=candidate["stable_id"])
        candidate["candidate_canonical_sha256"] = obligation.canonical_sha256
        candidate["mapping_sha256"] = obligation.candidate_requirement_mapping.canonical_sha256
        for evidence in candidate["authority_evidence"]:
            evidence["source_sha256"] = authorities[evidence["authority_id"]].content_sha256
    return review


def test_committed_descriptor_is_hash_only_and_bounded_to_federal_question():
    payload = _json()
    assert {entry["stable_id"] for entry in payload["authorities"]} == {
        "USCODE_28_USC_1331",
        "SCOTUS_US_REPORTS_MOTTLEY_211_US_149",
    }
    assert all("content_base64" not in entry for entry in payload["authorities"])
    assert all(
        entry["storage_disposition"] == "TRANSIENT_HASH_ONLY" for entry in payload["authorities"]
    )
    cluster = payload["subject_candidate_cluster"]
    assert cluster["official_topic_id"] == TOPIC_ID
    assert cluster["requirement_id"] == REQUIREMENT_ID
    assert set(cluster["target_slot_ids"]) == set(EXPECTED_SLOTS)
    encoded = CANDIDATE_PATH.read_text().lower()
    for prohibited in (
        "complete preemption",
        "supplemental jurisdiction",
        "diversity jurisdiction",
        "removal procedure",
        "grable",
        "gunn",
    ):
        assert prohibited not in encoded


def test_compile_maps_three_review_pending_candidates_to_exact_approved_slots():
    compile_version, report, created, _, _ = _compile()
    assert created and compile_version.status == "RECONCILED"
    assert compile_version.coverage_class == "PILOT_ONLY"
    assert compile_version.national_complete is False
    assert report["blocking_issue_count"] == 0
    assert report["warning_issue_count"] == 0
    assert report["subject_candidate_topic_ids"] == [TOPIC_ID]
    assert report["subject_candidate_requirement_ids"] == [REQUIREMENT_ID]
    assert report["candidate_human_review_status"] == "PENDING"
    assert report["subject_certified"] is False
    assert {
        entry["slot_id"]: entry["obligation_kind"] for entry in report["candidate_slot_results"]
    } == EXPECTED_SLOTS
    assert all(entry["sufficient"] for entry in report["candidate_slot_results"])

    mappings = CandidateRequirementMapping.objects.select_related(
        "obligation", "slot", "official_topic"
    )
    assert mappings.count() == 3
    assert {mapping.official_topic.stable_id for mapping in mappings} == {TOPIC_ID}
    assert {mapping.slot.requirement.stable_id for mapping in mappings} == {REQUIREMENT_ID}
    assert {
        mapping.slot.stable_id: mapping.obligation.kind for mapping in mappings
    } == EXPECTED_SLOTS
    assert {mapping.inherited_treatment for mapping in mappings} == {"RECALLED_REQUIRED"}
    assert set(compile_version.obligations.values_list("decision", flat=True)) == {
        "REVIEW_REQUIRED"
    }
    assert set(compile_version.obligations.values_list("reconciliation_status", flat=True)) == {
        "RECONCILED"
    }
    result = compile_result(compile_version)
    assert result["human_review_pending_count"] == 3
    assert result["certification_eligible"] is False
    assert not ObligationHumanReview.objects.filter(
        obligation__compile_version=compile_version
    ).exists()
    assert not CoverageReleaseSnapshot.objects.filter(compile_version=compile_version).exists()


def test_exact_human_reviews_bind_all_candidate_evidence_and_replay_idempotently(tmp_path):
    compile_version, _, _, _, _ = _compile()
    review = _review_payload(compile_version)
    review_path = tmp_path / "review.json"
    review_path.write_text(json.dumps(review))
    first_stdout = StringIO()
    call_command(
        "apply_obligation_reviews",
        review_path,
        "--packet",
        REVIEW_PACKET_PATH,
        stdout=first_stdout,
    )
    first = json.loads(first_stdout.getvalue())
    second_stdout = StringIO()
    call_command(
        "apply_obligation_reviews",
        review_path,
        "--packet",
        REVIEW_PACKET_PATH,
        stdout=second_stdout,
    )
    second = json.loads(second_stdout.getvalue())

    assert first["reviews_created"] == 3 and second["reviews_created"] == 0
    assert first["review_manifest_sha256"] == second["review_manifest_sha256"]
    assert [entry["record_sha256"] for entry in first["review_records"]] == [
        entry["record_sha256"] for entry in second["review_records"]
    ]
    assert {entry["created"] for entry in second["review_records"]} == {False}
    reviews = ObligationHumanReview.objects.filter(
        obligation__compile_version=compile_version
    ).select_related("obligation")
    assert reviews.count() == 3
    assert {review.reviewer_name for review in reviews} == {"Leo Rayos"}
    assert {review.reviewer_role_qualification for review in reviews} == {
        "JD; California bar exam passer; reviewer for BarClimb curriculum quality control."
    }
    assert {review.resolution for review in reviews} == {"APPROVE"}
    assert compile_result(compile_version)["human_review_pending_count"] == 0
    assert compile_result(compile_version)["certification_eligible"] is True
    compile_version.refresh_from_db()
    assert compile_version.reconciliation_report["candidate_human_review_status"] == "APPROVED"
    assert compile_version.reconciliation_report["subject_certified"] is False
    assert compile_version.reconciliation_report["national_complete"] is False
    assert not CoverageReleaseSnapshot.objects.filter(compile_version=compile_version).exists()

    subject_report = subject_coverage_report(
        compile_version.obligations.first().candidate_requirement_mapping.official_topic.manifest
    )
    assert subject_report["subject_complete"] is False
    assert subject_report["subject_certified"] is False
    assert subject_report["national_complete"] is False


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        ("statement", "candidate statements or evidence bindings differ"),
        ("authority", "candidate statements or evidence bindings differ"),
        ("relationship", "obligation relationships differ"),
        ("compile", "compile_checksum"),
        ("input", "input_checksum"),
        ("packet", "reviewed_packet"),
    ],
)
def test_human_review_rejects_changed_exact_evidence(tmp_path, mutation, expected):
    compile_version, _, _, _, _ = _compile()
    review = _review_payload(compile_version)
    packet_path = REVIEW_PACKET_PATH
    if mutation == "statement":
        review["candidates"][0]["statement"] += " Changed."
    elif mutation == "authority":
        review["candidates"][0]["authority_evidence"][0]["source_sha256"] = "0" * 64
    elif mutation == "compile":
        review["compile_checksum"] = "0" * 64
    elif mutation == "input":
        review["input_checksum"] = "0" * 64
    elif mutation == "relationship":
        review["relationships"][0]["kind"] = "HAS_LIMITATION"
    else:
        packet_path = tmp_path / "changed-packet.md"
        packet_path.write_text("changed packet")
    review_path = tmp_path / "review.json"
    review_path.write_text(json.dumps(review))
    with pytest.raises(CommandError, match=expected):
        call_command(
            "apply_obligation_reviews",
            review_path,
            "--packet",
            packet_path,
            stdout=StringIO(),
        )


def test_statute_and_controlling_case_provenance_are_proposition_specific():
    compile_version, _, _, _, _ = _compile()
    rule = compile_version.obligations.get(stable_id="civpro-fq-statutory-original-jurisdiction")
    element = compile_version.obligations.get(stable_id="civpro-fq-plaintiff-claim-arising-under")
    limitation = compile_version.obligations.get(stable_id="civpro-fq-federal-defense-limitation")
    assert set(rule.authority_evidence.values_list("authority__stable_id", "proposition_type")) == {
        ("USCODE_28_USC_1331", "GOVERNING_STATUTORY_TEXT")
    }
    for candidate in (element, limitation):
        assert set(
            candidate.authority_evidence.values_list("authority__stable_id", "proposition_type")
        ) == {
            (
                "SCOTUS_US_REPORTS_MOTTLEY_211_US_149",
                "WELL_PLEADED_COMPLAINT_CONTROLLING_HOLDING",
            )
        }

    acquisitions = SubjectAuthorityAcquisition.objects.filter(requirement__stable_id=REQUIREMENT_ID)
    assert acquisitions.count() == 2
    assert {acquisition.authority_plan.stable_id for acquisition in acquisitions} == {
        "authority-28-usc-jurisdiction-removal",
        "authority-scotus-jurisdiction",
    }
    assert not acquisitions.filter(
        authority_plan__stable_id="authority-us-constitution-article-iii"
    ).exists()


def test_statute_alone_cannot_satisfy_well_pleaded_complaint_authority():
    payload = _json()
    payload["compile"]["version_identifier"] += "_STATUTE_ONLY_TEST"
    payload["coverage_policy"]["policy_version"] += "_STATUTE_ONLY_TEST"
    payload["subject_authority_acquisitions"] = payload["subject_authority_acquisitions"][:1]
    payload["authorities"] = payload["authorities"][:1]
    for obligation in payload["obligations"][1:]:
        obligation["evidence"] = [
            {
                "authority_id": "USCODE_28_USC_1331",
                "role": "SUBSTANTIVE_SUPPORT",
                "locator": "28 U.S.C. § 1331",
                "proposition_type": "GOVERNING_STATUTORY_TEXT",
                "proposition": "Statutory text alone does not establish the WPC holding.",
            }
        ]
    _, report, _, _, _ = _compile(payload)
    assert report["provenance_deficient_count"] == 1
    assert report["blocking_issue_count"] == 1


def test_conditional_article_iii_is_not_demanded_without_boundary_proposition():
    _, report, _, _, _ = _compile()
    assert report["blocking_issue_count"] == 0
    assert not SubjectAuthorityAcquisition.objects.filter(
        authority_plan__stable_id="authority-us-constitution-article-iii"
    ).exists()


def test_removal_topic_or_requirement_cannot_enter_bounded_cluster():
    _approved_v3_plan()
    payload = _json()
    payload["subject_candidate_cluster"]["official_topic_id"] = (
        "civpro-topic-concurrent-removal-jurisdiction"
    )
    contents = _authority_bytes(payload)
    with pytest.raises(ScopeCoverageRequirement.DoesNotExist):
        compile_manifest(payload, authority_contents=contents)


def test_unrelated_authority_acquisition_cannot_enter_bounded_cluster():
    _approved_v3_plan()
    payload = _json()
    payload["subject_authority_acquisitions"][0]["requirement_id"] = "civpro-diversity"
    contents = _authority_bytes(payload)
    with pytest.raises(ValidationError, match="bounded requirement"):
        compile_manifest(payload, authority_contents=contents)


@pytest.mark.parametrize(
    ("case", "expected_category"),
    [
        ("omission", "OMISSION"),
        ("excess", "EXCESS"),
        ("unsupported", "UNSUPPORTED_PROVENANCE"),
        ("conflict", "CONFLICT"),
        ("duplicate", "DUPLICATE"),
        ("invalid-structure", "INVALID_STRUCTURE"),
        ("jurisdiction", "UNSUPPORTED_JURISDICTION"),
    ],
)
def test_focused_reconciliation_detects_each_required_failure_family(case, expected_category):
    payload = _json()
    payload["compile"]["version_identifier"] += f"_{case.upper()}_TEST"
    payload["coverage_policy"]["policy_version"] += f"_{case.upper()}_TEST"
    if case == "omission":
        payload["obligations"] = payload["obligations"][:2]
        payload["relationships"] = payload["relationships"][:1]
    elif case == "excess":
        extra = copy.deepcopy(payload["obligations"][0])
        extra["stable_id"] = "civpro-fq-excess-context"
        extra["statement"] = "An unrelated contextual proposition is not perimeter coverage."
        extra["classification"] = "EXCESS"
        payload["obligations"].append(extra)
    elif case == "unsupported":
        payload["obligations"][0]["evidence"] = []
    elif case == "conflict":
        payload["obligations"][0]["conflict_group"] = "federal-question-rule"
        payload["obligations"][1]["conflict_group"] = "federal-question-rule"
    elif case == "duplicate":
        duplicate = copy.deepcopy(payload["obligations"][0])
        duplicate["stable_id"] = "civpro-fq-duplicate-rule"
        payload["obligations"].append(duplicate)
    elif case == "invalid-structure":
        payload["relationships"][0]["kind"] = "HAS_LIMITATION"
    elif case == "jurisdiction":
        payload["obligations"][0]["jurisdiction"] = "CALIFORNIA"

    compile_version, _, _, _, _ = _compile(payload)
    assert compile_version.issues.filter(category=expected_category).exists()


def test_reacquisition_is_idempotent_and_changed_bytes_require_new_authority_version():
    compile_version, _, created, payload, contents = _compile()
    replay, replay_created = compile_manifest(payload, authority_contents=contents)
    assert created and not replay_created and replay.pk == compile_version.pk
    assert AuthoritySource.objects.filter(stable_id="USCODE_28_USC_1331").count() == 1

    changed = copy.deepcopy(payload)
    changed["compile"]["version_identifier"] += "_CHANGED_BYTES_TEST"
    changed["coverage_policy"]["policy_version"] += "_CHANGED_BYTES_TEST"
    changed_contents = dict(contents)
    changed_contents["USCODE_28_USC_1331"] = b"changed statutory bytes"
    with pytest.raises(ValidationError, match="expected_sha256"):
        compile_manifest(changed, authority_contents=changed_contents)

    changed["authorities"][0]["source_version"] += "_SUCCESSOR_TEST"
    changed["authorities"][0]["expected_sha256"] = hashlib.sha256(
        changed_contents["USCODE_28_USC_1331"]
    ).hexdigest()
    successor, successor_created = compile_manifest(changed, authority_contents=changed_contents)
    assert successor_created
    assert AuthoritySource.objects.filter(stable_id="USCODE_28_USC_1331").count() == 2


def test_m2_2c_and_rule4_truth_remain_unchanged_after_candidate_compile():
    compile_version, report, _, _, _ = _compile()
    subject_manifest = CandidateRequirementMapping.objects.first().official_topic.manifest
    subject_report = subject_coverage_report(subject_manifest)
    assert (
        set(
            subject_manifest.official_topics.filter(is_terminal=True).values_list(
                "stable_id", flat=True
            )
        )
        == EXPECTED_TERMINAL_TOPIC_IDS
    )
    assert (
        subject_manifest.official_topics.filter(is_terminal=True, official_marker="STARRED").count()
        == 14
    )
    assert (
        subject_manifest.official_topics.filter(
            is_terminal=True, official_marker="UNSTARRED"
        ).count()
        == 13
    )
    assert subject_report["coverage_requirement_count"] == 43
    assert subject_report["required_slot_count"] == 149
    assert subject_report["authority_plan_count"] == 22
    assert subject_report["authority_status_counts"] == {
        "ACQUIRED": 1,
        "PARTIALLY_ACQUIRED": 2,
        "PLANNED": 19,
    }
    assert subject_report["subject_complete"] is False
    assert subject_report["subject_certified"] is False
    assert subject_report["national_complete"] is False
    assert report["national_complete"] is False
    rule4 = CoverageReleaseSnapshot.objects.get(pk=RULE4_SNAPSHOT)
    assert rule4.compile_version.canonical_sha256 == RULE4_COMPILE
    assert rule4.certification_sha256 == RULE4_CERTIFICATION


@pytest.mark.postgres
def test_postgres_candidate_and_acquisition_mappings_are_database_immutable():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL-specific candidate-foundation triggers")
    _compile()
    acquisition = SubjectAuthorityAcquisition.objects.first()
    mapping = CandidateRequirementMapping.objects.first()
    with pytest.raises(DatabaseError), transaction.atomic():
        SubjectAuthorityAcquisition.objects.filter(pk=acquisition.pk).update(locators=["mutated"])
    with pytest.raises(DatabaseError), transaction.atomic():
        CandidateRequirementMapping.objects.filter(pk=mapping.pk).delete()
