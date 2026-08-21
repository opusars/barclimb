import copy
import json
from io import StringIO

import pytest
from curriculum_fixtures import (
    KINDS,
    compiler_manifest,
    problematic_compiler_manifest,
    synthetic_scope_manifest,
)
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.management import call_command
from django.test import override_settings
from rest_framework.test import APIClient

from accounts.models import User
from curriculum.models import (
    CoverageReleaseSnapshot,
    CurriculumCompileVersion,
    ObligationRelationship,
    ReconciliationIssue,
)
from curriculum.services import (
    certify_curriculum,
    compare_scope_drift,
    compile_manifest,
    normalize_statement,
    reconcile_curriculum,
    resolve_issue,
)
from official_scope.importer import import_manifest
from official_scope.models import OfficialScopeVersion
from official_scope.services import validate_and_activate

pytestmark = pytest.mark.django_db


def active_scope(version="TEST_FIXTURE_SCOPE_A", *, changed=False):
    import_manifest(synthetic_scope_manifest(version, changed=changed))
    scope = OfficialScopeVersion.objects.get(version_identifier=version)
    validate_and_activate(scope.pk, allow_test_fixture=True)
    scope.refresh_from_db()
    return scope


def compiled_clean(**kwargs):
    active_scope(kwargs.get("scope_version", "TEST_FIXTURE_SCOPE_A"))
    compile_version, created = compile_manifest(compiler_manifest(**kwargs))
    return compile_version, created


def test_normalization_and_canonical_compile_are_deterministic_and_idempotent():
    assert normalize_statement("  TEST\u00a0Fixture   RULE ") == "test fixture rule"
    compile_version, created = compiled_clean()
    rerun, created_again = compile_manifest(copy.deepcopy(compiler_manifest()))
    assert created is True and created_again is False
    assert rerun.pk == compile_version.pk
    assert rerun.canonical_sha256 == compile_version.canonical_sha256
    changed = compiler_manifest()
    changed["obligations"][0]["statement"] = "TEST_FIXTURE changed"
    with pytest.raises(ValidationError, match="different deterministic input"):
        compile_manifest(changed)


def test_all_obligation_kinds_and_typed_relationships_compile():
    compile_version, _ = compiled_clean()
    assert set(compile_version.obligations.values_list("kind", flat=True)) == set(KINDS)
    assert (
        ObligationRelationship.objects.filter(source__compile_version=compile_version).count() == 10
    )
    assert not compile_version.issues.exists()
    assert all(
        obligation.decision == "AUTO_APPROVABLE" for obligation in compile_version.obligations.all()
    )


def test_many_to_many_scope_mapping_is_version_scoped():
    active_scope()
    payload = compiler_manifest()
    payload["obligations"][0]["scope_item_ids"] = [
        "fictional-leaf-a",
        "fictional-leaf-b",
    ]
    compile_version, _ = compile_manifest(payload)
    rule = compile_version.obligations.get(stable_id="fixture-rule")
    assert set(rule.scope_items.values_list("stable_id", flat=True)) == {
        "fictional-leaf-a",
        "fictional-leaf-b",
    }


def test_problem_fixture_reports_every_reconciliation_category_and_blocks_jurisdiction():
    active_scope()
    compile_version, _ = compile_manifest(problematic_compiler_manifest())
    _, report = reconcile_curriculum(compile_version.pk)
    categories = set(compile_version.issues.values_list("category", flat=True))
    assert {
        "OMISSION",
        "EXCESS",
        "CONFLICT",
        "AMBIGUITY",
        "DUPLICATE",
        "UNSUPPORTED_PROVENANCE",
        "UNSUPPORTED_JURISDICTION",
    } <= categories
    blocked = compile_version.obligations.filter(
        stable_id__in=(
            "fixture-california-rule",
            "fixture-state-constitution-rule",
            "fixture-local-procedure",
        )
    )
    assert blocked.count() == 3
    assert all(
        obligation.compiler_status == "BLOCKED"
        and obligation.is_core is False
        and obligation.decision == "BLOCKED"
        for obligation in blocked
    )
    assert report["blocking_omission_count"] == 1
    assert report["excess_count"] == 1
    assert report["unresolved_conflict_count"] == 1
    assert report["unresolved_ambiguity_count"] == 1
    assert report["provenance_deficient_count"] == 1


