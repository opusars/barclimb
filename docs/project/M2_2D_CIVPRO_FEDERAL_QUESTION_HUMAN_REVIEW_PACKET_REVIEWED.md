# M2.2d Civil Procedure Federal-Question Candidate Review Packet

**HUMAN REVIEW PENDING — CANDIDATES NOT APPROVED — TOPIC NOT CERTIFIED — SUBJECT NOT CERTIFIED**

This packet presents one bounded candidate cluster for qualified substantive review. It does not
record reviewer identity or disposition, approve any candidate, certify the topic or subject, or
expand the approved M2.2c V3 coverage plan.

## Compile identity and boundary

- Accepted-main starting SHA: `e7b1517dc0a048ecf4b102306dd0e9e86f2401f8`
- Working branch: `m2-2d-civpro-federal-question`
- Compiler schema: `BARCLIMB_RULE_COMPILER_V2`
- Compile/version ID: `BARCLIMB_CIVPRO_FEDERAL_QUESTION_2026_V1`
- Input-manifest SHA-256: `238b15e7b5bfc492ebb5dde77a88c09b09a4bafd463f772c3cbe24277fb03f4f`
- Candidate compile SHA-256: `a46fbd51a441ec54fa74f2826a50241ff94e4fd3eefa49e24e568174d15b606d`
- Source class: `PRODUCTION`
- Coverage classification: `PILOT_ONLY`
- Official scope: `NCBE_NEXTGEN_SCOPE_2026_07_2027_02`
- Exact official topic: `civpro-topic-federal-question-jurisdiction` — Federal question
  jurisdiction, p. 11, I.A.1
- Official hierarchy: `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` →
  `civpro-subsection-i-a-federal-subject-matter` →
  `civpro-topic-federal-question-jurisdiction`
- Official marker/treatment: `STARRED` / `RECALLED_REQUIRED`
- Nonauthoritative planning aggregate: `civil-procedure-jurisdiction`

This cluster excludes diversity, supplemental jurisdiction, removal/remand, concurrent
jurisdiction, personal jurisdiction, Erie, venue, complete preemption, artful pleading,
declaratory-judgment jurisdiction, and embedded/substantial-federal-issue doctrine. No candidate
in this packet may satisfy another topic or requirement.

## Approved V3 requirement and completeness structure

The controlling approved requirement is `civpro-federal-question`: “Federal-question
jurisdiction, including the well-pleaded-complaint and arising-under boundaries.” It is a
`GOVERNING_RULE`, inherits `RECALL` treatment, is required for subject completeness, requires
human review, and permits only `RULE`, `ELEMENT`, and `LIMITATION` candidates.

The exact required typed slots are:

| Slot | Required kind | Minimum | Required relationship |
|---|---|---:|---|
| `civpro-federal-question-rule` | `RULE` | 1 | Governing source |
| `civpro-federal-question-element` | `ELEMENT` | 1 | Rule → `HAS_ELEMENT` |
| `civpro-federal-question-limitation` | `LIMITATION` | 1 | Rule → `HAS_LIMITATION` |

The approved authority mappings are:

| Role | Authority plan | Proposition tag | Condition |
|---|---|---|---|
| `REQUIRED` | `authority-28-usc-jurisdiction-removal` | `GOVERNING_STATUTORY_TEXT` | None |
| `REQUIRED` | `authority-scotus-jurisdiction` | `WELL_PLEADED_COMPLAINT_CONTROLLING_HOLDING` | None |
| `CONDITIONAL` | `authority-us-constitution-article-iii` | `CONSTITUTIONAL_BOUNDARY` | Only if a candidate distinguishes constitutional judicial power from statutory jurisdiction |

No candidate makes the conditional constitutional/statutory-boundary proposition. Article III
was therefore neither required nor acquired. The cluster does not use statutory text alone to
support the well-pleaded-complaint holding.

## Controlled primary-authority acquisition

Raw source bytes were used transiently to verify hashes and compile provenance. They are not
committed. The committed descriptor contains only metadata, locators, and cryptographic hashes.

### 28 U.S.C. § 1331

- Authority ID: `USCODE_28_USC_1331`
- Class/type: `SUBSTANTIVE_PRIMARY` / `UNITED_STATES_CODE`
- Citation: 28 U.S.C. § 1331
- Issuer: Office of the Law Revision Counsel, U.S. House of Representatives
- Official source: `https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid%3AUSC-prelim-title28-section1331`
- Source version: `PRELIM_LAWS_IN_EFFECT_2026-09-01`
- Effective-state metadata: current preliminary U.S. Code text, laws in effect September 1, 2026;
  section effective date recorded as December 1, 1980
