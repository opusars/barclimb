# Deterministic Rule Obligation Compiler

## Grammar and relationships

Canonical obligation kinds are `RULE`, `ELEMENT`, `FACTOR`, `EXCEPTION`, `LIMITATION`, `DEFENSE`, `REMEDY`, `PROCEDURAL_STEP`, `DISTINCTION`, `DEFINITION`, and `ETHICS_DUTY`. Stable identity is unique within one immutable compile version. Unicode NFKC, whitespace collapse, trim, and case-folding define deterministic statement normalization; kind plus normalized statement defines the obligation checksum.

Relations are directed and typed: `HAS_ELEMENT`, `HAS_FACTOR`, `HAS_EXCEPTION`, `HAS_LIMITATION`, `HAS_DEFENSE`, `HAS_REMEDY`, `HAS_PROCEDURAL_STEP`, `HAS_DISTINCTION`, `DEFINES`, and `HAS_ETHICS_DUTY`. Each relation constrains the target kind. Compiler validation rejects self-relations, semantic mismatches, and cycles. Many-to-many mappings connect obligations directly to M2.1 `OfficialScopeItem` leaves under the compile’s exact `OfficialScopeVersion`.

## Provenance

M2.1 artifacts remain official exam-perimeter authority. M2.2a `AuthoritySource` records represent immutable versioned substantive-primary or secondary-reconciliation evidence with citation, type, URI, classification, and content SHA-256. `AuthorityEvidence` records proposition hash, locator, role, and support direction. Secondary evidence may explain or reconcile but cannot define perimeter or satisfy a policy requiring substantive primary authority.

## Lifecycle and reports

The lifecycle is `DRAFT → COMPILED → RECONCILED → CERTIFIED → SUPERSEDED`. Compilation, reconciliation, review, and certification are explicit services. No model save certifies truth. Identical manifests and compiler versions are idempotent; conflicting input under an existing version identity fails.

Reconciliation categories are omission, excess, conflict, ambiguity, duplicate, unsupported provenance, invalid structure, and unsupported jurisdiction. Each issue has blocking, warning, or informational severity and open/resolved state. The report counts official granular leaves, mapped leaves, fixture-policy-sufficient leaves, omissions, excess, conflicts, ambiguities, provenance deficiencies, and severity totals.

`CoveragePolicy` is immutable and versioned. The fixture policy demonstrates minimum qualifying obligations, allowed kinds, and primary-authority requirements; it is not a production completeness claim. Real-source policy requires later subject/legal review and may demand richer kind-specific conditions.

## Decision and review boundary

`AUTO_APPROVABLE` means exact valid mapping, supported kind, complete required provenance, and no deterministic conflict/ambiguity signal. `REVIEW_REQUIRED` targets ambiguity, conflict, deficient provenance, or explicit risk signals. `BLOCKED` covers unsupported jurisdiction/structure. These are deterministic policy outcomes, not probabilistic or AI confidence.

Staff-only review records the triggering issue, resolution, reviewer identity, timestamp, rationale, and whether canonical truth changes. A resolution must be followed by reconciliation before certification so snapshot counts cannot become stale. Future sampled subject QA can use this boundary without making every clean obligation manually approved.

## Certification and history

Certification refuses open blocking omissions, conflicts, jurisdiction issues, invalid mappings/structure, and policy-required provenance failures. It rechecks canonical output, requires a fresh zero-blocking report, and transactionally writes an immutable snapshot covering scope/compiler/policy hashes, obligation/leaf counts, issue counts, review evidence, and certification checksum. A later certified compile can supersede—not rewrite—the previous version.

Scope drift comparison deterministically reports added, removed, and changed official items plus potentially impacted and unaffected obligations. It does not download or monitor NCBE sources. Historical compiles, mappings, evidence, reviews, and snapshots remain attributable to their original official scope version.

## Fixture and operator isolation

All M2.2a corpus text is `TEST_FIXTURE`/development-only and fictional. Fixture compiles must match fixture scope/authority classification, cannot certify through the production operator path, and are hidden from the production API. They never count toward real curriculum completeness, assessments, learner evidence/readiness, SEO, public learning, or a real release certification.

```bash
python apps/backend/manage.py compile_rule_obligations fixture.json --dry-run
python apps/backend/manage.py compile_rule_obligations fixture.json --reconcile
python apps/backend/manage.py compile_rule_obligations controlled.json --reconcile --certify
```

The command performs no acquisition/network work and reports scope/compiler versions, obligation and issue counts, eligibility, checksum, creation/dry-run state, and certification state. Mutation/review/certification are not public client APIs; Admin is inspection-only.

## M2.2b boundary

M2.2b should perform controlled acquisition and provenance registration for the real current NCBE perimeter plus a bounded real-authority pilot. It should verify licensing/public-distribution decisions, create production-classified compiler inputs, define reviewed leaf-specific completeness policy, and prove a narrow real-source reconciliation through this gate. It must not claim national completeness from M2.2a fixtures, import commercial sourcebooks as dependencies, or add OpenAI/embeddings/probabilistic extraction before deterministic real-source controls are proven.
