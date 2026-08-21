import json

from django.core.management.base import BaseCommand, CommandError

from curriculum.models import SubjectCurriculumManifest
from curriculum.subject_planning import subject_coverage_report


class Command(BaseCommand):
    help = "Report every remaining subject-planning, authority, candidate, and review gap."

    def add_arguments(self, parser):
        parser.add_argument("manifest_identity")

    def handle(self, *args, **options):
        identity = options["manifest_identity"]
        try:
            stable_id, manifest_version = identity.rsplit("@", 1)
            manifest = SubjectCurriculumManifest.objects.get(
                stable_id=stable_id, manifest_version=manifest_version
            )
        except (ValueError, SubjectCurriculumManifest.DoesNotExist) as error:
            raise CommandError(
                "Unknown subject manifest identity; use STABLE_ID@VERSION."
            ) from error
        self.stdout.write(json.dumps(subject_coverage_report(manifest), sort_keys=True, indent=2))
