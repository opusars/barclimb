import pytest
from django.db import DatabaseError, connection, transaction

from official_scope.models import (
    OfficialScopeItem,
    OfficialScopeSource,
    OfficialScopeVersion,
    OfficialSourceArtifact,
)
from official_scope.services import (
    register_artifact,
    validate_and_activate,
    validate_scope_version,
)

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.postgres]


def test_postgres_trigger_rejects_queryset_artifact_update_and_delete():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL-specific immutable artifact trigger")
    artifact, _ = register_artifact(
        content=b"TEST_FIXTURE immutable bytes",
        stable_id="TEST_FIXTURE_POSTGRES_IMMUTABLE",
        source_authority="TEST_FIXTURE",
        artifact_type="SYNTHETIC",
        official_title="TEST_FIXTURE PostgreSQL immutability",
        source_version="V1",
        source_class="TEST_FIXTURE",
    )
    with pytest.raises(DatabaseError), transaction.atomic():
        OfficialSourceArtifact.objects.filter(pk=artifact.pk).update(official_title="changed")
    with pytest.raises(DatabaseError), transaction.atomic():
        OfficialSourceArtifact.objects.filter(pk=artifact.pk).delete()
    artifact.refresh_from_db()
    assert artifact.official_title == "TEST_FIXTURE PostgreSQL immutability"


def test_postgres_triggers_reject_historical_scope_and_child_bulk_mutation():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL-specific historical scope triggers")
    artifact, _ = register_artifact(
        content=b"TEST_FIXTURE scope",
        stable_id="TEST_FIXTURE_POSTGRES_SCOPE",
        source_authority="TEST_FIXTURE",
        artifact_type="SYNTHETIC",
        official_title="TEST_FIXTURE PostgreSQL scope",
        source_version="V1",
        source_class="TEST_FIXTURE",
    )
    scope = OfficialScopeVersion.objects.create(
        version_identifier="TEST_FIXTURE_POSTGRES_SCOPE_V1", is_test_fixture=True
    )
    OfficialScopeSource.objects.create(scope_version=scope, artifact=artifact, role="PERIMETER")
    root = OfficialScopeItem.objects.create(
        scope_version=scope,
        stable_id="fictional-root",
        official_label="TEST_FIXTURE Fictional root",
        source_artifact=artifact,
        source_locator="fixture:1",
    )
    item = OfficialScopeItem.objects.create(
        scope_version=scope,
        stable_id="fictional-leaf",
        parent=root,
        official_label="TEST_FIXTURE Fictional granular leaf",
        perimeter="TESTABLE",
        is_leaf=True,
        source_artifact=artifact,
        source_locator="fixture:1.1",
    )
    validate_scope_version(scope.pk)
    validate_and_activate(scope.pk, allow_test_fixture=True)
    with pytest.raises(DatabaseError), transaction.atomic():
        OfficialScopeItem.objects.filter(pk=item.pk).update(official_label="changed")
    with pytest.raises(DatabaseError), transaction.atomic():
        OfficialScopeVersion.objects.filter(pk=scope.pk).update(normalized_sha256="0" * 64)
    item.refresh_from_db()
    scope.refresh_from_db()
    assert item.official_label == "TEST_FIXTURE Fictional granular leaf"
    assert scope.status == "ACTIVE"
