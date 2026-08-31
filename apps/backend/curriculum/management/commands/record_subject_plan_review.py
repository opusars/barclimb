import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from curriculum.models import SubjectCurriculumManifest
from curriculum.subject_planning import record_subject_plan_review


class Command(BaseCommand):
    help = "Record one exact external-human review of an immutable subject coverage plan."

    def add_arguments(self, parser):
        parser.add_argument("review_manifest", type=Path)
        parser.add_argument("--packet", type=Path, required=True)

    def handle(self, *args, **options):
        path = options["review_manifest"]
        try:
            raw = path.read_bytes()
            payload = json.loads(raw)
            packet_sha256 = hashlib.sha256(options["packet"].read_bytes()).hexdigest()
            if packet_sha256 != payload["review_packet_sha256"]:
                raise ValueError("Review packet does not match review_packet_sha256.")
            manifest = SubjectCurriculumManifest.objects.get(
                stable_id=payload["subject_manifest"]["stable_id"],
                manifest_version=payload["subject_manifest"]["manifest_version"],
            )
            if payload.get("schema") == "BARCLIMB_SUBJECT_PLAN_HUMAN_REVIEW_V1":
                if payload["subject_manifest"].get("canonical_sha256") != manifest.canonical_sha256:
                    raise ValueError(
                        "Review subject-manifest checksum does not match immutable truth."
                    )
                policy = payload.get("coverage_policy", {})
                if policy != {
                    "stable_id": manifest.coverage_policy.stable_id,
                    "policy_version": manifest.coverage_policy.policy_version,
                    "canonical_sha256": manifest.coverage_policy.canonical_sha256,
                }:
                    raise ValueError(
                        "Review coverage-policy identity does not match immutable truth."
                    )
                if (
                    payload.get("certification_gate_version")
                    != manifest.coverage_policy.certification_gate_version
                ):
                    raise ValueError(
                        "Review certification-gate identity does not match immutable truth."
                    )
                if payload.get("official_scope") != {
                    "version_identifier": manifest.official_scope_version.version_identifier,
                    "normalized_sha256": manifest.official_scope_version.normalized_sha256,
                }:
                    raise ValueError(
                        "Review official-scope identity does not match immutable truth."
                    )
                if not re.fullmatch(r"[0-9a-f]{40}", payload.get("reviewed_git_sha", "")):
                    raise ValueError("Review requires an exact lowercase Git SHA.")
            review, created = record_subject_plan_review(
                manifest.pk,
                reviewer=None,
                reviewer_name=payload["reviewer_name"],
                reviewer_role_qualification=payload["reviewer_role_qualification"],
                resolution=payload["resolution"],
                rationale=payload["rationale"],
                attestation=payload["attestation"],
                review_packet_sha256=payload["review_packet_sha256"],
                reviewed_at=(
                    datetime.fromisoformat(payload["reviewed_at"].replace("Z", "+00:00"))
                    if payload.get("reviewed_at")
                    else None
                ),
                operator_manifest=True,
            )
        except Exception as error:
            raise CommandError(str(error)) from error
        self.stdout.write(
            json.dumps(
                {
                    "created": created,
                    "review_id": review.pk,
                    "review_manifest_sha256": hashlib.sha256(raw).hexdigest(),
                    "resolution": review.resolution,
                },
                sort_keys=True,
            )
        )
