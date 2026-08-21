# Deterministic Rule Obligation Compiler

## Grammar and relationships

Canonical obligation kinds are `RULE`, `ELEMENT`, `FACTOR`, `EXCEPTION`, `LIMITATION`, `DEFENSE`, `REMEDY`, `PROCEDURAL_STEP`, `DISTINCTION`, `DEFINITION`, and `ETHICS_DUTY`. Stable identity is unique within one immutable compile version. Unicode NFKC, whitespace collapse, trim, and case-folding define deterministic statement normalization; kind plus normalized statement defines the obligation checksum.

Relations are directed and typed: `HAS_ELEMENT`, `HAS_FACTOR`, `HAS_EXCEPTION`, `HAS_LIMITATION`, `HAS_DEFENSE`, `HAS_REMEDY`, `HAS_PROCEDURAL_STEP`, `HAS_DISTINCTION`, `DEFINES`, and `HAS_ETHICS_DUTY`. Each relation constrains the target kind. Compiler validation rejects self-relations, semantic mismatches, and cycles. Many-to-many mappings connect obligations directly to M2.1 `OfficialScopeItem` leaves under the compile’s exact `OfficialScopeVersion`.

## Provenance

M2.1 artifacts remain official exam-perimeter authority. M2.2a `AuthoritySource` records represent immutable versioned substantive-primary or secondary-reconciliation evidence with citation, type, URI, classification, and content SHA-256. `AuthorityEvidence` records proposition hash, locator, role, and support direction. Secondary evidence may explain or reconcile but cannot define perimeter or satisfy a policy requiring substantive primary authority.

## Lifecycle and reports

The lifecycle is `DRAFT → COMPILED → RECONCILED → CERTIFIED → SUPERSEDED`. Compilation, reconciliation, review, and certification are explicit services. No model save certifies truth. Identical manifests and compiler versions are idempotent; conflicting input under an existing version identity fails.

Reconciliation categories are omission, excess, conflict, ambiguity, duplicate, unsupported provenance, invalid structure, and unsupported jurisdiction. Each issue has blocking, warning, or informational severity and open/resolved state. The report counts official granular leaves, mapped leaves, fixture-policy-sufficient leaves, omissions, excess, conflicts, ambiguities, provenance deficiencies, and severity totals.

`CoveragePolicy` is immutable and versioned. `NATIONAL` policies evaluate the full testable perimeter. `PILOT_ONLY` policies require an explicit leaf subset and cannot claim national completeness. Compiler mappings outside that subset are blocked. Reports always expose pilot class, target leaves, active-scope leaf count, and `national_complete: false`; no misleading national percentage is calculated.

## Decision and review boundary

`AUTO_APPROVABLE` means exact valid mapping, supported kind, complete required provenance, and no deterministic conflict/ambiguity signal. `REVIEW_REQUIRED` targets ambiguity, conflict, deficient provenance, or explicit risk signals. `BLOCKED` covers unsupported jurisdiction/structure. These are deterministic policy outcomes, not probabilistic or AI confidence.

Staff-only issue review records the triggering issue, resolution, reviewer identity, timestamp, rationale, and whether canonical truth changes. Production policies may additionally require an immutable `ObligationHumanReview` for every included obligation, including otherwise clean candidates. A review may be recorded by an authenticated staff reviewer or through the privileged body-free operator-manifest path for a named external human reviewer. The latter preserves the supplied name, role/qualification, decision, rationale, attestation, timestamp, and manifest hash without fabricating a BarClimb account. Certification refuses a missing, non-authority-reviewed, or rejected attestation. A resolution must be followed by reconciliation before certification so snapshot counts cannot become stale.

## Certification and history

Certification refuses open blocking omissions, conflicts, jurisdiction issues, invalid mappings/structure, and policy-required provenance failures. It rechecks canonical output, requires a fresh zero-blocking report, and transactionally writes an immutable snapshot covering scope/compiler/policy hashes, authority provenance, named review evidence, obligation/leaf counts, issue counts, and certification checksum. The snapshot ID is deterministic from the compile and review-evidence hashes; PostgreSQL rejects review and snapshot mutation. A later certified compile can supersede—not rewrite—the previous version.

Scope drift comparison deterministically reports added, removed, and changed official items plus potentially impacted and unaffected obligations. It does not download or monitor NCBE sources. Historical compiles, mappings, evidence, reviews, and snapshots remain attributable to their original official scope version.

## Fixture and operator isolation

All M2.2a corpus text is `TEST_FIXTURE`/development-only and fictional. Fixture compiles must match fixture scope/authority classification, cannot certify through the production operator path, and are hidden from the production API. They never count toward real curriculum completeness, assessments, learner evidence/readiness, SEO, public learning, or a real release certification.

```bash
python apps/backend/manage.py compile_rule_obligations fixture.json --dry-run
python apps/backend/manage.py compile_rule_obligations fixture.json --reconcile
python apps/backend/manage.py compile_rule_obligations controlled.json --reconcile --certify
python apps/backend/manage.py apply_obligation_reviews controlled-review.json --certify
```

