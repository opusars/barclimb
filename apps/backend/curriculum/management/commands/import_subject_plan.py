import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from curriculum.subject_planning import import_subject_plan, subject_coverage_report


class Command(BaseCommand):
    help = "Import one immutable subject coverage plan after its scope and certified subsets exist."

    def add_arguments(self, parser):
        parser.add_argument("manifest", type=Path)

    def handle(self, *args, **options):
        try:
            payload = json.loads(options["manifest"].read_text())
            manifest, created = import_subject_plan(payload)
        except Exception as error:
            raise CommandError(str(error)) from error
        report = subject_coverage_report(manifest)
        report["created"] = created
        self.stdout.write(json.dumps(report, sort_keys=True, indent=2))