- Retrieved: `2026-09-02T22:10:00Z`
- Media type/size: `application/xhtml+xml`; 150,606 bytes
- Exact source SHA-256: `f1a418156a2be3117aa698c83788ff6b544d68c602bb4559d06cc2daa2129ac7`
- Proposition locator: 28 U.S.C. § 1331; official House preliminary text in effect September 1,
  2026
- Proposition tag: `GOVERNING_STATUTORY_TEXT`
- Storage disposition: `TRANSIENT_HASH_ONLY`

### Louisville & Nashville Railroad Co. v. Mottley

- Authority ID: `SCOTUS_US_REPORTS_MOTTLEY_211_US_149`
- Class/type: `SUBSTANTIVE_PRIMARY` / `UNITED_STATES_SUPREME_COURT_OPINION`
- Citation: 211 U.S. 149 (1908)
- Issuer: Supreme Court of the United States; official U.S. Reports scan supplied by the Library
  of Congress
- Official source: `https://tile.loc.gov/storage-services/service/ll/usrep/usrep211/usrep211149/usrep211149.pdf`
- Source version/publication date: `1908-11-16`
- Retrieved: `2026-09-02T22:10:00Z`
- Media type/size: `application/pdf`; 207,960 bytes
- Exact source SHA-256: `73c4f2d4ada6a12b94106e045533c9b835a492cba9475f09de4da267341978ec`
- Proposition locator: 211 U.S. 149, 152–53 (1908); official U.S. Reports PDF pp. 4–5
- Proposition tag: `WELL_PLEADED_COMPLAINT_CONTROLLING_HOLDING`
- Storage disposition: `TRANSIENT_HASH_ONLY`

Mottley is the only case acquired. It is the smallest controlling primary-authority set needed for
the approved element and limitation slots. Rivet, Grable, Gunn, and other case lines were not
acquired because this cluster asserts neither removal/complete-preemption doctrine nor the
state-law substantial-federal-issue pathway.

## Candidate Rule Obligations

All candidates are compiler-included, deterministically reconciled, marked `REVIEW_REQUIRED`, and
have no human-review record. “Reconciled” below means only that the deterministic checks found no
open issue; it is not substantive approval or certification.

### 1. `civpro-fq-statutory-original-jurisdiction`

- Kind: `RULE`
- Exact statement: “Under 28 U.S.C. § 1331, federal district courts have original jurisdiction over
  civil actions arising under the Constitution, laws, or treaties of the United States.”
- Exact proposition asserted: Federal district courts have original jurisdiction over civil
  actions arising under the Constitution, laws, or treaties of the United States.
- Topic: `civpro-topic-federal-question-jurisdiction`
- Requirement/slot: `civpro-federal-question` /
  `civpro-federal-question-rule`
- Inherited treatment: `RECALLED_REQUIRED`
- Authority: `USCODE_28_USC_1331`; 28 U.S.C. § 1331; official House preliminary text in effect
  September 1, 2026; `GOVERNING_STATUTORY_TEXT`
- Relationship source: `HAS_ELEMENT` to
  `civpro-fq-plaintiff-claim-arising-under`; `HAS_LIMITATION` to
  `civpro-fq-federal-defense-limitation`
- Compiler/reconciliation state: `INCLUDED`; `REVIEW_REQUIRED`; `RECONCILED`; human review
  `PENDING`

### 2. `civpro-fq-plaintiff-claim-arising-under`

- Kind: `ELEMENT`
- Exact statement: “For a civil action to arise under federal law, the plaintiff’s properly pleaded
  statement of the plaintiff’s own cause of action must show that the cause is based on federal
  law.”
- Exact proposition asserted: The plaintiff’s statement of the plaintiff’s own cause of action must
  show that the cause is based on federal law.
- Topic: `civpro-topic-federal-question-jurisdiction`
- Requirement/slot: `civpro-federal-question` /
  `civpro-federal-question-element`
- Inherited treatment: `RECALLED_REQUIRED`
- Authority: `SCOTUS_US_REPORTS_MOTTLEY_211_US_149`; 211 U.S. 149, 152 (1908), official U.S.
  Reports PDF p. 4; `WELL_PLEADED_COMPLAINT_CONTROLLING_HOLDING`
- Relationship: target of governing rule → `HAS_ELEMENT`
- Compiler/reconciliation state: `INCLUDED`; `REVIEW_REQUIRED`; `RECONCILED`; human review
  `PENDING`

### 3. `civpro-fq-federal-defense-limitation`

- Kind: `LIMITATION`
- Exact statement: “Federal-question jurisdiction cannot rest solely on a federal defense,
  including a defense anticipated in the plaintiff’s complaint.”
- Exact proposition asserted: Federal-question jurisdiction cannot be based on an anticipated
  federal defense.
- Topic: `civpro-topic-federal-question-jurisdiction`
- Requirement/slot: `civpro-federal-question` /
  `civpro-federal-question-limitation`
