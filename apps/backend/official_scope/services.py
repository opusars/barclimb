import hashlib
import json
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .models import (
    OfficialScopeItem,
    OfficialScopeSource,
    OfficialScopeVersion,
    OfficialSourceArtifact,
)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def canonical_sha256(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256_bytes(payload.encode("utf-8"))


@dataclass(frozen=True)
class ValidationReport:
    errors: tuple[dict, ...]
    warnings: tuple[dict, ...]
    info: tuple[dict, ...]

    @property
    def valid(self):
        return not self.errors

    def as_dict(self):
        return {
            "valid": self.valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "info": list(self.info),
        }


def register_artifact(*, content: bytes, **metadata):
    checksum = sha256_bytes(content)
    identity = {
        "stable_id": metadata["stable_id"],
        "source_version": metadata["source_version"],
    }
    existing = OfficialSourceArtifact.objects.filter(**identity).first()
    if existing:
        immutable = (
            "source_authority",
            "artifact_type",
            "official_title",
            "source_uri",
            "publication_date",
            "effective_date",
            "source_class",
            "status",
        )
        if (
            existing.content_sha256 != checksum
            or any(
                getattr(existing, key) != metadata.get(key, getattr(existing, key))
                for key in immutable
            )
            or existing.supersedes_id != getattr(metadata.get("supersedes"), "pk", None)
        ):
            raise ValidationError(
                "Artifact identity already exists with different bytes or identity metadata."
            )
        return existing, False
    artifact = OfficialSourceArtifact(content_sha256=checksum, **metadata)
    artifact.full_clean()
    artifact.save()
    return artifact, True


def _normalized_scope(scope):
    sources = [
        {
            "stable_id": link.artifact.stable_id,
            "version": link.artifact.source_version,
            "sha256": link.artifact.content_sha256,
            "role": link.role,
            "ordering": link.ordering,
        }
        for link in OfficialScopeSource.objects.filter(scope_version=scope)
        .select_related("artifact")
        .order_by("ordering", "artifact__stable_id")
    ]
    items = [
        {
            "stable_id": item.stable_id,
            "parent": item.parent.stable_id if item.parent_id else None,
            "label": item.official_label,
            "text": item.official_text,
            "ordering": item.ordering,
            "perimeter": item.perimeter,
            "subject_group": item.subject_group,
            "is_leaf": item.is_leaf,
            "source": [item.source_artifact.stable_id, item.source_artifact.source_version],
            "source_locator": item.source_locator,
            "treatment": item.treatment_metadata,
        }
        for item in scope.items.select_related("parent", "source_artifact").order_by("stable_id")
    ]
    return {
        "exam_program": scope.exam_program,
        "exam_component": scope.exam_component,
        "is_national": scope.is_national,
        "sources": sources,
        "items": items,
    }


def validate_scope(scope):
    errors = []
    warnings = []
    info = []
    if (
        scope.exam_program != OfficialScopeVersion.EXAM_PROGRAM
        or scope.exam_component != OfficialScopeVersion.EXAM_COMPONENT
        or not scope.is_national
        or scope.jurisdiction
    ):
        errors.append({"code": "UNSUPPORTED_JURISDICTION", "message": "V1 is national only."})
    source_links = list(
        OfficialScopeSource.objects.filter(scope_version=scope).select_related("artifact")
    )
    if not source_links:
        errors.append({"code": "MISSING_SOURCE", "message": "No official artifacts are linked."})
    if not scope.is_test_fixture and any(
        link.artifact.source_class != OfficialSourceArtifact.SourceClass.OFFICIAL
        for link in source_links
    ):
        errors.append(
            {"code": "FIXTURE_SOURCE", "message": "Test fixtures cannot support official scope."}
        )
    items = list(scope.items.select_related("parent", "source_artifact"))
    linked_ids = {link.artifact_id for link in source_links}
    linked_identities = {
        (link.artifact.stable_id, link.artifact.source_version) for link in source_links
    }
    if not items:
        errors.append({"code": "EMPTY_SCOPE", "message": "Scope has no items."})
    for item in items:
        if item.parent_id and item.parent.scope_version_id != scope.id:
            errors.append({"code": "MISSING_PARENT", "item": item.stable_id})
        if item.source_artifact_id not in linked_ids:
            errors.append({"code": "UNRESOLVED_SOURCE_MAPPING", "item": item.stable_id})
        treatment_source = item.treatment_metadata.get("source")
        if (
            treatment_source
            and (treatment_source["stable_id"], treatment_source["source_version"])
            not in linked_identities
        ):
            errors.append({"code": "UNRESOLVED_TREATMENT_SOURCE", "item": item.stable_id})
        if item.is_leaf and item.children.exists():
            errors.append({"code": "LEAF_HAS_CHILDREN", "item": item.stable_id})
        if (
            item.is_leaf
            and item.perimeter == OfficialScopeItem.Perimeter.TESTABLE
            and not (item.official_label.strip() or item.official_text.strip())
        ):
            errors.append({"code": "EMPTY_TESTABLE_LEAF", "item": item.stable_id})
        if not item.is_leaf and not item.children.exists():
            warnings.append({"code": "EMPTY_BRANCH", "item": item.stable_id})
    roots = [item for item in items if item.parent_id is None]
    if not roots:
        errors.append({"code": "NO_ROOT", "message": "Scope hierarchy has no root."})
    info.append({"code": "COUNTS", "items": len(items), "leaves": sum(i.is_leaf for i in items)})
    normalized = _normalized_scope(scope)
    checksum = canonical_sha256(normalized)
    info.append({"code": "NORMALIZED_SHA256", "value": checksum})
    return ValidationReport(tuple(errors), tuple(warnings), tuple(info)), checksum


@transaction.atomic
def validate_scope_version(scope_id):
    scope = OfficialScopeVersion.objects.select_for_update().get(pk=scope_id)
    if scope.status not in (
        OfficialScopeVersion.Status.DRAFT,
        OfficialScopeVersion.Status.VALIDATED,
    ):
        raise ValidationError("Only draft or validated scopes may be validated.")
    report, checksum = validate_scope(scope)
    scope.validation_report = report.as_dict()
    scope.normalized_sha256 = checksum
    scope.validated_at = timezone.now()
    scope.status = (
        OfficialScopeVersion.Status.VALIDATED if report.valid else OfficialScopeVersion.Status.DRAFT
    )
    scope.save()
    return scope, report


@transaction.atomic
def validate_and_activate(scope_id, *, allow_test_fixture=False):
    scope = OfficialScopeVersion.objects.select_for_update().get(pk=scope_id)
    if scope.status not in (
        OfficialScopeVersion.Status.DRAFT,
        OfficialScopeVersion.Status.VALIDATED,
    ):
        raise ValidationError("Only draft or validated scope versions may be activated.")
    if scope.is_test_fixture and not allow_test_fixture:
        raise ValidationError("TEST_FIXTURE scope cannot be activated as production truth.")
    report, checksum = validate_scope(scope)
    if not report.valid:
        raise ValidationError(report.as_dict())
    if scope.normalized_sha256 != checksum or not scope.validation_report.get("valid"):
        raise ValidationError(
            "Scope must be explicitly validated after its last normalized change."
        )
    previous = (
        OfficialScopeVersion.objects.select_for_update()
        .filter(
            exam_program=scope.exam_program,
            exam_component=scope.exam_component,
            status=OfficialScopeVersion.Status.ACTIVE,
            is_test_fixture=scope.is_test_fixture,
        )
        .exclude(pk=scope.pk)
        .first()
    )
    if previous:
        previous.status = OfficialScopeVersion.Status.SUPERSEDED
        previous.save(update_fields=("status",))
        scope.supersedes = previous
    scope.status = OfficialScopeVersion.Status.ACTIVE
    scope.activated_at = timezone.now()
    scope.save()
    return scope, report
