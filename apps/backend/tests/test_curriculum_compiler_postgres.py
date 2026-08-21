import pytest
from curriculum_fixtures import compiler_manifest, synthetic_scope_manifest
from django.db import DatabaseError, IntegrityError, connection, transaction

from curriculum.models import (
    AuthoritySource,
    CoveragePolicy,
    CoverageReleaseSnapshot,
    CurriculumCompileVersion,
    ObligationRelationship,
    RuleObligation,
)
from curriculum.services import certify_curriculum, compile_manifest, reconcile_curriculum
from official_scope.importer import import_manifest
from official_scope.models import OfficialScopeVersion
from official_scope.services import validate_and_activate

pytestmark = [pytest.mark.django_db(transaction=True), pytest.mark.postgres]


def certified_fixture_compile():
    import_manifest(synthetic_scope_manifest())
    scope = OfficialScopeVersion.objects.get(version_identifier="TEST_FIXTURE_SCOPE_A")
    validate_and_activate(scope.pk, allow_test_fixture=True)
    compile_version, _ = compile_manifest(compiler_manifest())
    reconcile_curriculum(compile_version.pk)
    snapshot = certify_curriculum(compile_version.pk, allow_test_fixture=True)
    return compile_version, snapshot


def test_postgres_constraints_reject_duplicate_identity_and_self_relationship():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL-specific curriculum constraints")
    compile_version, _ = certified_fixture_compile()
    obligation = compile_version.obligations.get(stable_id="fixture-rule")
    with pytest.raises(IntegrityError), transaction.atomic():
        RuleObligation.objects.bulk_create(
            [
                RuleObligation(
                    compile_version=compile_version,
                    stable_id=obligation.stable_id,
                    kind="RULE",
                    normalized_statement="duplicate",
                    statement="duplicate",
                    canonical_sha256="1" * 64,
                    decision="BLOCKED",
                    inclusion_rationale="TEST_FIXTURE duplicate",
                )
            ]
        )
    with pytest.raises(IntegrityError), transaction.atomic():
        ObligationRelationship.objects.bulk_create(
            [
                ObligationRelationship(
                    source=obligation,
                    target=obligation,
                    kind="HAS_ELEMENT",
                )
            ]
        )
    with pytest.raises(IntegrityError), transaction.atomic():
        CoveragePolicy.objects.bulk_create(
            [
                CoveragePolicy(
                    stable_id="TEST_FIXTURE_ZERO_POLICY",
                    policy_version="V1",
                    minimum_obligations_per_leaf=0,
                    requires_primary_authority=True,
                    allowed_obligation_kinds=["RULE"],
                    canonical_sha256="2" * 64,
                    source_class="TEST_FIXTURE",
                )
            ]
        )


def test_postgres_triggers_reject_certified_history_and_provenance_bulk_mutation():
    if connection.vendor != "postgresql":
        pytest.skip("PostgreSQL-specific certified-history triggers")
    compile_version, snapshot = certified_fixture_compile()
    obligation = compile_version.obligations.get(stable_id="fixture-rule")
    authority = AuthoritySource.objects.get(stable_id="fixture-primary-authority")
    with pytest.raises(DatabaseError), transaction.atomic():
        CurriculumCompileVersion.objects.filter(pk=compile_version.pk).update(
            canonical_sha256="0" * 64
        )
    with pytest.raises(DatabaseError), transaction.atomic():
        RuleObligation.objects.filter(pk=obligation.pk).update(statement="changed")
    with pytest.raises(DatabaseError), transaction.atomic():
        AuthoritySource.objects.filter(pk=authority.pk).update(title="changed")
    with pytest.raises(DatabaseError), transaction.atomic():
        CoverageReleaseSnapshot.objects.filter(pk=snapshot.pk).delete()
    compile_version.refresh_from_db()
    obligation.refresh_from_db()
    assert compile_version.status == "CERTIFIED"
    assert obligation.statement.startswith("TEST_FIXTURE")
