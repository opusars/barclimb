import base64
import copy

KINDS = (
    "RULE",
    "ELEMENT",
    "FACTOR",
    "EXCEPTION",
    "LIMITATION",
    "DEFENSE",
    "REMEDY",
    "PROCEDURAL_STEP",
    "DISTINCTION",
    "DEFINITION",
    "ETHICS_DUTY",
)

RELATIONSHIPS = {
    "ELEMENT": "HAS_ELEMENT",
    "FACTOR": "HAS_FACTOR",
    "EXCEPTION": "HAS_EXCEPTION",
    "LIMITATION": "HAS_LIMITATION",
    "DEFENSE": "HAS_DEFENSE",
    "REMEDY": "HAS_REMEDY",
    "PROCEDURAL_STEP": "HAS_PROCEDURAL_STEP",
    "DISTINCTION": "HAS_DISTINCTION",
    "DEFINITION": "DEFINES",
    "ETHICS_DUTY": "HAS_ETHICS_DUTY",
}


def synthetic_scope_manifest(version="TEST_FIXTURE_SCOPE_A", *, changed=False, remove_leaf_a=False):
    content = f"TEST_FIXTURE official perimeter {version}"
    leaves = [
        {
            "stable_id": "fictional-leaf-a",
            "parent_id": "fictional-root",
            "official_label": "TEST_FIXTURE Fictional Leaf A",
            "perimeter": "TESTABLE",
            "is_leaf": True,
            "source_artifact_id": f"fixture-scope-{version}",
            "source_locator": "TEST_FIXTURE:1.1",
        },
        {
            "stable_id": "fictional-leaf-b",
            "parent_id": "fictional-root",
            "official_label": (
                "TEST_FIXTURE Fictional Leaf B revised"
                if changed
                else "TEST_FIXTURE Fictional Leaf B"
            ),
            "perimeter": "TESTABLE",
            "is_leaf": True,
            "source_artifact_id": f"fixture-scope-{version}",
            "source_locator": "TEST_FIXTURE:1.2",
        },
    ]
    if remove_leaf_a:
        leaves = [leaf for leaf in leaves if leaf["stable_id"] != "fictional-leaf-a"]
    if changed:
        leaves.append(
            {
                "stable_id": "fictional-leaf-c",
                "parent_id": "fictional-root",
                "official_label": "TEST_FIXTURE Fictional Added Leaf C",
                "perimeter": "TESTABLE",
                "is_leaf": True,
                "source_artifact_id": f"fixture-scope-{version}",
                "source_locator": "TEST_FIXTURE:1.3",
            }
        )
    return {
        "schema": "BARCLIMB_OFFICIAL_SCOPE_IMPORT_V1",
        "artifacts": [
            {
                "stable_id": f"fixture-scope-{version}",
                "source_authority": "TEST_FIXTURE",
                "artifact_type": "SYNTHETIC_SCOPE",
                "official_title": f"TEST_FIXTURE synthetic perimeter {version}",
                "source_version": version,
                "source_class": "TEST_FIXTURE",
                "provenance_notes": "TEST_FIXTURE; never real NCBE content.",
                "content_base64": base64.b64encode(content.encode()).decode(),
            }
        ],
        "scope": {
            "version_identifier": version,
            "is_test_fixture": True,
            "sources": [{"artifact_id": f"fixture-scope-{version}", "role": "PERIMETER"}],
            "items": [
                {
                    "stable_id": "fictional-root",
                    "official_label": "TEST_FIXTURE Fictional Root",
                    "source_artifact_id": f"fixture-scope-{version}",
                    "source_locator": "TEST_FIXTURE:1",
                },
                *leaves,
            ],
        },
    }


