from collections import Counter
from datetime import date

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from official_scope.models import OfficialScopeVersion

from .models import (
    AuthoritySource,
    CaseAuthorityRequirement,
    CoverageReleaseSnapshot,
    CoverageRequirementSlot,
    RequirementAuthorityPlan,
    ScopeCoverageRequirement,
    SubjectAuthorityPlan,
    SubjectCertifiedSubset,
    SubjectCoveragePolicy,
    SubjectCurriculumManifest,
    SubjectManifestLeaf,
    SubjectPlanHumanReview,
)
from .services import canonical_sha256

SUBJECT_PLAN_SCHEMA = "BARCLIMB_SUBJECT_COVERAGE_PLAN_V1"
SUBJECT_CERTIFICATION_GATE = "BARCLIMB_SUBJECT_CERTIFICATION_GATE_V1"
RELATIONSHIP_TARGET_KINDS = {
    "HAS_ELEMENT": "ELEMENT",
    "HAS_FACTOR": "FACTOR",
    "HAS_EXCEPTION": "EXCEPTION",
    "HAS_LIMITATION": "LIMITATION",
    "HAS_DEFENSE": "DEFENSE",
    "HAS_REMEDY": "REMEDY",
    "HAS_PROCEDURAL_STEP": "PROCEDURAL_STEP",
    "HAS_DISTINCTION": "DISTINCTION",
    "DEFINES": "DEFINITION",
    "HAS_ETHICS_DUTY": "ETHICS_DUTY",
}


def _date(value):
    return date.fromisoformat(value)


def _hierarchy_path(scope_item):
    path = []
    current = scope_item
    while current is not None:
        path.append(current.stable_id)
        current = current.parent
    return list(reversed(path))


def _entry_sha256(entry):
    return canonical_sha256(entry)


def _require_keys(entry, keys, label):
    missing = sorted(set(keys) - set(entry))
    if missing:
        raise ValidationError({label: {"missing_keys": missing}})


