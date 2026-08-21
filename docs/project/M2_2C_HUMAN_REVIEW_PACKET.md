# M2.2c Civil Procedure Coverage-Plan Human Review Packet

Status: **REVIEW PENDING — NOT APPROVED — NOT SUBJECT CERTIFIED**

This packet asks a qualified human reviewer to assess the proposed Civil Procedure scope
decomposition, structural completeness requirements, treatment distinctions, and primary-authority
acquisition plan. It does not ask the reviewer to approve substantive Rule Obligation statements.
M2.2c creates none. The eight previously reviewed Rule 4 V2 obligations remain the only certified
production subset and are not reopened by this review.

## Immutable inputs and boundary

- Official scope: `NCBE_NEXTGEN_SCOPE_2026_07_2027_02`
- Official scope SHA-256: `2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f`
- Administration period: July 2026 through February 2027
- Subject manifest: `BARCLIMB_CIVPRO_CURRICULUM_MANIFEST@2026_V1`
- Subject-manifest SHA-256: `8fd6506bfc4cfda72e1ee6aaad6d62f8ab233fb1c48ff45c308e01b12b60ebd8`
- Coverage policy: `BARCLIMB_CIVPRO_COVERAGE_POLICY@2026_V1`
- Certification gate: `BARCLIMB_SUBJECT_CERTIFICATION_GATE_V1`
- Existing pilot compile: `BARCLIMB_PILOT_FRCP_RULE4_2025_V2`
- Existing snapshot: `8ffc025a-ddac-5765-b7b2-130c84282c83` (`PILOT_ONLY`)
- Existing compile SHA-256: `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`
- Existing certification SHA-256: `60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0`

Official NCBE PDF bytes remain transient and are not reproduced here. Short factual labels and exact
locators below come from the accepted immutable scope descriptor. Review against the hash-identified
official source where exact subtopic/star-marker interpretation matters.

## Proposed leaf inventory and decomposition

The current official scope contains exactly six active testable Civil Procedure leaves. The
`ScopeCoverageRequirement` rows below are curriculum-layer planning requirements, not edits to NCBE
truth and not substantive legal propositions.

### `civil-procedure-jurisdiction`

- Official label: **Jurisdiction and related court authority**
- NCBE locator: p. 11, I.A–B
- Treatment: `MIXED_OFFICIAL_MARKERS`
- Proposed requirements:
  - `civpro-jurisdiction-subject-matter` — subject-matter jurisdiction and court authority;
    required kinds: `RULE`, `ELEMENT`, `LIMITATION`.
  - `civpro-jurisdiction-personal` — personal jurisdiction and constitutional limits; required
    kinds: `RULE`, `FACTOR`, `LIMITATION`, `DISTINCTION`.
  - `civpro-jurisdiction-removal-supplemental` — removal, remand, and supplemental jurisdiction;
    required kinds: `RULE`, `PROCEDURAL_STEP`, `EXCEPTION`, `REMEDY`.
- Required authority families: Article III; Due Process Clauses as applicable; current Title 28
  jurisdiction/removal provisions; current FRCP provisions where applicable; controlling Supreme
  Court proposition-level authority.
- Reviewer judgment: confirm the three proposed subareas neither omit nor overstate the exact I.A–B
  perimeter, and confirm mixed treatment is later assigned at the candidate/subtopic level rather
  than flattened into a blanket recall requirement.

### `civil-procedure-service-process-notice`

