import hashlib
import json
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime

from curriculum.models import (
    AuthoritySource,
    CoverageReleaseSnapshot,
    CurriculumCompileVersion,
    ObligationHumanReview,
    ObligationRelationship,
)
from curriculum.services import (
    certify_curriculum,
    reconcile_curriculum,
    record_obligation_review,
)
from official_scope.services import canonical_sha256


class Command(BaseCommand):
    help = "Apply a controlled named-human review manifest and optionally certify its compile."

    def add_arguments(self, parser):
        parser.add_argument("input", type=Path)
        parser.add_argument("--packet", type=Path)
        parser.add_argument("--certify", action="store_true")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        try:
            payload = json.loads(options["input"].read_text())
            with transaction.atomic():
                result = self._apply(
                    payload,
                    packet_path=options["packet"],
                    certify=options["certify"],
                )
                if options["dry_run"]:
                    transaction.set_rollback(True)
        except Exception as error:
            raise CommandError(str(error)) from error
        result["dry_run"] = options["dry_run"]
        self.stdout.write(json.dumps(result, sort_keys=True))

    def _apply(self, payload, *, packet_path, certify):
        schema = payload.get("schema")
        if schema not in {
            "BARCLIMB_OBLIGATION_REVIEW_V1",
            "BARCLIMB_OBLIGATION_REVIEW_V2",
        }:
            raise ValidationError("Unsupported obligation review schema.")
        manifest_sha256 = canonical_sha256(payload)
        compile_version = CurriculumCompileVersion.objects.select_for_update().get(
            version_identifier=payload["compile_version"]
        )
        scope = compile_version.official_scope_version
        checks = {
            "compile_checksum": compile_version.canonical_sha256,
            "scope_version": scope.version_identifier,
            "scope_checksum": scope.normalized_sha256,
            "coverage_class": compile_version.coverage_class,
        }
        for field, actual in checks.items():
            if payload.get(field) != actual:
                raise ValidationError({field: f"Expected {actual}; received {payload.get(field)}"})
        if compile_version.national_complete or payload.get("national_complete") is not False:
            raise ValidationError(
                "The reviewed pilot must remain explicitly non-national-complete."
            )

        if schema == "BARCLIMB_OBLIGATION_REVIEW_V2":
            self._validate_exact_review_bindings(payload, compile_version, packet_path)

        authorities = payload.get("authorities") or [payload["authority"]]
        for authority in authorities:
            if not AuthoritySource.objects.filter(
                stable_id=authority["stable_id"],
                source_version=authority["source_version"],
                content_sha256=authority["sha256"],
                authority_class=AuthoritySource.AuthorityClass.SUBSTANTIVE_PRIMARY,
                source_class=AuthoritySource.SourceClass.PRODUCTION,
            ).exists():
                raise ValidationError(
                    "The reviewed primary-authority provenance is not registered."
                )

        obligations = {
            obligation.stable_id: obligation
            for obligation in compile_version.obligations.filter(compiler_status="INCLUDED")
        }
        decisions = payload.get("decisions", [])
        decision_ids = [decision.get("obligation") for decision in decisions]
        if len(decision_ids) != len(set(decision_ids)) or set(decision_ids) != set(obligations):
            raise ValidationError(
                "Review decisions must exactly cover every included obligation once."
            )

        reviewer = payload["reviewer"]
        reviewed_at = parse_datetime(payload["reviewed_at"])
        if reviewed_at is None or reviewed_at.tzinfo is None:
            raise ValidationError("reviewed_at must be an explicit timezone-aware timestamp.")
        created_count = 0
        review_records = []
        for decision in decisions:
            if decision.get("resolution") not in ObligationHumanReview.Resolution.values:
                raise ValidationError("Review manifest contains an unsupported resolution.")
            if decision.get("authority_reviewed") is not True:
                raise ValidationError("Every production approval must attest authority review.")
            review, created = record_obligation_review(
                obligations[decision["obligation"]].pk,
                reviewer=None,
                reviewer_name=reviewer["name"],
                reviewer_role_qualification=reviewer["role_qualification"],
                resolution=decision["resolution"],
                rationale=payload["rationale"],
                attestation=payload["attestation"],
                authority_reviewed=True,
                review_manifest_sha256=manifest_sha256,
                reviewed_at=reviewed_at,
                operator_manifest=True,
            )
            created_count += int(created)
            record_payload = {
                "obligation": review.obligation.stable_id,
                "candidate_canonical_sha256": review.obligation.canonical_sha256,
                "reviewer_name": review.reviewer_name,
                "reviewer_role_qualification": review.reviewer_role_qualification,
                "resolution": review.resolution,
                "rationale": review.rationale,
                "attestation": review.attestation,
                "authority_reviewed": review.authority_reviewed,
                "review_manifest_sha256": review.review_manifest_sha256,
                "reviewed_at": review.reviewed_at.isoformat(),
            }
            review_records.append(
                {
                    "obligation": review.obligation.stable_id,
                    "database_id": review.pk,
                    "record_sha256": canonical_sha256(record_payload),
                    "created": created,
                }
            )

        if compile_version.status == CurriculumCompileVersion.Status.CERTIFIED:
            snapshot = compile_version.coverage_snapshot
        else:
            compile_version, report = reconcile_curriculum(compile_version.pk)
            if (
                report["blocking_issue_count"]
                or report["warning_issue_count"]
                or report["national_complete"]
                or report["coverage_class"] != "PILOT_ONLY"
                or (
                    schema == "BARCLIMB_OBLIGATION_REVIEW_V1"
                    and report["leaves_sufficiently_covered"] != report["total_official_leaves"]
                )
            ):
                raise ValidationError("Reviewed pilot failed its bounded certification gates.")
            snapshot = certify_curriculum(compile_version.pk) if certify else None

        reviews = list(
            ObligationHumanReview.objects.filter(obligation__compile_version=compile_version)
            .select_related("obligation")
            .order_by("obligation__stable_id")
        )
        result = {
            "compile_version": compile_version.version_identifier,
            "compile_checksum": compile_version.canonical_sha256,
            "review_manifest_sha256": manifest_sha256,
            "review_count": len(reviews),
            "reviews_created": created_count,
            "reviewed_at": reviewed_at.isoformat(),
            "reviewer_name": reviewer["name"],
            "reviewer_role_qualification": reviewer["role_qualification"],
            "resolutions": {review.obligation.stable_id: review.resolution for review in reviews},
            "review_records": sorted(review_records, key=lambda value: value["obligation"]),
            "certified": snapshot is not None,
        }
        if snapshot:
            result["snapshot"] = {
                "id": str(snapshot.pk),
                "certification_sha256": snapshot.certification_sha256,
                "authority_provenance_sha256": snapshot.authority_provenance_sha256,
                "human_review_sha256": snapshot.human_review_sha256,
                "coverage_class": snapshot.coverage_class,
                "national_complete": snapshot.national_complete,
                "leaf_count": snapshot.leaf_count,
                "covered_leaf_count": snapshot.covered_leaf_count,
                "obligation_count": snapshot.obligation_count,
                "blocking_issue_count": snapshot.blocking_issue_count,
                "warning_issue_count": snapshot.warning_issue_count,
                "certified_at": snapshot.certified_at.isoformat(),
            }
        elif CoverageReleaseSnapshot.objects.filter(compile_version=compile_version).exists():
            raise ValidationError("Unexpected certification snapshot state.")
        return result

    def _validate_exact_review_bindings(self, payload, compile_version, packet_path):
        if payload.get("input_checksum") != compile_version.input_sha256:
            raise ValidationError(
                {
                    "input_checksum": (
                        f"Expected {compile_version.input_sha256}; "
                        f"received {payload.get('input_checksum')}"
                    )
                }
            )
        packet = payload.get("reviewed_packet", {})
        if packet_path is None:
            raise ValidationError("V2 obligation review requires the exact reviewed packet.")
        packet_sha256 = hashlib.sha256(packet_path.read_bytes()).hexdigest()
        if packet.get("sha256") != packet_sha256:
            raise ValidationError(
                {"reviewed_packet": f"Expected {packet.get('sha256')}; received {packet_sha256}"}
            )
        if packet.get("path") and not packet_path.as_posix().endswith(packet["path"]):
            raise ValidationError("Reviewed packet path does not match the bound packet identity.")

        obligations = list(
            compile_version.obligations.filter(compiler_status="INCLUDED")
            .prefetch_related(
                "scope_items",
                "authority_evidence__authority",
            )
            .select_related(
                "candidate_requirement_mapping__slot__requirement",
                "candidate_requirement_mapping__official_topic",
            )
            .order_by("stable_id")
        )
        actual_candidates = []
        for obligation in obligations:
            mapping = obligation.candidate_requirement_mapping
            actual_candidates.append(
                {
                    "stable_id": obligation.stable_id,
                    "kind": obligation.kind,
                    "statement": obligation.statement,
                    "normalized_statement": obligation.normalized_statement,
                    "candidate_canonical_sha256": obligation.canonical_sha256,
                    "scope_item_ids": sorted(
                        obligation.scope_items.values_list("stable_id", flat=True)
                    ),
                    "topic_id": mapping.official_topic.stable_id,
                    "requirement_id": mapping.slot.requirement.stable_id,
                    "slot_id": mapping.slot.stable_id,
                    "inherited_treatment": mapping.inherited_treatment,
                    "mapping_sha256": mapping.canonical_sha256,
                    "authority_evidence": sorted(
                        [
                            {
                                "authority_id": evidence.authority.stable_id,
                                "source_version": evidence.authority.source_version,
                                "source_sha256": evidence.authority.content_sha256,
                                "role": evidence.role,
                                "locator": evidence.locator,
                                "proposition_type": evidence.proposition_type,
                                "proposition_sha256": evidence.proposition_sha256,
                                "supports": evidence.supports,
                            }
                            for evidence in obligation.authority_evidence.all()
                        ],
                        key=lambda value: (
                            value["authority_id"],
                            value["source_version"],
                            value["role"],
                            value["locator"],
                        ),
                    ),
                }
            )
        expected_candidates = sorted(
            payload.get("candidates", []), key=lambda value: value["stable_id"]
        )
        if expected_candidates != actual_candidates:
            raise ValidationError("Reviewed candidate statements or evidence bindings differ.")

        actual_relationships = sorted(
            [
                {
                    "source_id": edge.source.stable_id,
                    "kind": edge.kind,
                    "target_id": edge.target.stable_id,
                    "ordering": edge.ordering,
                }
                for edge in ObligationRelationship.objects.filter(
                    source__compile_version=compile_version
                ).select_related("source", "target")
            ],
            key=lambda value: (
                value["source_id"],
                value["kind"],
                value["target_id"],
                value["ordering"],
            ),
        )
        expected_relationships = sorted(
            payload.get("relationships", []),
            key=lambda value: (
                value["source_id"],
                value["kind"],
                value["target_id"],
                value["ordering"],
            ),
        )
        if expected_relationships != actual_relationships:
            raise ValidationError("Reviewed obligation relationships differ.")