def compiler_manifest(
    scope_version="TEST_FIXTURE_SCOPE_A",
    compile_version="TEST_FIXTURE_COMPILE_A",
):
    authorities = [
        {
            "stable_id": "fixture-primary-authority",
            "source_version": "TEST_FIXTURE_V1",
            "authority_class": "SUBSTANTIVE_PRIMARY",
            "authority_type": "SYNTHETIC_MODEL_RULE",
            "title": "TEST_FIXTURE Fictional Model Rule",
            "canonical_citation": "TEST_FIXTURE Rule 1",
            "source_class": "TEST_FIXTURE",
            "content_base64": base64.b64encode(b"TEST_FIXTURE primary authority").decode(),
        },
        {
            "stable_id": "fixture-secondary-authority",
            "source_version": "TEST_FIXTURE_V1",
            "authority_class": "SECONDARY_RECONCILIATION",
            "authority_type": "SYNTHETIC_COMMENTARY",
            "title": "TEST_FIXTURE Fictional Commentary",
            "canonical_citation": "TEST_FIXTURE Commentary 1",
            "source_class": "TEST_FIXTURE",
            "content_base64": base64.b64encode(b"TEST_FIXTURE secondary evidence").decode(),
        },
    ]
    obligations = []
    for index, kind in enumerate(KINDS):
        obligations.append(
            {
                "stable_id": f"fixture-{kind.lower().replace('_', '-')}",
                "kind": kind,
                "statement": f"TEST_FIXTURE normalized statement for {kind}.",
                "scope_item_ids": ["fictional-leaf-a" if index % 2 == 0 else "fictional-leaf-b"],
                "inclusion_rationale": "TEST_FIXTURE exact perimeter and primary authority.",
                "evidence": [
                    {
                        "authority_id": "fixture-primary-authority",
                        "role": "SUBSTANTIVE_SUPPORT",
                        "locator": f"TEST_FIXTURE section {index + 1}",
                        "proposition": f"TEST_FIXTURE proposition {kind}",
                    }
                ],
            }
        )
    root_id = "fixture-rule"
    relationships = [
        {
            "source_id": root_id,
            "target_id": f"fixture-{kind.lower().replace('_', '-')}",
            "kind": relationship,
            "ordering": index,
        }
        for index, (kind, relationship) in enumerate(RELATIONSHIPS.items(), start=1)
    ]
    return {
        "schema": "BARCLIMB_RULE_COMPILER_V1",
        "compile": {
            "version_identifier": compile_version,
            "official_scope_version": scope_version,
            "compiler_schema_version": "TEST_FIXTURE_COMPILER_V1",
            "source_class": "TEST_FIXTURE",
        },
        "coverage_policy": {
            "stable_id": "TEST_FIXTURE_POLICY",
            "policy_version": "V1",
            "minimum_obligations_per_leaf": 1,
            "requires_primary_authority": True,
            "allowed_obligation_kinds": list(KINDS),
        },
        "authorities": authorities,
        "obligations": obligations,
        "relationships": relationships,
    }


def problematic_compiler_manifest():
    payload = compiler_manifest(compile_version="TEST_FIXTURE_COMPILE_PROBLEMS")
    payload = copy.deepcopy(payload)
    # Create an omission by removing every mapping to leaf B.
    for candidate in payload["obligations"]:
        if candidate["scope_item_ids"] == ["fictional-leaf-b"]:
            candidate["scope_item_ids"] = ["fictional-leaf-a"]
    payload["obligations"].extend(
        [
            {
                **copy.deepcopy(payload["obligations"][0]),
                "stable_id": "fixture-duplicate",
            },
            {
                "stable_id": "fixture-excess",
                "kind": "RULE",
                "statement": "TEST_FIXTURE unsupported excess rule.",
                "classification": "EXCESS",
                "scope_item_ids": [],
                "evidence": [],
            },
            {
                "stable_id": "fixture-conflict-a",
                "kind": "RULE",
                "statement": "TEST_FIXTURE conflict answer A.",
                "scope_item_ids": ["fictional-leaf-a"],
                "conflict_group": "fictional-conflict",
                "evidence": copy.deepcopy(payload["obligations"][0]["evidence"]),
            },
            {
                "stable_id": "fixture-conflict-b",
                "kind": "RULE",
                "statement": "TEST_FIXTURE incompatible conflict answer B.",
                "scope_item_ids": ["fictional-leaf-a"],
                "conflict_group": "fictional-conflict",
                "evidence": copy.deepcopy(payload["obligations"][0]["evidence"]),
            },
            {
                "stable_id": "fixture-ambiguity",
                "kind": "DISTINCTION",
                "statement": "TEST_FIXTURE ambiguous mapping.",
                "scope_item_ids": ["fictional-leaf-a"],
                "ambiguous": True,
                "evidence": copy.deepcopy(payload["obligations"][0]["evidence"]),
            },
            {
                "stable_id": "fixture-no-provenance",
                "kind": "RULE",
                "statement": "TEST_FIXTURE provenance-deficient rule.",
                "scope_item_ids": ["fictional-leaf-a"],
                "evidence": [],
            },
            {
                "stable_id": "fixture-california-rule",
                "kind": "RULE",
                "statement": "TEST_FIXTURE California-only rule.",
                "scope_item_ids": ["fictional-leaf-a"],
                "jurisdiction": "California",
                "evidence": copy.deepcopy(payload["obligations"][0]["evidence"]),
            },
            {
                "stable_id": "fixture-state-constitution-rule",
                "kind": "RULE",
                "statement": "TEST_FIXTURE state constitutional doctrine.",
                "scope_item_ids": ["fictional-leaf-a"],
                "jurisdiction": "Fictional State",
                "evidence": copy.deepcopy(payload["obligations"][0]["evidence"]),
            },
            {
                "stable_id": "fixture-local-procedure",
                "kind": "PROCEDURAL_STEP",
                "statement": "TEST_FIXTURE unsupported local procedure.",
                "scope_item_ids": ["fictional-leaf-a"],
                "jurisdiction": "Fictional County",
                "evidence": copy.deepcopy(payload["obligations"][0]["evidence"]),
            },
        ]
    )
    return payload
