# Official Source Registry and National NextGen Scope

## Authority and lifecycle

Only controlling official perimeter artifacts belong in the production registry. The current product coordinates are exactly `NEXTGEN_UBE` and `NEXTGEN_CORE`; v1 has no jurisdiction field value or active state component. Secondary references may later attach reconciliation evidence, but they do not define this perimeter and are not M2.1 dependencies.

Artifact acquisition/download is outside Django. V1 manifests retain embedded bytes only for synthetic fixtures. Production operators use `BARCLIMB_OFFICIAL_SCOPE_IMPORT_V2` plus one `--artifact STABLE_ID=/controlled/path` argument per source. The operator command hashes those bytes before parsing and compares them with the committed expected SHA-256. It performs no network request and refuses missing, changed, or silently replaced bytes. The `(stable_id, source_version)` identity is immutable: identical input returns the existing row; changed bytes or identity metadata requires a new version.

M2.2b's current production descriptor registers the NCBE Content Scope and Blueprint for July 2026–February 2027. The acquired PDFs remain transient. NCBE's copyright notices and website terms do not clearly authorize repository redistribution, so Git and APIs retain only canonical URI, exact title/version/dates, retrieval time, hash, byte length, media type, rights/storage decision, short factual perimeter labels, and narrow locators.

## Scope normalization

A manifest links any number of artifacts to a scope version with explicit roles. Its item list retains only source-supported hierarchy levels and provides stable item identity, parent identity, label/text, order, perimeter, subject grouping, leaf status, exact artifact/locator, and bounded official exam-design treatment metadata. Canonical JSON uses sorted keys, compact separators, UTF-8, deterministic source/item ordering, and SHA-256. The scope checksum therefore changes when a linked artifact checksum, hierarchy, official content, perimeter, locator, or treatment input changes.

Treatment metadata remains separate from doctrine and learner state. Each leaf now has an explicit knowledge-treatment classification: recalled knowledge required, may be tested with or without resources, resources always provided, foundational skill, exam-design metadata, or an aggregate containing mixed official markers. Family law and trusts and estates are context domains with supplied legal resources through February 2028; they are not current recalled-knowledge `NEXTGEN_CORE` doctrine. The announced July 2028 family-law transition is future truth and cannot be activated early.

## Validation and activation

Import validates and records a machine-readable report with `errors`, `warnings`, `info`, counts, and normalized checksum. Activation is never the default. `--activate` runs a transaction and requires a current valid report/checksum, linked artifacts, resolvable source mappings, valid same-version parents, a rooted hierarchy, nonempty testable leaves, national v1 coordinates, and no production fixture contamination. Blocking errors roll back activation and cannot supersede the current active version.

Successful activation locks the new version as `ACTIVE` and changes the previous active version to `SUPERSEDED`; all historical artifacts, links, items, checksums, and reports remain queryable. A future-classified version may coexist but activation refuses it. Production versions require explicit administration dates, a freshness timestamp, treatment classification on every leaf, and no blocking normalization status. Model guards, `PROTECT` foreign keys, constraints/indexes, and PostgreSQL immutability triggers prevent casual or bulk mutation. Admin is read-only. Ordinary API clients can only authenticate and read the production active projection; source bodies and internal rights notes are never serialized.

## Operator workflow

```bash
python apps/backend/manage.py import_official_scope apps/backend/official_scope/manifests/ncbe-nextgen-2026-07.json \
  --artifact NCBE_NEXTGEN_CONTENT_SCOPE=/controlled/content-scope.pdf \
  --artifact NCBE_NEXTGEN_BLUEPRINT=/controlled/blueprint.pdf \
  --dry-run
# Repeat without --dry-run, then repeat with --activate after reviewing validation output.
```

Output states artifact creation/count/hash-derived scope checksum, scope version, item/leaf counts, validation report, dry-run state, and activation state. The command performs no network access and cannot activate `TEST_FIXTURE` truth.

Before any release certification, an operator must revisit the official NCBE content-scope page, reacquire the applicable administration-period artifacts, compare hashes and dates, and create a new immutable version if they changed. The current version cannot be assumed current indefinitely. Production drift awaits a second genuine comparable official version; synthetic fixtures are never treated as its predecessor.

## M2.2b boundary

The production normalization contains 32 auditable items and 26 leaves, including 20 current testable aggregate/skill leaves. It preserves the official perimeter and treatment boundaries without copying NCBE prose or inventing BarClimb doctrinal leaves. It is not proof that all detailed NCBE subtopics have Rule Obligations. Only `civil-procedure-service-process-notice` is selected for the M2.2b curriculum pilot.