@transaction.atomic
def import_subject_plan(payload):
    if payload.get("schema") != SUBJECT_PLAN_SCHEMA:
        raise ValidationError("Unsupported subject-plan schema.")
    supplied_checksum = payload.get("canonical_sha256")
    canonical_payload = {key: value for key, value in payload.items() if key != "canonical_sha256"}
    calculated_checksum = canonical_sha256(canonical_payload)
    if supplied_checksum != calculated_checksum:
        raise ValidationError("Subject-plan canonical_sha256 does not match canonical payload.")

    definition = payload["manifest"]
    _require_keys(
        definition,
        {
            "stable_id",
            "manifest_version",
            "subject_id",
            "subject_label",
            "official_scope_version",
            "source_class",
        },
        "manifest",
    )
    scope = OfficialScopeVersion.objects.get(
        version_identifier=definition["official_scope_version"]
    )
    if definition.get("official_scope_sha256") != scope.normalized_sha256:
        raise ValidationError("Subject plan does not match the immutable official-scope checksum.")
    if definition["source_class"] == "PRODUCTION":
        if scope.status != OfficialScopeVersion.Status.ACTIVE or scope.is_test_fixture:
            raise ValidationError(
                "Production subject plans require active non-fixture scope truth."
            )

    existing = SubjectCurriculumManifest.objects.filter(
        stable_id=definition["stable_id"], manifest_version=definition["manifest_version"]
    ).first()
    if existing:
        if existing.canonical_sha256 != calculated_checksum:
            raise ValidationError("Existing subject manifest differs from immutable input.")
        return existing, False

    subject_leaves = {
        item.stable_id: item
        for item in scope.items.filter(
            is_leaf=True,
            perimeter="TESTABLE",
            subject_group=definition["subject_id"],
        ).select_related("parent__parent")
    }
    declared_leaf_ids = [entry["scope_item_id"] for entry in payload.get("leaves", [])]
    if len(declared_leaf_ids) != len(set(declared_leaf_ids)):
        raise ValidationError("Subject plan contains duplicate official leaves.")
    if set(declared_leaf_ids) != set(subject_leaves):
        raise ValidationError(
            {
                "official_leaf_mismatch": {
                    "missing": sorted(set(subject_leaves) - set(declared_leaf_ids)),
                    "excess": sorted(set(declared_leaf_ids) - set(subject_leaves)),
                }
            }
        )

    policy_entry = payload["coverage_policy"]
    if policy_entry.get("certification_gate_version") != SUBJECT_CERTIFICATION_GATE:
        raise ValidationError("Unknown subject certification gate version.")
    policy_supersedes = None
    if policy_entry.get("supersedes"):
        policy_supersedes = SubjectCoveragePolicy.objects.get(
            stable_id=policy_entry["supersedes"]["stable_id"],
            policy_version=policy_entry["supersedes"]["policy_version"],
        )
    policy = SubjectCoveragePolicy.objects.create(
        stable_id=policy_entry["stable_id"],
        policy_version=policy_entry["policy_version"],
        official_scope_version=scope,
        administration_start=_date(policy_entry["administration_start"]),
        administration_end=_date(policy_entry["administration_end"]),
        requires_primary_authority=policy_entry.get("requires_primary_authority", True),
        requires_human_review=policy_entry.get("requires_human_review", True),
        certification_gate_version=policy_entry["certification_gate_version"],
        canonical_sha256=_entry_sha256(policy_entry),
        source_class=definition["source_class"],
        supersedes=policy_supersedes,
    )
    manifest_supersedes = None
    if definition.get("supersedes"):
        manifest_supersedes = SubjectCurriculumManifest.objects.get(
            stable_id=definition["supersedes"]["stable_id"],
            manifest_version=definition["supersedes"]["manifest_version"],
        )
    manifest = SubjectCurriculumManifest.objects.create(
        stable_id=definition["stable_id"],
        manifest_version=definition["manifest_version"],
        subject_id=definition["subject_id"],
        subject_label=definition["subject_label"],
        official_scope_version=scope,
        coverage_policy=policy,
        canonical_sha256=calculated_checksum,
        source_class=definition["source_class"],
        supersedes=manifest_supersedes,
    )

    leaf_models = {}
    requirement_models = {}
    for leaf_entry in payload["leaves"]:
        scope_item = subject_leaves[leaf_entry["scope_item_id"]]
        expected_path = _hierarchy_path(scope_item)
        if leaf_entry["official_label"] != scope_item.official_label:
            raise ValidationError(f"Official label changed for {scope_item.stable_id}.")
        if leaf_entry["source_locator"] != scope_item.source_locator:
            raise ValidationError(f"Official source locator changed for {scope_item.stable_id}.")
        if leaf_entry["hierarchy_path"] != expected_path:
            raise ValidationError(f"Official hierarchy changed for {scope_item.stable_id}.")
        if leaf_entry["treatment"] != scope_item.knowledge_treatment:
            raise ValidationError(f"Official treatment changed for {scope_item.stable_id}.")
        leaf_model = SubjectManifestLeaf.objects.create(
            manifest=manifest,
            scope_item=scope_item,
            hierarchy_path=leaf_entry["hierarchy_path"],
            treatment=leaf_entry["treatment"],
            coverage_status=leaf_entry["coverage_status"],
            review_required=leaf_entry.get("review_required", True),
            canonical_sha256=_entry_sha256(leaf_entry),
        )
        leaf_models[scope_item.stable_id] = leaf_model
        requirements = leaf_entry.get("requirements", [])
        if not requirements:
            raise ValidationError(
                f"Official leaf {scope_item.stable_id} has no coverage requirements."
            )
        for requirement_entry in requirements:
            requirement_id = requirement_entry["stable_id"]
            if requirement_id in requirement_models:
                raise ValidationError(f"Duplicate coverage requirement: {requirement_id}")
            slots = requirement_entry.get("slots", [])
            if not slots:
                raise ValidationError(f"Coverage requirement {requirement_id} has no slots.")
            requirement = ScopeCoverageRequirement.objects.create(
                manifest_leaf=leaf_model,
                stable_id=requirement_id,
                doctrinal_subarea=requirement_entry["doctrinal_subarea"],
                requirement_type=requirement_entry["requirement_type"],
                treatment_requirement=requirement_entry["treatment_requirement"],
                review_required=requirement_entry.get("review_required", True),
                canonical_sha256=_entry_sha256(
                    {key: value for key, value in requirement_entry.items() if key != "slots"}
                ),
            )
            requirement_models[requirement_id] = requirement
            slot_entries = {entry["stable_id"]: entry for entry in slots}
            if len(slot_entries) != len(slots):
                raise ValidationError(f"Duplicate requirement slot in {requirement_id}.")
            slot_ids = set()
            for slot_entry in slots:
                if slot_entry["stable_id"] in slot_ids:
                    raise ValidationError(f"Duplicate requirement slot: {slot_entry['stable_id']}")
                slot_ids.add(slot_entry["stable_id"])
                for expectation in slot_entry.get("relationship_expectations", []):
                    source_slot = slot_entries.get(expectation.get("source_slot_id"))
                    relationship_kind = expectation.get("relationship_kind")
                    if source_slot is None or source_slot is slot_entry:
                        raise ValidationError(
                            f"Relationship expectation for {slot_entry['stable_id']} has an "
                            "unknown or self source slot."
                        )
                    if (
                        RELATIONSHIP_TARGET_KINDS.get(relationship_kind)
                        != slot_entry["obligation_kind"]
                    ):
                        raise ValidationError(
                            f"Relationship expectation for {slot_entry['stable_id']} has an "
                            "invalid target kind."
                        )
                CoverageRequirementSlot.objects.create(
                    requirement=requirement,
                    stable_id=slot_entry["stable_id"],
                    obligation_kind=slot_entry["obligation_kind"],
                    minimum_count=slot_entry.get("minimum_count", 1),
                    relationship_expectations=slot_entry.get("relationship_expectations", []),
                    canonical_sha256=_entry_sha256(slot_entry),
                )

    authority_models = {}
    for authority_entry in payload.get("authority_plans", []):
        stable_id = authority_entry["stable_id"]
        if stable_id in authority_models:
            raise ValidationError(f"Duplicate authority plan: {stable_id}")
        acquired = None
        acquired_identity = authority_entry.get("acquired_authority")
        if acquired_identity:
            acquired = AuthoritySource.objects.get(
                stable_id=acquired_identity["stable_id"],
                source_version=acquired_identity["source_version"],
            )
        authority = SubjectAuthorityPlan.objects.create(
            manifest=manifest,
            stable_id=stable_id,
            source_family=authority_entry["source_family"],
            authority_level=authority_entry["authority_level"],
            planned_title=authority_entry["planned_title"],
            canonical_source_uri=authority_entry.get("canonical_source_uri", ""),
            version_requirement=authority_entry["version_requirement"],
            freshness_requirement=authority_entry["freshness_requirement"],
            drift_action=authority_entry["drift_action"],
            case_authority_required=authority_entry.get("case_authority_required", False),
            acquisition_status=authority_entry.get("acquisition_status", "PLANNED"),
            acquired_authority=acquired,
            canonical_sha256=_entry_sha256(
                {key: value for key, value in authority_entry.items() if key != "case_requirements"}
            ),
        )
        authority_models[stable_id] = authority
        for case_entry in authority_entry.get("case_requirements", []):
            CaseAuthorityRequirement.objects.create(
                authority_plan=authority,
                stable_id=case_entry["stable_id"],
                proposition_type=case_entry["proposition_type"],
                required_court=case_entry.get(
                    "required_court", "Supreme Court of the United States"
                ),
                exact_case_identity_required=case_entry.get("exact_case_identity_required", True),
                decision_date_required=case_entry.get("decision_date_required", True),
                reliable_source_uri_required=case_entry.get("reliable_source_uri_required", True),
                proposition_locator_required=case_entry.get("proposition_locator_required", True),
                authority_status_required=case_entry.get("authority_status_required", True),
                later_treatment_review_required=case_entry.get(
                    "later_treatment_review_required", True
                ),
                canonical_sha256=_entry_sha256(case_entry),
            )

    mapped_requirements = set()
    for mapping_entry in payload.get("requirement_authority_mappings", []):
        requirement = requirement_models.get(mapping_entry["requirement_id"])
        authority = authority_models.get(mapping_entry["authority_plan_id"])
        if requirement is None or authority is None:
            raise ValidationError("Authority mapping references an unknown requirement or plan.")
        RequirementAuthorityPlan.objects.create(
            requirement=requirement,
            authority_plan=authority,
            role=mapping_entry["role"],
            proposition_types=mapping_entry["proposition_types"],
            canonical_sha256=_entry_sha256(mapping_entry),
        )
        if mapping_entry["role"] in ("REQUIRED", "CONDITIONAL"):
            mapped_requirements.add(requirement.stable_id)
    unmapped_requirements = sorted(set(requirement_models) - mapped_requirements)
    if unmapped_requirements:
        raise ValidationError({"requirements_without_primary_authority": unmapped_requirements})

    for subset_entry in payload.get("certified_subsets", []):
        snapshot = CoverageReleaseSnapshot.objects.select_related("compile_version").get(
            pk=subset_entry["snapshot_id"]
        )
        if snapshot.certification_sha256 != subset_entry["certification_sha256"]:
            raise ValidationError("Certified subset checksum does not match immutable snapshot.")
        if snapshot.compile_version.canonical_sha256 != subset_entry["compile_sha256"]:
            raise ValidationError("Certified subset compile checksum does not match.")
        if snapshot.compile_version.version_identifier != subset_entry["compile_version"]:
            raise ValidationError("Certified subset compile identity does not match.")
        if snapshot.coverage_class != subset_entry["coverage_class"]:
            raise ValidationError("Certified subset coverage class does not match.")
        if snapshot.national_complete != subset_entry["national_complete"]:
            raise ValidationError("Certified subset national-completeness truth does not match.")
        SubjectCertifiedSubset.objects.create(
            manifest_leaf=leaf_models[subset_entry["scope_item_id"]],
            coverage_snapshot=snapshot,
            contribution_class=subset_entry["contribution_class"],
            canonical_sha256=_entry_sha256(subset_entry),
        )

    return manifest, True


