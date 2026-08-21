import base64
from datetime import date, datetime

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import (
    OfficialScopeItem,
    OfficialScopeSource,
    OfficialScopeVersion,
    OfficialSourceArtifact,
)
from .services import (
    register_artifact,
    validate_and_activate,
    validate_scope,
    validate_scope_version,
)


def _date(value):
    return date.fromisoformat(value) if value else None


def _datetime(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


@transaction.atomic
def import_manifest(payload, *, activate=False, allow_test_fixture=False):
    if payload.get("schema") != "BARCLIMB_OFFICIAL_SCOPE_IMPORT_V1":
        raise ValidationError("Unsupported official-scope import schema.")
    artifact_entries = payload.get("artifacts", [])
    artifact_ids = [entry.get("stable_id") for entry in artifact_entries]
    if len(artifact_ids) != len(set(artifact_ids)):
        raise ValidationError("Duplicate artifact stable_id in import manifest.")
    artifact_map = {}
    created_artifacts = 0
    for entry in artifact_entries:
        try:
            content = base64.b64decode(entry["content_base64"], validate=True)
        except Exception as error:
            raise ValidationError("Artifact content_base64 is invalid.") from error
        supersedes = None
        predecessor = entry.get("supersedes")
        if predecessor:
            supersedes = OfficialSourceArtifact.objects.filter(
                stable_id=predecessor["stable_id"],
                source_version=predecessor["source_version"],
            ).first()
            if supersedes is None:
                raise ValidationError("Artifact supersedes reference does not exist.")
        artifact, created = register_artifact(
            content=content,
            stable_id=entry["stable_id"],
            source_authority=entry["source_authority"],
            artifact_type=entry["artifact_type"],
            official_title=entry["official_title"],
            source_uri=entry.get("source_uri", ""),
            publication_date=_date(entry.get("publication_date")),
            effective_date=_date(entry.get("effective_date")),
            retrieved_at=_datetime(entry.get("retrieved_at")),
            source_version=entry["source_version"],
            status=entry.get("status", "PUBLISHED"),
            supersedes=supersedes,
            source_class=entry.get("source_class", "OFFICIAL"),
            provenance_notes=entry.get("provenance_notes", ""),
        )
        artifact_map[entry["stable_id"]] = artifact
        created_artifacts += created

    definition = payload["scope"]
    scope, scope_created = OfficialScopeVersion.objects.get_or_create(
        version_identifier=definition["version_identifier"],
        defaults={
            "exam_program": definition.get("exam_program", "NEXTGEN_UBE"),
            "exam_component": definition.get("exam_component", "NEXTGEN_CORE"),
            "is_national": definition.get("is_national", True),
            "jurisdiction": definition.get("jurisdiction", ""),
            "is_test_fixture": definition.get("is_test_fixture", False),
        },
    )
    expected = (
        definition.get("exam_program", "NEXTGEN_UBE"),
        definition.get("exam_component", "NEXTGEN_CORE"),
        definition.get("is_national", True),
        definition.get("jurisdiction", ""),
        definition.get("is_test_fixture", False),
    )
    actual = (
        scope.exam_program,
        scope.exam_component,
        scope.is_national,
        scope.jurisdiction,
        scope.is_test_fixture,
    )
    if actual != expected:
        raise ValidationError("Scope identity exists with different immutable metadata.")
    if not scope_created and scope.status != OfficialScopeVersion.Status.DRAFT:
        report, checksum = validate_scope(scope)
        return _result(scope, report, checksum, created_artifacts, False, False)

    for ordering, source in enumerate(definition.get("sources", [])):
        artifact = artifact_map.get(source["artifact_id"])
        if artifact is None:
            raise ValidationError(f"Unknown artifact: {source['artifact_id']}")
        link, link_created = OfficialScopeSource.objects.get_or_create(
            scope_version=scope,
            artifact=artifact,
            defaults={"role": source["role"], "ordering": ordering},
        )
        if not link_created and (link.role != source["role"] or link.ordering != ordering):
            raise ValidationError("Existing source mapping differs from deterministic import.")

    item_entries = definition.get("items", [])
    item_ids = [item.get("stable_id") for item in item_entries]
    if len(item_ids) != len(set(item_ids)):
        raise ValidationError("Duplicate scope-item stable_id in import manifest.")
    pending = {item["stable_id"]: item for item in item_entries}
    created_items = {}
    while pending:
        progressed = False
        for stable_id, item in list(pending.items()):
            parent_id = item.get("parent_id")
            if parent_id and parent_id not in created_items:
                continue
            source = artifact_map.get(item["source_artifact_id"])
            if source is None:
                raise ValidationError(f"Unknown item source: {item['source_artifact_id']}")
            created, was_created = OfficialScopeItem.objects.get_or_create(
                scope_version=scope,
                stable_id=stable_id,
                defaults={
                    "parent": created_items.get(parent_id),
                    "official_label": item["official_label"],
                    "official_text": item.get("official_text", ""),
                    "ordering": item.get("ordering", 0),
                    "perimeter": item.get("perimeter", "UNSPECIFIED"),
                    "subject_group": item.get("subject_group", ""),
                    "is_leaf": item.get("is_leaf", False),
                    "source_artifact": source,
                    "source_locator": item["source_locator"],
                    "treatment_metadata": item.get("treatment_metadata", {}),
                },
            )
            if not was_created:
                comparable = {
                    "parent_id": created_items.get(parent_id).id if parent_id else None,
                    "official_label": item["official_label"],
                    "official_text": item.get("official_text", ""),
                    "ordering": item.get("ordering", 0),
                    "perimeter": item.get("perimeter", "UNSPECIFIED"),
                    "subject_group": item.get("subject_group", ""),
                    "is_leaf": item.get("is_leaf", False),
                    "source_artifact_id": source.id,
                    "source_locator": item["source_locator"],
                    "treatment_metadata": item.get("treatment_metadata", {}),
                }
                if any(getattr(created, key) != value for key, value in comparable.items()):
                    raise ValidationError(f"Scope item {stable_id} changed during re-import.")
            created_items[stable_id] = created
            del pending[stable_id]
            progressed = True
        if not progressed:
            raise ValidationError({"items": "Missing or cyclic parent reference."})

    scope, report = validate_scope_version(scope.pk)
    checksum = scope.normalized_sha256
    activated = False
    if activate:
        scope, report = validate_and_activate(scope.pk, allow_test_fixture=allow_test_fixture)
        checksum = scope.normalized_sha256
        activated = True
    return _result(scope, report, checksum, created_artifacts, scope_created, activated)


def _result(scope, report, checksum, artifacts_created, scope_created, activated):
    return {
        "artifacts_created": artifacts_created,
        "artifact_count": scope.source_artifacts.count(),
        "scope_created": scope_created,
        "scope_version": scope.version_identifier,
        "scope_sha256": checksum,
        "item_count": scope.items.count(),
        "leaf_count": scope.items.filter(is_leaf=True).count(),
        "validation": report.as_dict(),
        "activated": activated,
    }