- Inherited treatment: `RECALLED_REQUIRED`
- Authority: `SCOTUS_US_REPORTS_MOTTLEY_211_US_149`; 211 U.S. 149, 152–53 (1908), official U.S.
  Reports PDF pp. 4–5; `WELL_PLEADED_COMPLAINT_CONTROLLING_HOLDING`
- Relationship: target of governing rule → `HAS_LIMITATION`
- Compiler/reconciliation state: `INCLUDED`; `REVIEW_REQUIRED`; `RECONCILED`; human review
  `PENDING`

## Deterministic reconciliation

The exact-byte compile and reconciliation produced:

| Check | Count/status |
|---|---:|
| Candidate obligations | 3 |
| Required slots with one qualifying candidate | 3 of 3 |
| Omission | 0 |
| Excess | 0 |
| Unsupported provenance | 0 |
| Conflict | 0 |
| Ambiguity | 0 |
| Invalid structure | 0 |
| Duplicate included candidate | 0 |
| Jurisdiction contamination | 0 |
| Open blocking issues | 0 |
| Open warnings | 0 |
| Required human reviews pending | 3 |
| Certification eligible | `false` |
| Candidate human-review status | `PENDING` |
| Topic/subject certification | `false` / `false` |

Focused negative cases independently prove that omission, excess, unsupported provenance,
conflict, duplicate, invalid structure, incorrect topic placement, and jurisdiction contamination
remain detectable blockers or findings as classified. The statute-only negative case cannot satisfy
the controlling well-pleaded-complaint authority requirement.

## Authority-plan and completeness state

- Before this slice: 22 authority plans — 1 `ACQUIRED`, 21 `PLANNED`.
- After exact requirement-specific acquisition: 22 authority plans — 1 `ACQUIRED`, 2
  `PARTIALLY_ACQUIRED`, 19 `PLANNED`.
- The two partial plans are `authority-28-usc-jurisdiction-removal` and
  `authority-scotus-jurisdiction`. Each is shared with other requirements, so satisfying only this
  requirement does not mark the whole family acquired.
- `authority-us-constitution-article-iii` remains `PLANNED` and was not acquired.
- This candidate cluster fills all three federal-question candidate slots for review. None is
  human-approved or certified, so none counts as a certified subject-completeness slot.
- The other 146 V3 typed slots are outside this cluster and received no candidate from this slice.
- Certified V3 slots remain 0 of 149.
- `subject_complete`: `false`
- `subject_certified`: `false`
- `national_complete`: `false`

## Preserved accepted evidence

- M2.2c V3 plan review: `APPROVE — COVERAGE PLAN ACCEPTED`
- M2.2c immutable review-manifest SHA-256:
  `6ceea17f91c7523c993a25a702b6e7ab923117d8a918baa7ed916d57bac87c97`
- Civil Procedure invariants: 27 official terminal topics; 14 starred; 13 unstarred; six
  nonauthoritative planning aggregates; 43 requirements; 149 typed slots.
- Rule 4 compile SHA-256:
  `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`
- Rule 4 snapshot ID: `8ffc025a-ddac-5765-b7b2-130c84282c83`
- Rule 4 certification SHA-256:
  `60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0`

The historical Rule 4 pilot and its human-review evidence were not mutated.

## Questions for the qualified substantive reviewer

For each candidate, record an independent `APPROVE` or `REJECT` decision through the existing
obligation-review workflow and explain any rejection. In particular:

1. Does the `RULE` statement accurately and atomically state the current § 1331 jurisdictional
   grant without implying broader constitutional or removal doctrine?
2. Does the `ELEMENT` statement accurately express Mottley’s plaintiff-claim/properly-pleaded
   boundary, and is “based on federal law” sufficiently precise for this bounded obligation?
3. Does the `LIMITATION` statement accurately express that an actual or anticipated federal
   defense alone does not create federal-question jurisdiction, without importing removal or
   complete-preemption doctrine?
4. Are the statute and Mottley locators adequate and proposition-specific for each statement?
5. Are the `RULE` → `HAS_ELEMENT` and `RULE` → `HAS_LIMITATION` relationships substantively
   correct?
6. Does the three-candidate set satisfy exactly the approved federal-question typed slots without
   doctrinal leakage or an omitted proposition required by the approved V3 requirement?

Approval, if later supplied and validly recorded, must be bounded to these exact three candidates
and sources. It would not approve another federal-question doctrine, another Civil Procedure
topic, the Civil Procedure subject, any assessment inventory, learner mastery/readiness truth, or
national NextGen curriculum completeness. No certification action is part of this review packet.

**HUMAN REVIEW PENDING — CANDIDATES NOT APPROVED — TOPIC NOT CERTIFIED — SUBJECT NOT CERTIFIED**