def test_invalid_and_circular_or_nonsensical_relationships_are_visible():
    active_scope()
    payload = compiler_manifest()
    payload["relationships"].append(
        {
            "source_id": "fixture-element",
            "target_id": "fixture-rule",
            "kind": "HAS_ELEMENT",
        }
    )
    payload["relationships"].extend(
        [
            {
                "source_id": "fixture-element",
                "target_id": "fixture-factor",
                "kind": "HAS_FACTOR",
            },
            {
                "source_id": "fixture-factor",
                "target_id": "fixture-element",
                "kind": "HAS_ELEMENT",
            },
        ]
    )
    compile_version, _ = compile_manifest(payload)
    issues = compile_version.issues.filter(category="INVALID_STRUCTURE")
    assert issues.count() == 2
    assert set(issues.values_list("severity", flat=True)) == {"BLOCKING"}


def test_secondary_evidence_alone_is_provenance_deficient_and_review_required():
    active_scope()
    payload = compiler_manifest()
    payload["obligations"][0]["evidence"] = [
        {
            "authority_id": "fixture-secondary-authority",
            "role": "SECONDARY_RECONCILIATION",
            "locator": "TEST_FIXTURE note 1",
        }
    ]
    compile_version, _ = compile_manifest(payload)
    rule = compile_version.obligations.get(stable_id="fixture-rule")
    assert rule.decision == "REVIEW_REQUIRED"
    assert compile_version.issues.filter(
        obligation=rule, category="UNSUPPORTED_PROVENANCE", severity="BLOCKING"
    ).exists()


def test_clean_reconciliation_and_explicit_fixture_certification_snapshot():
    compile_version, _ = compiled_clean()
    compile_version, report = reconcile_curriculum(compile_version.pk)
    assert report["total_official_leaves"] == 2
    assert report["leaves_sufficiently_covered"] == 2
    assert report["blocking_issue_count"] == 0
    with pytest.raises(ValidationError, match="cannot certify as production"):
        certify_curriculum(compile_version.pk)
    snapshot = certify_curriculum(compile_version.pk, allow_test_fixture=True)
    compile_version.refresh_from_db()
    assert compile_version.status == "CERTIFIED"
    assert snapshot.source_class == "TEST_FIXTURE"
    assert snapshot.obligation_count == 11
    assert snapshot.covered_leaf_count == 2
    assert len(snapshot.certification_sha256) == 64
    with pytest.raises(ValidationError):
        snapshot.save()


def test_certification_rolls_back_with_blocking_issue():
    compile_version, _ = compiled_clean()
    reconcile_curriculum(compile_version.pk)
    ReconciliationIssue.objects.create(
        compile_version=compile_version,
        stable_id="TEST_FIXTURE-late-block",
        category="CONFLICT",
        severity="BLOCKING",
        message="TEST_FIXTURE unresolved late conflict",
        canonical_sha256="0" * 64,
    )
    with pytest.raises(ValidationError):
        certify_curriculum(compile_version.pk, allow_test_fixture=True)
    compile_version.refresh_from_db()
    assert compile_version.status == "RECONCILED"
    assert not CoverageReleaseSnapshot.objects.filter(compile_version=compile_version).exists()


def test_review_boundary_requires_staff_and_records_resolution():
    active_scope()
    compile_version, _ = compile_manifest(problematic_compiler_manifest())
    issue = compile_version.issues.get(category="CONFLICT")
    ordinary = User.objects.create_user("reader@example.com", "reader", "strong-password-1")
    with pytest.raises(PermissionDenied):
        resolve_issue(
            issue.pk,
            reviewer=ordinary,
            resolution="ACCEPT",
            rationale="TEST_FIXTURE unauthorized",
        )
    reviewer = User.objects.create_user(
        "reviewer@example.com", "reviewer", "strong-password-1", is_staff=True
    )
    review = resolve_issue(
        issue.pk,
        reviewer=reviewer,
        resolution="ACCEPT",
        rationale="TEST_FIXTURE reviewed conflict evidence.",
        changes_canonical_truth=False,
    )
    issue.refresh_from_db()
    assert issue.status == "RESOLVED"
    assert review.reviewer == reviewer and review.rationale