- Official label: **Service of process and notice**
- NCBE locator: p. 11, I.C
- Treatment: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Proposed requirements:
  - `civpro-service-issuance-and-methods` — issuance, service responsibility, permitted methods,
    and waiver; required kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`, `LIMITATION`.
  - `civpro-service-timing-and-consequences` — timing, extensions, and consequences; required
    kinds: `LIMITATION`, `EXCEPTION`, `REMEDY`.
  - `civpro-notice-constitutional-sufficiency` — constitutional sufficiency of notice; required
    kinds: `RULE`, `FACTOR`, `LIMITATION`.
- Required authority families: current FRCP; Due Process Clauses; controlling Supreme Court notice
  authority.
- Existing evidence: the immutable Rule 4 V2 snapshot contributes partial historical coverage to
  this leaf. Its eight obligations do not satisfy all proposed slots and do not establish complete
  Rule 4, complete notice doctrine, or complete leaf coverage.
- Reviewer judgment: confirm the recognition/resource split is responsible and does not convert
  unstarred recognition into unsupported memorization.

### `civil-procedure-venue-transfer`

- Official label: **Venue, forum non conveniens, and transfer**
- NCBE locator: p. 11, I.D
- Treatment: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Proposed requirements:
  - `civpro-venue-selection` — federal venue selection; required kinds: `RULE`, `ELEMENT`,
    `LIMITATION`.
  - `civpro-venue-transfer-dismissal` — transfer, cure, and forum non conveniens; required kinds:
    `RULE`, `FACTOR`, `PROCEDURAL_STEP`, `REMEDY`, `DISTINCTION`.
- Required authority families: current Title 28 venue/transfer provisions and controlling Supreme
  Court authority where operative doctrine cannot be responsibly established by statute alone.
- Reviewer judgment: confirm the distinction among venue selection, statutory transfer/cure, and
  forum non conveniens is required by the official leaf without creating state-specific doctrine.

### `civil-procedure-litigation`

- Official label: **Law applied by federal courts and pretrial litigation**
- NCBE locator: pp. 11–12, II–III
- Treatment: `MIXED_OFFICIAL_MARKERS`
- Proposed requirements:
  - `civpro-erie-hanna-cluster` — Erie/Hanna multi-authority cluster; required kinds: `RULE`,
    `ELEMENT`, `DISTINCTION`, `LIMITATION`.
  - `civpro-pleading-and-responsive-motions` — pleading standards, responsive pleadings, and
    pleading motions; required kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `DEFENSE`, `LIMITATION`.
  - `civpro-joinder-and-party-structure` — claim/party joinder and related structure; required
    kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`, `DISTINCTION`.
  - `civpro-discovery-and-disclosure` — disclosure, discovery scope/procedure, protection, and
    sanctions; required kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`, `DEFENSE`, `REMEDY`.
  - `civpro-pretrial-disposition` — pretrial disposition and summary adjudication; required kinds:
    `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`.
- Required authority families: current FRCP; Article III where applicable; Rules of Decision Act;
  Rules Enabling Act; current jurisdiction statutes where applicable; controlling Supreme Court
  holdings; optional secondary evidence for reconciliation only.
- Multi-authority proof: `civpro-erie-hanna-cluster` requires constitutional, statutory,
  rule-enabling, applicable FRCP, and controlling Supreme Court proposition types. A single generic
  Rule Obligation cannot satisfy it.
- National-core boundary: federal doctrine that directs incorporation or comparison of state law is
  nationally testable federal doctrine. Actual California, New York, or other state-specific
  procedural rules remain prohibited from `NEXTGEN_CORE` except as exact primary-source facts used
  only when a federal rule itself makes the comparison relevant.
- Reviewer judgment: confirm the five subareas match the official II–III perimeter; identify any
  missing or overbroad subarea; confirm the proposed Erie/Hanna authority cluster and the national
  federal/state distinction.

### `civil-procedure-motions-judgments`

- Official label: **Motions, verdicts, and judgments**
- NCBE locator: p. 13, IV–V
- Treatment: `MIXED_OFFICIAL_MARKERS`
- Proposed requirements:
  - `civpro-jury-verdict` — jury trial, verdicts, and judgment as a matter of law; required kinds:
    `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`.
  - `civpro-posttrial-relief` — posttrial motions and relief from judgment; required kinds: `RULE`,
    `ELEMENT`, `LIMITATION`, `PROCEDURAL_STEP`, `REMEDY`.
  - `civpro-preclusion` — claim and issue preclusion; required kinds: `RULE`, `ELEMENT`,
    `EXCEPTION`, `DISTINCTION`.
- Required authority families: Seventh Amendment where applicable; current FRCP; related current
  federal statutes where applicable; controlling Supreme Court proposition-level authority;
  optional secondary reconciliation evidence for preclusion only.
- Reviewer judgment: confirm preclusion belongs in this official grouping, and confirm that jury,
  motion, verdict, and judgment requirements are neither collapsed nor expanded beyond the source.

### `civil-procedure-appeals`

- Official label: **Appellate review**
- NCBE locator: p. 13, VI
- Treatment: `MIXED_OFFICIAL_MARKERS`
- Proposed requirements:
  - `civpro-appellate-jurisdiction` — final-judgment and interlocutory appellate jurisdiction;
    required kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `DISTINCTION`.
  - `civpro-appellate-procedure-review` — appellate procedure, preservation, and standards of
    review; required kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`, `DISTINCTION`, `REMEDY`.