def subject_coverage_report(manifest):
    leaves = list(
        manifest.manifest_leaves.select_related("scope_item").prefetch_related(
            "coverage_requirements__slots__satisfactions",
            "certified_subsets__coverage_snapshot__compile_version",
        )
    )
    leaf_results = []
    requirement_count = 0
    slot_count = 0
    certified_slot_count = 0
    for leaf in leaves:
        requirements = list(leaf.coverage_requirements.all())
        requirement_count += len(requirements)
        required_slots = []
        satisfied_slots = []
        for requirement in requirements:
            slots = list(requirement.slots.all())
            slots_by_id = {slot.stable_id: slot for slot in slots}
            for slot in slots:
                required_slots.append(slot)
                certified_satisfactions = list(
                    slot.satisfactions.filter(status="CERTIFIED").select_related("obligation")
                )
                relationships_satisfied = True
                for expectation in slot.relationship_expectations:
                    source_slot = slots_by_id[expectation["source_slot_id"]]
                    source_obligation_ids = source_slot.satisfactions.filter(
                        status="CERTIFIED"
                    ).values_list("obligation_id", flat=True)
                    target_obligation_ids = [
                        satisfaction.obligation_id for satisfaction in certified_satisfactions
                    ]
                    if not source_slot.satisfactions.filter(status="CERTIFIED").exists() or not (
                        source_slot.satisfactions.filter(
                            obligation__outgoing_relationships__source_id__in=source_obligation_ids,
                            obligation__outgoing_relationships__target_id__in=target_obligation_ids,
                            obligation__outgoing_relationships__kind=expectation[
                                "relationship_kind"
                            ],
                        ).exists()
                    ):
                        relationships_satisfied = False
                        break
                if len(certified_satisfactions) >= slot.minimum_count and relationships_satisfied:
                    satisfied_slots.append(slot)
        slot_count += len(required_slots)
        certified_slot_count += len(satisfied_slots)
        subsets = list(leaf.certified_subsets.all())
        structurally_complete = bool(required_slots) and len(satisfied_slots) == len(required_slots)
        leaf_results.append(
            {
                "scope_item_id": leaf.scope_item.stable_id,
                "official_label": leaf.scope_item.official_label,
                "treatment": leaf.treatment,
                "coverage_status": leaf.coverage_status,
                "requirement_count": len(requirements),
                "required_slot_count": len(required_slots),
                "certified_slot_count": len(satisfied_slots),
                "structurally_complete": structurally_complete,
                "certified_subsets": [
                    {
                        "snapshot_id": str(subset.coverage_snapshot_id),
                        "compile_version": (
                            subset.coverage_snapshot.compile_version.version_identifier
                        ),
                        "coverage_class": subset.coverage_snapshot.coverage_class,
                        "contribution_class": subset.contribution_class,
                    }
                    for subset in subsets
                ],
            }
        )
    authority_counts = Counter(
        manifest.authority_plans.values_list("acquisition_status", flat=True)
    )
    human_review = getattr(manifest, "human_review", None)
    human_review_status = human_review.resolution if human_review else "PENDING"
    all_leaves_structurally_complete = all(
        result["structurally_complete"] for result in leaf_results
    )
    all_authority_acquired = not manifest.authority_plans.exclude(
        acquisition_status="ACQUIRED"
    ).exists()
    all_leaves_certified = all(
        result["coverage_status"] == SubjectManifestLeaf.CoverageStatus.LEAF_CERTIFIED
        for result in leaf_results
    )
    subject_complete = bool(
        leaf_results
        and all_leaves_structurally_complete
        and all_authority_acquired
        and all_leaves_certified
        and human_review_status == SubjectPlanHumanReview.Resolution.APPROVE
    )
    # M2.2c contains no explicit subject-certification domain operation. Percentage arithmetic
    # therefore cannot turn a structurally eligible plan into certified subject truth.
    subject_certified = False
    return {
        "schema": "BARCLIMB_SUBJECT_COVERAGE_REPORT_V1",
        "official_scope_version": manifest.official_scope_version.version_identifier,
        "official_scope_sha256": manifest.official_scope_version.normalized_sha256,
        "subject_id": manifest.subject_id,
        "subject_label": manifest.subject_label,
        "subject_manifest": f"{manifest.stable_id}@{manifest.manifest_version}",
        "subject_manifest_sha256": manifest.canonical_sha256,
        "coverage_policy": (
            f"{manifest.coverage_policy.stable_id}@{manifest.coverage_policy.policy_version}"
        ),
        "coverage_policy_sha256": manifest.coverage_policy.canonical_sha256,
        "official_leaf_count": len(leaves),
        "coverage_requirement_count": requirement_count,
        "required_slot_count": slot_count,
        "certified_slot_count": certified_slot_count,
        "authority_plan_count": manifest.authority_plans.count(),
        "authority_status_counts": dict(sorted(authority_counts.items())),
        "human_review_status": human_review_status,
        "leaf_results": leaf_results,
        "uncovered_leaf_ids": [
            result["scope_item_id"]
            for result in leaf_results
            if result["coverage_status"] != SubjectManifestLeaf.CoverageStatus.LEAF_CERTIFIED
        ],
        "unresolved_authority_gap_count": manifest.authority_plans.exclude(
            acquisition_status="ACQUIRED"
        ).count(),
        "unresolved_candidate_slot_count": slot_count - certified_slot_count,
        "unresolved_human_review_count": int(human_review_status != "APPROVE"),
        "structurally_eligible": subject_complete,
        "subject_certified": subject_certified,
        "subject_complete": False,
        "national_complete": False,
        "certification_note": (
            "SUBJECT_CERTIFIED requires a future explicit certification operation after every "
            "structural, authority, reconciliation, jurisdiction, and human-review gate passes."
        ),
    }


