# Official Source Registry and National NextGen Scope

## Authority and lifecycle

Only controlling official perimeter artifacts belong in the production registry. The current product coordinates are exactly `NEXTGEN_UBE` and `NEXTGEN_CORE`; v1 has no jurisdiction field value or active state component. Secondary references may later attach reconciliation evidence, but they do not define this perimeter and are not M2.1 dependencies.

Artifact acquisition/download is outside Django. Operators supply a controlled `BARCLIMB_OFFICIAL_SCOPE_IMPORT_V1` JSON manifest. Each artifact includes provenance metadata plus base64-encoded acquired bytes. Registration hashes the original bytes with SHA-256. The `(stable_id, source_version)` identity is immutable: identical input returns the existing row; changed bytes or identity metadata fails and requires a new version. Official documents are not committed by M2.1 because no licensing/distribution review was completed; tests use only synthetic `TEST_FIXTURE` bytes.

## Scope normalization

A manifest links any number of artifacts to a scope version with explicit roles. Its item list retains only source-supported hierarchy levels and provides stable item identity, parent identity, label/text, order, perimeter, subject grouping, leaf status, exact artifact/locator, and bounded official exam-design treatment metadata. Canonical JSON uses sorted keys, compact separators, UTF-8, deterministic source/item ordering, and SHA-256. The scope checksum therefore changes when a linked artifact checksum, hierarchy, official content, perimeter, locator, or treatment input changes.

Treatment metadata remains separate from doctrine and learner state. It may describe official weighting, emphasis, skill, or assessment-form information. It may not encode learner mastery, readiness, difficulty, AI-generation frequency, or guessed question counts.

## Validation and activation

Import validates and records a machine-readable report with `errors`, `warnings`, `info`, counts, and normalized checksum. Activation is never the default. `--activate` runs a transaction and requires a current valid report/checksum, linked artifacts, resolvable source mappings, valid same-version parents, a rooted hierarchy, nonempty testable leaves, national v1 coordinates, and no production fixture contamination. Blocking errors roll back activation and cannot supersede the current active version.

Successful activation locks the new version as `ACTIVE` and changes the previous active version to `SUPERSEDED`; all historical artifacts, links, items, checksums, and reports remain queryable. Model guards, `PROTECT` foreign keys, constraints/indexes, and PostgreSQL immutability triggers prevent casual or bulk mutation. Admin is read-only. Ordinary API clients can only authenticate and read the production active projection.

## Operator workflow

```bash
python apps/backend/manage.py import_official_scope /controlled/path/manifest.json --dry-run
python apps/backend/manage.py import_official_scope /controlled/path/manifest.json
python apps/backend/manage.py import_official_scope /controlled/path/manifest.json --activate
```

Output states artifact creation/count/hash-derived scope checksum, scope version, item/leaf counts, validation report, dry-run state, and activation state. The command performs no network access and cannot activate `TEST_FIXTURE` truth.

## M2.2 handoff

M2.2 may add the Rule Obligation/compiler layer keyed to immutable `(OfficialScopeVersion, OfficialScopeItem)` provenance. It must not mutate official scope truth, treat secondary sources as perimeter authority, or infer coverage from question counts. M2.1 does not yet solve rules/elements/factors/exceptions/limitations/defenses/remedies, doctrine graphs, authority reconciliation, omissions/excess/conflicts, certifications, assessment inventory, or AI generation.
