import hashlib
import json
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_datetime

from curriculum.models import CurriculumCompileVersion
from curriculum.services import certify_curriculum
from official_scope.services import canonical_sha256


class Command(BaseCommand):
    help = "Certify one exact reviewed topic through the canonical coverage snapshot workflow."

    def add_arguments(self, parser):
        parser.add_argument("input", type=Path)
        parser.add_argument("--subject-review-record", type=Path, required=True)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        try:
            evidence = json.loads(options["input"].read_text())
            review_record_bytes = options["subject_review_record"].read_bytes()
            json.loads(review_record_bytes)
            expected_review_sha = evidence.get("subject_plan_review_manifest_sha256")
            actual_review_sha = hashlib.sha256(review_record_bytes).hexdigest()
            if expected_review_sha != actual_review_sha:
                raise ValidationError(
                    {
                        "subject_plan_review_manifest_sha256": (
                            f"Expected {expected_review_sha}; received {actual_review_sha}"
                        )
                    }
                )
            certified_at = parse_datetime(evidence.get("certified_at", ""))
            if certified_at is None or certified_at.tzinfo is None:
                raise ValidationError("certified_at must be an explicit timezone-aware timestamp.")
            compile_version = CurriculumCompileVersion.objects.get(
                version_identifier=evidence["compile_version"]
            )
            with transaction.atomic():
                snapshot = certify_curriculum(
                    compile_version.pk,
                    topic_certification=evidence,
                    certified_at=certified_at,
                )
                if options["dry_run"]:
                    transaction.set_rollback(True)
        except Exception as error:
            raise CommandError(str(error)) from error
        result = {
            "compile_version": compile_version.version_identifier,
            "compile_sha256": compile_version.canonical_sha256,
            "topic_id": evidence["topic_id"],
            "requirement_id": evidence["requirement_id"],
            "snapshot_id": str(snapshot.pk),
            "certification_sha256": snapshot.certification_sha256,
            "topic_certification_input_sha256": canonical_sha256(evidence),
            "slot_count": len(evidence["slots"]),
            "topic_certified": True,
            "subject_complete": False,
            "subject_certified": False,
            "national_complete": snapshot.national_complete,
            "certified_at": snapshot.certified_at.isoformat(),
            "dry_run": options["dry_run"],
        }
        self.stdout.write(json.dumps(result, sort_keys=True))