def assert_subject_certification_ready(manifest):
    report = subject_coverage_report(manifest)
    blockers = {
        "uncovered_leaf_ids": report["uncovered_leaf_ids"],
        "unresolved_authority_gap_count": report["unresolved_authority_gap_count"],
        "unresolved_candidate_slot_count": report["unresolved_candidate_slot_count"],
        "unresolved_human_review_count": report["unresolved_human_review_count"],
    }
    if any(blockers.values()):
        raise ValidationError(f"subject_certification_blocked: {blockers}")
    raise ValidationError(
        "Structural eligibility cannot itself certify a subject; explicit certification "
        "is required."
    )


@transaction.atomic
def record_subject_plan_review(
    manifest_id,
    *,
    reviewer,
    reviewer_name,
    reviewer_role_qualification,
    resolution,
    rationale,
    attestation,
    review_packet_sha256,
    reviewed_at=None,
    operator_manifest=False,
):
    if reviewer is None and not operator_manifest:
        raise PermissionDenied("External subject-plan review requires the operator workflow.")
    if reviewer is not None and not reviewer.is_staff:
        raise PermissionDenied("Subject-plan review requires staff authority.")
    manifest = SubjectCurriculumManifest.objects.select_for_update().get(pk=manifest_id)
    existing = SubjectPlanHumanReview.objects.filter(manifest=manifest).first()
    if existing:
        expected = {
            "reviewer_id": getattr(reviewer, "pk", None),
            "reviewer_name": reviewer_name,
            "reviewer_role_qualification": reviewer_role_qualification,
            "resolution": resolution,
            "rationale": rationale,
            "attestation": attestation,
            "review_packet_sha256": review_packet_sha256,
            "reviewed_at": reviewed_at or existing.reviewed_at,
        }
        if any(getattr(existing, field) != value for field, value in expected.items()):
            raise ValidationError("Existing subject-plan review differs from immutable input.")
        return existing, False
    review = SubjectPlanHumanReview.objects.create(
        manifest=manifest,
        reviewer=reviewer,
        reviewer_name=reviewer_name,
        reviewer_role_qualification=reviewer_role_qualification,
        resolution=resolution,
        rationale=rationale,
        attestation=attestation,
        review_packet_sha256=review_packet_sha256,
        reviewed_at=reviewed_at or timezone.now(),
    )
    return review, True
