import hashlib
import json
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
