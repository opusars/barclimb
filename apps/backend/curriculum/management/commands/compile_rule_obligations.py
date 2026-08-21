import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from curriculum.services import (
    certify_curriculum,
    compile_manifest,
    compile_result,
    reconcile_curriculum,
)


class Command(BaseCommand):
    help = "Deterministically compile/reconcile and optionally certify Rule Obligations."

    def add_arguments(self, parser):
        parser.add_argument("input", type=Path)
        parser.add_argument("--reconcile", action="store_true")
        parser.add_argument("--certify", action="store_true")
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument(
            "--authority",
            action="append",
            default=[],
            metavar="STABLE_ID=PATH",
            help="Provide acquired authority bytes without embedding or committing them.",
        )

    def handle(self, *args, **options):
        try:
            payload = json.loads(options["input"].read_text())
            authority_contents = {}
            for value in options["authority"]:
                stable_id, separator, path = value.partition("=")
                if not separator or not stable_id or not path:
                    raise CommandError("--authority must be STABLE_ID=PATH")
                authority_contents[stable_id] = Path(path).read_bytes()
            with transaction.atomic():
                compile_version, created = compile_manifest(
                    payload, authority_contents=authority_contents
                )
                initial_status = compile_version.status
                if options["reconcile"] or options["certify"]:
                    compile_version, _ = reconcile_curriculum(compile_version.pk)
                if options["certify"]:
                    certify_curriculum(compile_version.pk)
                    compile_version.refresh_from_db()
                result = compile_result(compile_version)
                result.update(
                    {
                        "created": created,
                        "dry_run": options["dry_run"],
                        "certified": compile_version.status == "CERTIFIED",
                        "state_changed": created or compile_version.status != initial_status,
                    }
                )
                if options["dry_run"]:
                    transaction.set_rollback(True)
        except Exception as error:
            raise CommandError(str(error)) from error
        self.stdout.write(json.dumps(result, sort_keys=True))
