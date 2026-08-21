import base64
import copy
import hashlib
import json
from io import StringIO

import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import override_settings
from rest_framework.test import APIClient

from accounts.models import User
from official_scope.importer import import_manifest
from official_scope.models import OfficialScopeItem, OfficialScopeVersion, OfficialSourceArtifact
from official_scope.services import (
    canonical_sha256,
    register_artifact,
    validate_and_activate,
    validate_scope,
)

pytestmark = pytest.mark.django_db


def fixture_manifest(version="TEST_FIXTURE_SCOPE_V1"):
    def artifact(stable_id, title, content):
        return {
            "stable_id": stable_id,
            "source_authority": "TEST_FIXTURE",
            "artifact_type": "SYNTHETIC_SCOPE" if "scope" in stable_id else "SYNTHETIC_BLUEPRINT",
            "official_title": f"TEST_FIXTURE — {title}",
            "source_version": "TEST_FIXTURE_V1",
            "source_class": "TEST_FIXTURE",
            "provenance_notes": (
                "Synthetic test material; not NCBE content and publication-ineligible."
            ),
            "content_base64": base64.b64encode(content.encode()).decode(),
        }

    return {
        "schema": "BARCLIMB_OFFICIAL_SCOPE_IMPORT_V1",
        "artifacts": [
            artifact("test-fixture-scope", "fictional content scope", "synthetic scope bytes"),
            artifact("test-fixture-blueprint", "fictional blueprint", "synthetic blueprint bytes"),
        ],
        "scope": {
            "version_identifier": version,
            "exam_program": "NEXTGEN_UBE",
            "exam_component": "NEXTGEN_CORE",
            "is_national": True,
            "jurisdiction": "",
            "is_test_fixture": True,
            "sources": [
                {"artifact_id": "test-fixture-scope", "role": "PERIMETER"},
                {"artifact_id": "test-fixture-blueprint", "role": "TREATMENT"},
            ],
            "items": [
                {
                    "stable_id": "fictional-domain",
                    "official_label": "TEST_FIXTURE Fictional Domain",
                    "source_artifact_id": "test-fixture-scope",
                    "source_locator": "fixture:1",
                    "subject_group": "TEST_FIXTURE",
                },
                {
                    "stable_id": "fictional-leaf",
                    "parent_id": "fictional-domain",
                    "official_label": "TEST_FIXTURE Fictional granular leaf",
                    "ordering": 1,
                    "perimeter": "TESTABLE",
                    "subject_group": "TEST_FIXTURE",
                    "is_leaf": True,
                    "source_artifact_id": "test-fixture-scope",
                    "source_locator": "fixture:1.1",
                    "treatment_metadata": {
                        "emphasis": "TEST_FIXTURE_HIGH",
                        "assessment_forms": ["TEST_FIXTURE_FORM"],
                        "source": {
                            "stable_id": "test-fixture-blueprint",
                            "source_version": "TEST_FIXTURE_V1",
                        },
                    },
                },
            ],
        },
    }


def test_hashing_and_artifact_registration_are_deterministic_and_idempotent():
    kwargs = {
        "stable_id": "TEST_FIXTURE_ARTIFACT",
        "source_authority": "TEST_FIXTURE",
        "artifact_type": "SYNTHETIC",
        "official_title": "TEST_FIXTURE artifact",
        "source_version": "V1",
        "source_class": "TEST_FIXTURE",
    }
    first, created = register_artifact(content=b"same bytes", **kwargs)
    second, created_again = register_artifact(content=b"same bytes", **kwargs)
    assert created is True and created_again is False and first.pk == second.pk
    assert first.content_sha256 == hashlib.sha256(b"same bytes").hexdigest()
    with pytest.raises(ValidationError):
        register_artifact(content=b"changed bytes", **kwargs)
    changed = dict(kwargs, official_title="changed identity metadata")
    with pytest.raises(ValidationError):
        register_artifact(content=b"same bytes", **changed)
    notes_changed = dict(kwargs, provenance_notes="later nonidentity operator note")
    same, was_created = register_artifact(content=b"same bytes", **notes_changed)
    assert same.pk == first.pk and was_created is False