The command performs no acquisition/network work and reports scope/compiler versions, obligation and issue counts, eligibility, checksum, creation/dry-run state, and certification state. Mutation/review/certification are not public client APIs; Admin is inspection-only.

## M2.2b real-source pilot

The first production candidate set targets only `civil-procedure-service-process-notice`. Its sole substantive authority is the official December 1, 2025 Federal Rules of Civil Procedure pamphlet from U.S. Courts, hash-pinned and supplied transiently through `--authority`. Eight manually constructed Rule 4 candidates exercise RULE, PROCEDURAL_STEP, DISTINCTION, LIMITATION, EXCEPTION, and REMEDY. The body-free manifest uses exact Rule 4 locators and no secondary authority.

Deterministic compilation and reconciliation produce zero issues and satisfy the one-leaf pilot policy. Leo Rayos supplied explicit approval for all eight V2 candidates after reviewing the hash-identified official authority. The body-free review manifest was applied through `record_obligation_review`, then the pilot was reconciled and certified. Snapshot `8ffc025a-ddac-5765-b7b2-130c84282c83` has certification SHA-256 `60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0`, remains `PILOT_ONLY`, covers one leaf, and records `national_complete: false`—never “100% NextGen complete.” The packet and immutable execution record are in `docs/project/M2_2B_HUMAN_REVIEW_PACKET.md` and `docs/project/M2_2B_CERTIFICATION_RECORD.json`.

First human review required a versioned V2 correction rather than mutation of V1 history. V2 removes two misleading procedural-step relationships from the plaintiff-responsibility rule, classifies the nonparty-adult server requirement as a `LIMITATION`, preserves the Rule 4(h) waiver addressee distinction, restores both United States location predicates and both expense categories in Rule 4(d)(2), and uses Rule 4(e)'s precise forum-state/service-state formulation. Candidates 6–8 and the valid Rule 4(m) exception/remedy relationships remain unchanged. V1's correction-required disposition is retained in `docs/project/M2_2B_HUMAN_REVIEW_PACKET_V1.md`; the distinct V2 review and certification do not rewrite it.

Negative tests reject missing primary authority, secondary-only support, jurisdiction-specific content, mappings outside the selected leaf, and conflicting candidates. Normal production APIs expose only certified production truth; fixtures, drafts, source bodies, and raw NCBE bytes remain excluded.

## M2.2c Civil Procedure completeness planning

The first subject-scale manifest is
`BARCLIMB_CIVPRO_CURRICULUM_MANIFEST@2026_V1`, checksum
`8fd6506bfc4cfda72e1ee6aaad6d62f8ab233fb1c48ff45c308e01b12b60ebd8`. It targets exact
scope `NCBE_NEXTGEN_SCOPE_2026_07_2027_02` and policy
`BARCLIMB_CIVPRO_COVERAGE_POLICY@2026_V1`. The immutable plan contains all six Civil Procedure
leaves, 18 curriculum-layer requirements, 75 typed obligation slots, 16 authority-family plans, 45
requirement/authority mappings, and five proposition-level Supreme Court case plans.

The slots make completeness noncircular. A future obligation must match the slot kind, map to the same
official leaf, pass ordinary compiler/reconciliation/authority/jurisdiction review, and link through a
certified snapshot before it may satisfy the slot. Every required slot and primary-authority mapping
must pass; a percentage, a raw obligation count, or one obligation per leaf cannot produce
`LEAF_CERTIFIED` or `SUBJECT_CERTIFIED`.

Civil Procedure becomes subject-certification eligible only after every active testable leaf is
addressed; all required slots have certified satisfactions; required primary authority is acquired and
current; omissions, conflicts, authority gaps, and unsupported jurisdiction content are zero; human
reviews are complete; reconciliation passes; and exact scope/manifest/authority/compiler/policy hashes
are captured. Eligibility still requires a future explicit certification operation. M2.2c deliberately
implements no subject snapshot or certification command.

The Rule 4 snapshot is linked as `PARTIAL_LEAF_COVERAGE`, not decomposed or recertified. It establishes
known certified evidence within `civil-procedure-service-process-notice` but satisfies no proposed
subject slot without a later reviewed mapping. Every other leaf is `AUTHORITY_PLANNED`; the service leaf
is `PARTIALLY_COVERED`; all remain uncovered for subject-certification purposes.

Operator workflows:

```bash
python apps/backend/manage.py import_subject_plan \
  apps/backend/curriculum/manifests/civil-procedure-subject-plan-2026-v1.json
python apps/backend/manage.py report_subject_coverage \
  BARCLIMB_CIVPRO_CURRICULUM_MANIFEST@2026_V1
python apps/backend/manage.py record_subject_plan_review /controlled/review.json
```

The import requires the accepted active scope, acquired FRCP authority, and immutable Rule 4 snapshot
to exist. It is deterministic and idempotent. Reporting is read-only and exposes planning/provenance
metadata only. Review records exact external-human evidence through a privileged operator path and
does not create or certify substantive obligations.
