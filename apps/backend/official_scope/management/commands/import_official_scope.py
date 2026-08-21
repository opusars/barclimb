import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from official_scope.importer import import_manifest


class Command(BaseCommand):
    help = "Register, normalize, validate, and optionally activate a controlled scope manifest."

    def add_arguments(self, parser):
        parser.add_argument("input", type=Path)
        parser.add_argument("--activate", action="store_true")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        try:
            payload = json.loads(options["input"].read_text())
            with transaction.atomic():
                result = import_manifest(payload, activate=options["activate"])
                if options["dry_run"]:
                    transaction.set_rollback(True)
        except Exception as error:
            raise CommandError(str(error)) from error
        result["dry_run"] = options["dry_run"]
        self.stdout.write(json.dumps(result, sort_keys=True))