def test_artifact_rows_are_immutable_and_new_content_requires_new_version():
    payload = fixture_manifest()
    import_manifest(payload)
    artifact = OfficialSourceArtifact.objects.get(stable_id="test-fixture-scope")
    artifact.official_title = "replacement"
    with pytest.raises(ValidationError):
        artifact.save()
    payload["artifacts"][0]["source_version"] = "TEST_FIXTURE_V2"
    payload["artifacts"][0]["content_base64"] = base64.b64encode(b"changed").decode()
    payload["artifacts"][0]["supersedes"] = {
        "stable_id": "test-fixture-scope",
        "source_version": "TEST_FIXTURE_V1",
    }
    payload["scope"]["version_identifier"] = "TEST_FIXTURE_SCOPE_V2"
    result = import_manifest(payload)
    assert result["artifacts_created"] == 1
    successor = OfficialSourceArtifact.objects.get(
        stable_id="test-fixture-scope", source_version="TEST_FIXTURE_V2"
    )
    assert successor.supersedes == artifact and artifact.has_been_superseded


def test_manifest_imports_multiple_sources_hierarchy_treatment_and_is_idempotent():
    payload = fixture_manifest()
    first = import_manifest(payload)
    second = import_manifest(copy.deepcopy(payload))
    assert first["artifact_count"] == 2
    assert first["item_count"] == 2 and first["leaf_count"] == 1
    assert first["scope_sha256"] == second["scope_sha256"]
    assert second["artifacts_created"] == 0 and second["scope_created"] is False
    leaf = OfficialScopeItem.objects.get(stable_id="fictional-leaf")
    assert leaf.parent.stable_id == "fictional-domain"
    assert leaf.treatment_metadata["emphasis"] == "TEST_FIXTURE_HIGH"


def test_canonical_checksum_changes_with_normalized_perimeter_but_not_key_order():
    assert canonical_sha256({"b": 2, "a": 1}) == canonical_sha256({"a": 1, "b": 2})
    assert canonical_sha256({"a": 1}) != canonical_sha256({"a": 2})
    first = import_manifest(fixture_manifest())
    changed = fixture_manifest("TEST_FIXTURE_SCOPE_V2")
    changed["scope"]["items"][1]["official_label"] = "TEST_FIXTURE changed leaf"
    second = import_manifest(changed)
    assert first["scope_sha256"] != second["scope_sha256"]


def test_missing_or_cyclic_parent_is_rejected_transactionally():
    payload = fixture_manifest()
    payload["scope"]["items"][1]["parent_id"] = "does-not-exist"
    with pytest.raises(ValidationError):
        import_manifest(payload)
    assert OfficialScopeVersion.objects.count() == 0


def test_duplicate_manifest_identities_are_rejected():
    payload = fixture_manifest()
    payload["scope"]["items"].append(copy.deepcopy(payload["scope"]["items"][1]))
    with pytest.raises(ValidationError, match="Duplicate scope-item"):
        import_manifest(payload)
    assert OfficialScopeVersion.objects.count() == 0


def test_duplicate_item_identity_has_database_constraint():
    import_manifest(fixture_manifest())
    item = OfficialScopeItem.objects.get(stable_id="fictional-leaf")
    item.pk = None
    with pytest.raises(IntegrityError), transaction.atomic():
        OfficialScopeItem.objects.bulk_create([item])


def test_national_nextgen_invariants_reject_jurisdiction_and_other_programs():
    for change in (
        {"jurisdiction": "California", "is_national": False},
        {"exam_program": "LEGACY_UBE"},
        {"exam_component": "CALIFORNIA_ADDON"},
    ):
        payload = fixture_manifest()
        payload["scope"].update(change)
        with pytest.raises(ValidationError):
            import_manifest(payload)