def test_historical_supersession_and_scope_drift_preserve_old_truth():
    scope_a = active_scope()
    compile_a, _ = compile_manifest(compiler_manifest())
    reconcile_curriculum(compile_a.pk)
    snapshot_a = certify_curriculum(compile_a.pk, allow_test_fixture=True)
    scope_b = active_scope("TEST_FIXTURE_SCOPE_B", changed=True)
    payload_b = compiler_manifest("TEST_FIXTURE_SCOPE_B", "TEST_FIXTURE_COMPILE_B")
    payload_b["compile"]["supersedes"] = "TEST_FIXTURE_COMPILE_A"
    extra = copy.deepcopy(payload_b["obligations"][0])
    extra.update(
        {
            "stable_id": "fixture-added-leaf-rule",
            "statement": "TEST_FIXTURE rule for added leaf.",
            "scope_item_ids": ["fictional-leaf-c"],
        }
    )
    payload_b["obligations"].append(extra)
    compile_b, _ = compile_manifest(payload_b)
    reconcile_curriculum(compile_b.pk)
    certify_curriculum(compile_b.pk, allow_test_fixture=True)
    compile_a.refresh_from_db()
    assert compile_a.status == "SUPERSEDED"
    assert CoverageReleaseSnapshot.objects.get(pk=snapshot_a.pk).certification_sha256
    assert compile_a.obligations.get(stable_id="fixture-rule").statement.startswith("TEST_FIXTURE")
    drift = compare_scope_drift(scope_a, scope_b, old_compile=compile_a)
    assert drift["added_leaves"] == ["fictional-leaf-c"]
    assert drift["changed_leaves"] == ["fictional-leaf-b"]
    assert drift["requires_re_evaluation"] is True
    assert drift["potentially_impacted_obligations"]
    assert drift["unaffected_obligations"]

    scope_c_manifest = synthetic_scope_manifest(
        "TEST_FIXTURE_SCOPE_C", changed=True, remove_leaf_a=True
    )
    import_manifest(scope_c_manifest)
    scope_c = OfficialScopeVersion.objects.get(version_identifier="TEST_FIXTURE_SCOPE_C")
    validate_and_activate(scope_c.pk, allow_test_fixture=True)
    removed_drift = compare_scope_drift(scope_a, scope_c, old_compile=compile_a)
    assert removed_drift["removed_leaves"] == ["fictional-leaf-a"]
    assert "fixture-rule" in removed_drift["potentially_impacted_obligations"]


def test_internal_api_is_authenticated_read_only_and_fixture_excluded_by_default():
    compile_version, _ = compiled_clean()
    reconcile_curriculum(compile_version.pk)
    certify_curriculum(compile_version.pk, allow_test_fixture=True)
    client = APIClient()
    assert client.get("/api/v1/curriculum/certified/").status_code == 401
    user = User.objects.create_user("api@example.com", "api_reader", "strong-password-1")
    client.force_authenticate(user)
    assert client.get("/api/v1/curriculum/certified/").status_code == 404
    with override_settings(CURRICULUM_ALLOW_TEST_FIXTURE_API=True):
        response = client.get("/api/v1/curriculum/certified/")
    assert response.status_code == 200
    assert response.data["source_class"] == "TEST_FIXTURE"
    assert response.data["coverage"]["blocking_issue_count"] == 0
    assert len(response.data["obligations"]) == 11
    assert client.post("/api/v1/curriculum/certified/", {}).status_code == 405


def test_operator_dry_run_has_no_hidden_mutation(tmp_path):
    active_scope()
    path = tmp_path / "TEST_FIXTURE-compiler.json"
    path.write_text(json.dumps(compiler_manifest()))
    output = StringIO()
    call_command(
        "compile_rule_obligations",
        path,
        reconcile=True,
        dry_run=True,
        stdout=output,
    )
    result = json.loads(output.getvalue())
    assert result["dry_run"] is True and result["certified"] is False
    assert result["state_changed"] is True
    assert result["certification_eligible"] is True
    assert not CurriculumCompileVersion.objects.exists()