- Required authority families: current Title 28 appellate-jurisdiction provisions; FRAP only where
  genuinely required by the official perimeter; controlling Supreme Court authority; optional
  secondary reconciliation evidence.
- Reviewer judgment: confirm FRAP is a genuinely required primary family for the imported appellate
  leaf and that preservation/remedy slots do not overstate the official perimeter.

## Authority and freshness architecture to review

The plan contains 16 authority families: three constitutional plans, five Title 28/Rules Enabling
Act statutory plans, current FRCP, current FRAP, five Supreme Court case-authority plans, and one
optional secondary-reconciliation plan. Only the already hash-pinned December 1, 2025 FRCP source is
currently marked `ACQUIRED`; 15 remain `PLANNED`.

Each primary plan records its official source family, hierarchy, version/effective-date requirement,
freshness check, and deterministic drift action. The five case-law plans additionally require exact
case identity/citation, court, decision date, reliable source URI, proposition locator, authority
status, and later-treatment review. Optional secondary evidence is structurally prohibited from
serving as required primary authority.

## Objective certification gate

Future `SUBJECT_CERTIFIED` requires all of the following, not a percentage or one obligation per
leaf:

1. Every active testable Civil Procedure leaf is addressed.
2. Every typed requirement slot is satisfied by appropriately mapped certified obligations.
3. Required primary authority is acquired, current, and proposition-linked.
4. No blocking omission, substantive conflict, unsupported jurisdiction content, or authority gap
   remains.
5. All required human reviews are complete.
6. Deterministic reconciliation passes.
7. Exact scope, manifest, authority, compiler, and policy checksums are captured.
8. A separate explicit subject-certification operation occurs.

M2.2c has 18 proposed requirements and 75 structural slots. Zero slots are presently recorded as
certified. The report therefore returns `subject_complete: false` and `national_complete: false`.

## Review decisions requested

For each leaf and proposed requirement, record `APPROVE`, `REJECT`, or a precise required revision.
Please specifically address:

1. Whether the proposed decomposition is complete without exceeding the official NCBE perimeter.
2. Whether the typed obligation slots are doctrinally appropriate and avoid artificial uniformity.
3. Whether authority families are required/conditional/optional in the right places.
4. Whether the five case-law plans cover every area that cannot responsibly rely only on text.
5. Whether treatment distinctions respect exact official star/resource markers.
6. Whether the Erie/Hanna and federal/state boundary is correctly national and provider-neutral.
7. Whether FRAP, preclusion, removal/supplemental jurisdiction, and other potentially ambiguous
   placements match the exact imported scope.
8. Whether any planning requirement should be split, combined, renamed, or removed before candidate
   compilation begins.

## Attestation boundary

A future review record must identify the reviewer and qualification, the exact packet SHA-256,
resolution, rationale, attestation, and review time through `record_subject_plan_review`. Approval is
approval of this coverage plan only. It is not approval of substantive candidate statements, complete
Civil Procedure doctrine, any other subject, assessment inventory, learner mastery/readiness, or
national NextGen curriculum completeness.