def test_validation_detects_unresolved_source_and_leaf_shape():
    result = import_manifest(fixture_manifest())
    scope = OfficialScopeVersion.objects.get(version_identifier=result["scope_version"])
    other, _ = register_artifact(
        content=b"unlinked",
        stable_id="TEST_FIXTURE_UNLINKED",
        source_authority="TEST_FIXTURE",
        artifact_type="SYNTHETIC",
        official_title="TEST_FIXTURE unlinked",
        source_version="V1",
        source_class="TEST_FIXTURE",
    )
    leaf = scope.items.get(stable_id="fictional-leaf")
    treatment = copy.deepcopy(leaf.treatment_metadata)
    treatment["source"] = {"stable_id": "missing", "source_version": "V1"}
    OfficialScopeItem.objects.filter(pk=leaf.pk).update(
        source_artifact=other, treatment_metadata=treatment
    )
    report, _ = validate_scope(scope)
    codes = {error["code"] for error in report.errors}
    assert {"UNRESOLVED_SOURCE_MAPPING", "UNRESOLVED_TREATMENT_SOURCE"} <= codes


def test_activation_is_explicit_rejects_fixture_by_default_and_preserves_history():
    first = import_manifest(fixture_manifest())
    scope1 = OfficialScopeVersion.objects.get(version_identifier=first["scope_version"])
    assert scope1.status == "VALIDATED"
    with pytest.raises(ValidationError):
        validate_and_activate(scope1.pk)
    scope1.refresh_from_db()
    assert scope1.status == "VALIDATED"
    validate_and_activate(scope1.pk, allow_test_fixture=True)
    second = import_manifest(fixture_manifest("TEST_FIXTURE_SCOPE_V2"))
    scope2 = OfficialScopeVersion.objects.get(version_identifier=second["scope_version"])
    validate_and_activate(scope2.pk, allow_test_fixture=True)
    scope1.refresh_from_db()
    scope2.refresh_from_db()
    assert scope1.status == "SUPERSEDED"
    assert scope2.status == "ACTIVE" and scope2.supersedes == scope1
    assert scope1.items.get(stable_id="fictional-leaf").official_label
    with pytest.raises(ValidationError):
        scope1.delete()


def test_failed_activation_rolls_back_without_superseding_active_scope():
    first = import_manifest(fixture_manifest())
    scope1 = OfficialScopeVersion.objects.get(version_identifier=first["scope_version"])
    validate_and_activate(scope1.pk, allow_test_fixture=True)
    second = import_manifest(fixture_manifest("TEST_FIXTURE_SCOPE_INVALID"))
    scope2 = OfficialScopeVersion.objects.get(version_identifier=second["scope_version"])
    leaf = scope2.items.get(stable_id="fictional-leaf")
    OfficialScopeItem.objects.filter(pk=leaf.pk).update(official_label="", official_text="")
    with pytest.raises(ValidationError):
        validate_and_activate(scope2.pk, allow_test_fixture=True)
    scope1.refresh_from_db()
    scope2.refresh_from_db()
    assert scope1.status == "ACTIVE" and scope2.status == "VALIDATED"


def test_api_requires_authentication_and_serializes_active_contract():
    imported = import_manifest(fixture_manifest())
    scope = OfficialScopeVersion.objects.get(version_identifier=imported["scope_version"])
    validate_and_activate(scope.pk, allow_test_fixture=True)
    client = APIClient()
    assert client.get("/api/v1/official-scope/active/").status_code == 401
    user = User.objects.create_user("reader@example.com", "reader", "strong-password-1")
    client.force_authenticate(user)
    assert client.get("/api/v1/official-scope/active/").status_code == 404
    with override_settings(OFFICIAL_SCOPE_ALLOW_TEST_FIXTURE_API=True):
        response = client.get("/api/v1/official-scope/active/")
    assert response.status_code == 200
    assert response.data["exam_program"] == "NEXTGEN_UBE"
    assert len(response.data["sources"]) == 2 and len(response.data["items"]) == 2
    assert "validation_report" not in response.data
    assert client.post("/api/v1/official-scope/active/", {}).status_code == 405


def test_command_dry_run_reports_without_mutation(tmp_path):
    path = tmp_path / "TEST_FIXTURE-manifest.json"
    path.write_text(json.dumps(fixture_manifest()))
    output = StringIO()
    call_command("import_official_scope", path, dry_run=True, stdout=output)
    result = json.loads(output.getvalue())
    assert result["dry_run"] is True and result["activated"] is False
    assert OfficialScopeVersion.objects.count() == 0
