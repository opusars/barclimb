# M2.2c Civil Procedure Coverage-Plan Human Review Packet — V2

Status: **SECOND REVIEW PENDING — NOT APPROVED — NOT SUBJECT CERTIFIED**

This packet asks a qualified human reviewer to assess the corrected Civil Procedure official-topic normalization, curriculum decomposition, treatment fidelity, typed completeness requirements, and requirement-level authority plan. It does not ask for approval of substantive Rule Obligation statements. M2.2c V2 creates none.

Official source bytes remain transient and are not reproduced. The short factual topic labels, hierarchy identifiers, locators, and star classifications below were normalized from the accepted hash-identified NCBE source.

## Immutable inputs and review history

- Official scope: `NCBE_NEXTGEN_SCOPE_2026_07_2027_02`
- Official scope SHA-256: `2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f`
- Official source artifact: `NCBE_NEXTGEN_CONTENT_SCOPE@2025-08_JUL2026-FEB2027`
- Official source PDF SHA-256: `22aa277048c04fdd887db66284c28bade9989b9f8a654fab05781bafa5b19b1a`
- Administration period: July 2026 through February 2027
- Active subject manifest: `BARCLIMB_CIVPRO_CURRICULUM_MANIFEST@2026_V2`
- Active subject-manifest SHA-256: `ff98c996ac55135b6e7c0dc6410cac4be965a1c7f482a9c8cc6aff7a9b7cba20`
- Coverage policy: `BARCLIMB_CIVPRO_COVERAGE_POLICY@2026_V2`
- Certification gate: `BARCLIMB_SUBJECT_CERTIFICATION_GATE_V2`
- V1 packet: `M2_2C_HUMAN_REVIEW_PACKET_V1.md`, SHA-256 `153746608c27abad008dbfa5cd858113c746696ed05fc410a1b6242e558b1f6c`
- V1 disposition: **REJECT — REVISION REQUIRED**
- V1 reviewer identity/qualification: not supplied in repository-controlled input; no formal workflow attestation was fabricated.
- Existing Rule 4 compile: `BARCLIMB_PILOT_FRCP_RULE4_2025_V2`
- Existing Rule 4 snapshot: `8ffc025a-ddac-5765-b7b2-130c84282c83` (`PILOT_ONLY`)
- Existing compile SHA-256: `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`
- Existing certification SHA-256: `60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0`

## Changes from rejected V1

1. The six coarse accepted scope items are now explicitly BarClimb planning aggregates, never terminal completeness units.
2. Twenty-seven official terminal topics are represented individually with exact source hierarchy, locator, marker, treatment, and effective-period binding.
3. Supplemental jurisdiction and concurrent/removal jurisdiction remain separate; concurrent jurisdiction is explicit; personal jurisdiction is decomposed without flattening.
4. Rule 4(m) timing remains valid historical pilot evidence but is supplemental and not required for official-perimeter completeness.
5. Venue selection, improper-venue cure, transfer, and forum non conveniens are separate planning requirements.
6. Erie/Hanna authority is branch-dependent; no candidate must cite every constitutional, statutory, rule, and case family at once.
7. TRO/preliminary injunctions and Rule 11 are explicit. Pleadings, joinder, intervention, discovery, and e-discovery follow terminal-topic treatment.
8. Rule 12, judgment on the pleadings, summary judgment, and JMOL are separate dispositive-motion topics. Summary judgment is not pretrial-disposition coverage.
9. Jury preservation is separate from JMOL. Default/default judgment and claim/issue preclusion are explicit. Rule 59/60-style posttrial relief is not required.
10. Appeals are limited to final judgment, interlocutory review, and standards of review. FRAP is conditional, not a blanket completeness dependency.

## Operative treatment interpretation

- `STARRED` / `RECALLED_REQUIRED`: the topic requires recalled knowledge and understanding without supplied legal resources.
- `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`: the topic may be tested with or without resources; without resources, recalled understanding must be sufficient to recognize that the topic is at issue.
- Aggregate `MIXED_OFFICIAL_MARKERS` is display metadata only. It cannot govern candidate treatment or establish completeness.
- V2 contains 14 starred terminal topics and 13 unstarred terminal topics.

## Six BarClimb planning aggregates — not official terminal leaves

| Accepted coarse scope item | Display label | Locator | Aggregate treatment | Terminal topics |
|---|---|---|---|---:|
| `civil-procedure-jurisdiction` | Jurisdiction and related court authority | p. 11, I.A–B | `MIXED_OFFICIAL_MARKERS` | 5 |
| `civil-procedure-service-process-notice` | Service of process and notice | p. 11, I.C | `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | 1 |
| `civil-procedure-venue-transfer` | Venue, forum non conveniens, and transfer | p. 11, I.D | `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | 1 |
| `civil-procedure-litigation` | Law applied by federal courts and pretrial litigation | pp. 11–12, II–III | `MIXED_OFFICIAL_MARKERS` | 10 |
| `civil-procedure-motions-judgments` | Motions, verdicts, and judgments | p. 13, IV–V | `MIXED_OFFICIAL_MARKERS` | 7 |
| `civil-procedure-appeals` | Appellate review | p. 13, VI | `MIXED_OFFICIAL_MARKERS` | 3 |

Completeness is computed over the 27 terminal topics and their required slots. A six-group rollup, percentage, one obligation per group, or the Rule 4 pilot cannot establish subject completeness.

## Exact official terminal-topic inventory

| # | Stable topic ID | Exact parent hierarchy | Official label | Locator | Marker / treatment | Planning aggregate |
|---:|---|---|---|---|---|---|
| 1 | `civpro-topic-federal-question-jurisdiction` | `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-subsection-i-a-federal-subject-matter` → `civpro-topic-federal-question-jurisdiction` | Federal question jurisdiction | p. 11, I.A.1 | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-jurisdiction` |
| 2 | `civpro-topic-diversity-jurisdiction` | `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-subsection-i-a-federal-subject-matter` → `civpro-topic-diversity-jurisdiction` | Diversity jurisdiction | p. 11, I.A.2 | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-jurisdiction` |
| 3 | `civpro-topic-supplemental-jurisdiction` | `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-subsection-i-a-federal-subject-matter` → `civpro-topic-supplemental-jurisdiction` | Supplemental jurisdiction | p. 11, I.A.3 | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-jurisdiction` |
| 4 | `civpro-topic-concurrent-removal-jurisdiction` | `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-subsection-i-a-federal-subject-matter` → `civpro-topic-concurrent-removal-jurisdiction` | Concurrent and removal jurisdiction | p. 11, I.A.4 | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-jurisdiction` |
| 5 | `civpro-topic-personal-jurisdiction` | `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-topic-personal-jurisdiction` | Personal jurisdiction | p. 11, I.B | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-jurisdiction` |
| 6 | `civpro-topic-service-process-notice` | `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-topic-service-process-notice` | Service of process and notice | p. 11, I.C | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-service-process-notice` |
| 7 | `civpro-topic-venue-forum-transfer` | `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-topic-venue-forum-transfer` | Venue, forum non conveniens, and transfer | p. 11, I.D | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-venue-transfer` |
| 8 | `civpro-topic-state-law-federal-court` | `subject-civil-procedure` → `civpro-topic-state-law-federal-court` | II. State law in federal court | p. 11, II | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-litigation` |
| 9 | `civpro-topic-preliminary-injunctions-tro` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-topic-preliminary-injunctions-tro` | Preliminary injunctions and temporary restraining orders | p. 12, III.A | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-litigation` |
| 10 | `civpro-topic-pleadings-amended-pleadings` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-topic-pleadings-amended-pleadings` | Pleadings and amended pleadings | p. 12, III.B | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-litigation` |
| 11 | `civpro-topic-rule-11` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-topic-rule-11` | Rule 11 | p. 12, III.C | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-litigation` |
| 12 | `civpro-topic-joinder-claims-parties` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-d-joinder` → `civpro-topic-joinder-claims-parties` | Joinder of multiple claims, joinder of parties, counterclaims, crossclaims, third-party practice, and severance | p. 12, III.D.1 | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-litigation` |
| 13 | `civpro-topic-intervention-rule-24` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-d-joinder` → `civpro-topic-intervention-rule-24` | Intervention under Rule 24 | p. 12, III.D.2 | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-litigation` |
| 14 | `civpro-topic-discovery-scope-limits` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-e-discovery` → `civpro-topic-discovery-scope-limits` | Scope and limits of discovery | p. 12, III.E.1 | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-litigation` |
| 15 | `civpro-topic-discovery-rule-26f` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-e-discovery` → `civpro-topic-discovery-rule-26f` | Rule 26(f) conference and planning for discovery | p. 12, III.E.2 | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-litigation` |
| 16 | `civpro-topic-discovery-tools-ediscovery` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-e-discovery` → `civpro-topic-discovery-tools-ediscovery` | Discovery tools and mechanisms, including e-discovery | p. 12, III.E.3 | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-litigation` |
| 17 | `civpro-topic-discovery-motions` | `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-e-discovery` → `civpro-topic-discovery-motions` | Discovery motions | p. 12, III.E.4 | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-litigation` |
| 18 | `civpro-topic-jury-trial-preservation` | `subject-civil-procedure` → `civpro-topic-jury-trial-preservation` | IV. Preserving the right to a jury trial | p. 12, IV | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-motions-judgments` |
| 19 | `civpro-topic-rule-12-dismissal` | `subject-civil-procedure` → `civpro-section-v-dispositive-motions` → `civpro-topic-rule-12-dismissal` | Motion to dismiss under Rule 12 | p. 13, V.A | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-motions-judgments` |
| 20 | `civpro-topic-judgment-pleadings` | `subject-civil-procedure` → `civpro-section-v-dispositive-motions` → `civpro-topic-judgment-pleadings` | Motion for judgment on the pleadings | p. 13, V.B | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-motions-judgments` |
| 21 | `civpro-topic-summary-judgment` | `subject-civil-procedure` → `civpro-section-v-dispositive-motions` → `civpro-topic-summary-judgment` | Summary judgment motion | p. 13, V.C | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-motions-judgments` |
| 22 | `civpro-topic-jmol` | `subject-civil-procedure` → `civpro-section-v-dispositive-motions` → `civpro-topic-jmol` | Motion for judgment as a matter of law | p. 13, V.D | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-motions-judgments` |
| 23 | `civpro-topic-default-default-judgment` | `subject-civil-procedure` → `civpro-section-vi-judgments` → `civpro-topic-default-default-judgment` | Entry of default and default judgment | p. 13, VI.A | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-motions-judgments` |
| 24 | `civpro-topic-effect-judgment-preclusion` | `subject-civil-procedure` → `civpro-section-vi-judgments` → `civpro-topic-effect-judgment-preclusion` | Effect of judgment | p. 13, VI.B | `STARRED` / `RECALLED_REQUIRED` | `civil-procedure-motions-judgments` |
| 25 | `civpro-topic-final-judgment-rule` | `subject-civil-procedure` → `civpro-section-vii-appealability-review` → `civpro-topic-final-judgment-rule` | Final judgment rule | p. 13, VII.A | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-appeals` |
| 26 | `civpro-topic-interlocutory-review` | `subject-civil-procedure` → `civpro-section-vii-appealability-review` → `civpro-topic-interlocutory-review` | Availability of interlocutory review | p. 13, VII.B | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-appeals` |
| 27 | `civpro-topic-standards-review` | `subject-civil-procedure` → `civpro-section-vii-appealability-review` → `civpro-topic-standards-review` | Standard of review on appeal | p. 13, VII.C | `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES` | `civil-procedure-appeals` |

## Corrected coverage requirements, typed slots, and authority mappings

Every terminal topic has at least one required planning state. Required slots state the minimum structural Rule Obligation kinds future certified candidates must satisfy; allowed kinds bound what may be proposed without implying that every allowed kind is mandatory.

### `civpro-topic-federal-question-jurisdiction` — Federal question jurisdiction

- Hierarchy: `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-subsection-i-a-federal-subject-matter` → `civpro-topic-federal-question-jurisdiction`
- Locator: p. 11, I.A.1
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-jurisdiction`

#### `civpro-federal-question`

- Description: Federal-question jurisdiction, including the well-pleaded-complaint and arising-under boundaries.
- Requirement type: `GOVERNING_RULE`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Typed slots:
  - `civpro-federal-question-rule` — `RULE`; minimum `1`
  - `civpro-federal-question-element` — `ELEMENT`; minimum `1`; relationships: `civpro-federal-question-rule` → `HAS_ELEMENT`
  - `civpro-federal-question-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-federal-question-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-jurisdiction-removal` (Title 28 jurisdiction, removal, and remand provisions); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `CONDITIONAL` → `authority-scotus-jurisdiction` (U.S. Supreme Court jurisdiction authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a proposition not responsibly established by statutory text alone.
  - `CONDITIONAL` → `authority-us-constitution-article-iii` (U.S. Constitution, Article III); propositions: `CONSTITUTIONAL_BOUNDARY`. Condition: A candidate distinguishes constitutional judicial power from statutory jurisdiction.

### `civpro-topic-diversity-jurisdiction` — Diversity jurisdiction

- Hierarchy: `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-subsection-i-a-federal-subject-matter` → `civpro-topic-diversity-jurisdiction`
- Locator: p. 11, I.A.2
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-jurisdiction`

#### `civpro-diversity`

- Description: Diversity jurisdiction, citizenship, complete diversity, amount in controversy, and aggregation.
- Requirement type: `ELEMENTS_FACTORS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `DISTINCTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `DISTINCTION`, `LIMITATION`
- Typed slots:
  - `civpro-diversity-rule` — `RULE`; minimum `1`
  - `civpro-diversity-element` — `ELEMENT`; minimum `1`; relationships: `civpro-diversity-rule` → `HAS_ELEMENT`
  - `civpro-diversity-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-diversity-rule` → `HAS_DISTINCTION`
  - `civpro-diversity-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-diversity-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-jurisdiction-removal` (Title 28 jurisdiction, removal, and remand provisions); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `CONDITIONAL` → `authority-scotus-jurisdiction` (U.S. Supreme Court jurisdiction authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a proposition not responsibly established by statutory text alone.

### `civpro-topic-supplemental-jurisdiction` — Supplemental jurisdiction

- Hierarchy: `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-subsection-i-a-federal-subject-matter` → `civpro-topic-supplemental-jurisdiction`
- Locator: p. 11, I.A.3
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-jurisdiction`

#### `civpro-supplemental`

- Description: Supplemental jurisdiction, statutory inclusion limits, and discretionary declination.
- Requirement type: `EXCEPTIONS_LIMITATIONS`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `LIMITATION`
- Typed slots:
  - `civpro-supplemental-rule` — `RULE`; minimum `1`
  - `civpro-supplemental-element` — `ELEMENT`; minimum `1`; relationships: `civpro-supplemental-rule` → `HAS_ELEMENT`
  - `civpro-supplemental-exception` — `EXCEPTION`; minimum `1`; relationships: `civpro-supplemental-rule` → `HAS_EXCEPTION`
  - `civpro-supplemental-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-supplemental-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-jurisdiction-removal` (Title 28 jurisdiction, removal, and remand provisions); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `CONDITIONAL` → `authority-scotus-jurisdiction` (U.S. Supreme Court jurisdiction authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a proposition not responsibly established by statutory text alone.

### `civpro-topic-concurrent-removal-jurisdiction` — Concurrent and removal jurisdiction

- Hierarchy: `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-subsection-i-a-federal-subject-matter` → `civpro-topic-concurrent-removal-jurisdiction`
- Locator: p. 11, I.A.4
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-jurisdiction`

#### `civpro-concurrent-jurisdiction`

- Description: Concurrent federal and state court authority where the official combined topic requires it.
- Requirement type: `DISTINCTIONS_DEFINITIONS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `DISTINCTION`
- Allowed Rule Obligation kinds: `RULE`, `DISTINCTION`
- Typed slots:
  - `civpro-concurrent-jurisdiction-rule` — `RULE`; minimum `1`
  - `civpro-concurrent-jurisdiction-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-concurrent-jurisdiction-rule` → `HAS_DISTINCTION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-jurisdiction-removal` (Title 28 jurisdiction, removal, and remand provisions); propositions: `GOVERNING_STATUTORY_TEXT`.

#### `civpro-removal-remand`

- Description: Removal eligibility and procedure, remand grounds and procedure, and destination district.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Typed slots:
  - `civpro-removal-remand-rule` — `RULE`; minimum `1`
  - `civpro-removal-remand-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-removal-remand-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-removal-remand-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-removal-remand-rule` → `HAS_LIMITATION`
  - `civpro-removal-remand-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-removal-remand-rule` → `HAS_REMEDY`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-jurisdiction-removal` (Title 28 jurisdiction, removal, and remand provisions); propositions: `GOVERNING_STATUTORY_TEXT`.

### `civpro-topic-personal-jurisdiction` — Personal jurisdiction

- Hierarchy: `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-topic-personal-jurisdiction`
- Locator: p. 11, I.B
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-jurisdiction`

#### `civpro-personal-specific`

- Description: Specific personal jurisdiction and constitutional contacts, relatedness, and reasonableness.
- Requirement type: `ELEMENTS_FACTORS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `FACTOR`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `FACTOR`, `LIMITATION`
- Typed slots:
  - `civpro-personal-specific-rule` — `RULE`; minimum `1`
  - `civpro-personal-specific-factor` — `FACTOR`; minimum `1`; relationships: `civpro-personal-specific-rule` → `HAS_FACTOR`
  - `civpro-personal-specific-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-personal-specific-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-us-constitution-due-process` (U.S. Constitution, Due Process Clauses); propositions: `CONSTITUTIONAL_STANDARD`.
  - `REQUIRED` → `authority-scotus-personal-jurisdiction` (U.S. Supreme Court personal-jurisdiction authority); propositions: `CONTROLLING_HOLDING`.

#### `civpro-personal-general`

- Description: General personal jurisdiction for individuals and entities and the at-home distinction.
- Requirement type: `DISTINCTIONS_DEFINITIONS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `DISTINCTION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `DISTINCTION`
- Typed slots:
  - `civpro-personal-general-rule` — `RULE`; minimum `1`
  - `civpro-personal-general-element` — `ELEMENT`; minimum `1`; relationships: `civpro-personal-general-rule` → `HAS_ELEMENT`
  - `civpro-personal-general-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-personal-general-rule` → `HAS_DISTINCTION`
- Authority mappings:
  - `REQUIRED` → `authority-us-constitution-due-process` (U.S. Constitution, Due Process Clauses); propositions: `CONSTITUTIONAL_STANDARD`.
  - `REQUIRED` → `authority-scotus-personal-jurisdiction` (U.S. Supreme Court personal-jurisdiction authority); propositions: `CONTROLLING_HOLDING`.

#### `civpro-personal-authority-consent-waiver`

- Description: Long-arm authority, consent, and waiver within the personal-jurisdiction perimeter.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`, `LIMITATION`
- Typed slots:
  - `civpro-personal-authority-consent-waiver-rule` — `RULE`; minimum `1`
  - `civpro-personal-authority-consent-waiver-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-personal-authority-consent-waiver-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-personal-authority-consent-waiver-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-personal-authority-consent-waiver-rule` → `HAS_DISTINCTION`
  - `civpro-personal-authority-consent-waiver-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-personal-authority-consent-waiver-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-us-constitution-due-process` (U.S. Constitution, Due Process Clauses); propositions: `CONSTITUTIONAL_STANDARD`.
  - `REQUIRED` → `authority-scotus-personal-jurisdiction` (U.S. Supreme Court personal-jurisdiction authority); propositions: `CONTROLLING_HOLDING`.
  - `CONDITIONAL` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`. Condition: A candidate states a waiver or procedural-defense proposition governed by the FRCP.

### `civpro-topic-service-process-notice` — Service of process and notice

- Hierarchy: `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-topic-service-process-notice`
- Locator: p. 11, I.C
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-service-process-notice`

#### `civpro-notice-constitutional`

- Description: Constitutional sufficiency of notice.
- Requirement type: `ELEMENTS_FACTORS`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `FACTOR`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `FACTOR`, `LIMITATION`
- Typed slots:
  - `civpro-notice-constitutional-rule` — `RULE`; minimum `1`
  - `civpro-notice-constitutional-factor` — `FACTOR`; minimum `1`; relationships: `civpro-notice-constitutional-rule` → `HAS_FACTOR`
  - `civpro-notice-constitutional-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-notice-constitutional-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-us-constitution-due-process` (U.S. Constitution, Due Process Clauses); propositions: `CONSTITUTIONAL_STANDARD`.
  - `REQUIRED` → `authority-scotus-notice` (U.S. Supreme Court constitutional-notice authority); propositions: `CONTROLLING_HOLDING`.

#### `civpro-service-methods`

- Description: Permitted service methods for individuals and entities.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`
- Typed slots:
  - `civpro-service-methods-rule` — `RULE`; minimum `1`
  - `civpro-service-methods-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-service-methods-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-service-methods-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-service-methods-rule` → `HAS_DISTINCTION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

#### `civpro-service-waiver`

- Description: Waiver of service within the official perimeter.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`
- Typed slots:
  - `civpro-service-waiver-rule` — `RULE`; minimum `1`
  - `civpro-service-waiver-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-service-waiver-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-service-waiver-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-service-waiver-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-venue-forum-transfer` — Venue, forum non conveniens, and transfer

- Hierarchy: `subject-civil-procedure` → `civpro-section-i-jurisdiction-venue` → `civpro-topic-venue-forum-transfer`
- Locator: p. 11, I.D
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-venue-transfer`

#### `civpro-venue-selection`

- Description: Initial federal venue selection.
- Requirement type: `ELEMENTS_FACTORS`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Typed slots:
  - `civpro-venue-selection-rule` — `RULE`; minimum `1`
  - `civpro-venue-selection-element` — `ELEMENT`; minimum `1`; relationships: `civpro-venue-selection-rule` → `HAS_ELEMENT`
  - `civpro-venue-selection-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-venue-selection-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-venue-transfer` (Title 28 venue and transfer provisions); propositions: `GOVERNING_STATUTORY_TEXT`.

#### `civpro-venue-improper-cure`

- Description: Improper venue and available cure.
- Requirement type: `CONSEQUENCES_REMEDIES`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `REMEDY`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `REMEDY`
- Typed slots:
  - `civpro-venue-improper-cure-rule` — `RULE`; minimum `1`
  - `civpro-venue-improper-cure-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-venue-improper-cure-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-venue-improper-cure-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-venue-improper-cure-rule` → `HAS_REMEDY`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-venue-transfer` (Title 28 venue and transfer provisions); propositions: `GOVERNING_STATUTORY_TEXT`.

#### `civpro-venue-transfer`

- Description: Statutory transfer rules and relevant branch distinctions.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `FACTOR`, `PROCEDURAL_STEP`, `DISTINCTION`
- Allowed Rule Obligation kinds: `RULE`, `FACTOR`, `PROCEDURAL_STEP`, `DISTINCTION`
- Typed slots:
  - `civpro-venue-transfer-rule` — `RULE`; minimum `1`
  - `civpro-venue-transfer-factor` — `FACTOR`; minimum `1`; relationships: `civpro-venue-transfer-rule` → `HAS_FACTOR`
  - `civpro-venue-transfer-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-venue-transfer-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-venue-transfer-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-venue-transfer-rule` → `HAS_DISTINCTION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-venue-transfer` (Title 28 venue and transfer provisions); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `CONDITIONAL` → `authority-scotus-venue` (U.S. Supreme Court venue and forum non conveniens authority); propositions: `CONTROLLING_HOLDING`. Condition: The candidate states a transfer proposition not fully established by statutory text.

#### `civpro-forum-non-conveniens`

- Description: Forum non conveniens dismissal as distinct from statutory transfer and venue cure.
- Requirement type: `CONSEQUENCES_REMEDIES`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `FACTOR`, `REMEDY`, `DISTINCTION`
- Allowed Rule Obligation kinds: `RULE`, `FACTOR`, `REMEDY`, `DISTINCTION`
- Typed slots:
  - `civpro-forum-non-conveniens-rule` — `RULE`; minimum `1`
  - `civpro-forum-non-conveniens-factor` — `FACTOR`; minimum `1`; relationships: `civpro-forum-non-conveniens-rule` → `HAS_FACTOR`
  - `civpro-forum-non-conveniens-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-forum-non-conveniens-rule` → `HAS_REMEDY`
  - `civpro-forum-non-conveniens-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-forum-non-conveniens-rule` → `HAS_DISTINCTION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-venue-transfer` (Title 28 venue and transfer provisions); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `REQUIRED` → `authority-scotus-venue` (U.S. Supreme Court venue and forum non conveniens authority); propositions: `CONTROLLING_HOLDING`.

### `civpro-topic-state-law-federal-court` — II. State law in federal court

- Hierarchy: `subject-civil-procedure` → `civpro-topic-state-law-federal-court`
- Locator: p. 11, II
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-erie-substance-procedure`

- Description: Erie substance/procedure branch and circumstances in which state substantive law displaces federal decisional law.
- Requirement type: `DISTINCTIONS_DEFINITIONS`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `DISTINCTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `DISTINCTION`, `LIMITATION`
- Typed slots:
  - `civpro-erie-substance-procedure-rule` — `RULE`; minimum `1`
  - `civpro-erie-substance-procedure-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-erie-substance-procedure-rule` → `HAS_DISTINCTION`
  - `civpro-erie-substance-procedure-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-erie-substance-procedure-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-rules-of-decision-act` (Rules of Decision Act); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `REQUIRED` → `authority-scotus-erie` (U.S. Supreme Court Erie/Hanna authority); propositions: `CONTROLLING_HOLDING`.
  - `CONDITIONAL` → `authority-us-constitution-article-iii` (U.S. Constitution, Article III); propositions: `CONSTITUTIONAL_BOUNDARY`. Condition: The candidate expressly relies on a constitutional allocation proposition.

#### `civpro-erie-federal-rule-on-point`

- Description: Federal-rule-directly-on-point and Rules Enabling Act branch when those authorities are implicated.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `DISTINCTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `DISTINCTION`, `LIMITATION`
- Typed slots:
  - `civpro-erie-federal-rule-on-point-rule` — `RULE`; minimum `1`
  - `civpro-erie-federal-rule-on-point-element` — `ELEMENT`; minimum `1`; relationships: `civpro-erie-federal-rule-on-point-rule` → `HAS_ELEMENT`
  - `civpro-erie-federal-rule-on-point-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-erie-federal-rule-on-point-rule` → `HAS_DISTINCTION`
  - `civpro-erie-federal-rule-on-point-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-erie-federal-rule-on-point-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-scotus-erie` (U.S. Supreme Court Erie/Hanna authority); propositions: `CONTROLLING_HOLDING`.
  - `CONDITIONAL` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`. Condition: A Federal Rule of Civil Procedure is directly on point for the candidate proposition.
  - `CONDITIONAL` → `authority-rules-enabling-act` (Rules Enabling Act); propositions: `GOVERNING_STATUTORY_TEXT`. Condition: The candidate requires Rules Enabling Act validity or scope analysis.
  - `CONDITIONAL` → `authority-rules-of-decision-act` (Rules of Decision Act); propositions: `GOVERNING_STATUTORY_TEXT`. Condition: No federal rule is directly on point and the Rules of Decision Act branch controls.

#### `civpro-erie-choice-of-law`

- Description: State choice-of-law treatment within the national federal Erie inquiry.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`
- Typed slots:
  - `civpro-erie-choice-of-law-rule` — `RULE`; minimum `1`
  - `civpro-erie-choice-of-law-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-erie-choice-of-law-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-erie-choice-of-law-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-erie-choice-of-law-rule` → `HAS_DISTINCTION`
- Authority mappings:
  - `REQUIRED` → `authority-scotus-erie` (U.S. Supreme Court Erie/Hanna authority); propositions: `CONTROLLING_HOLDING`.
  - `REQUIRED` → `authority-rules-of-decision-act` (Rules of Decision Act); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `CONDITIONAL` → `authority-incorporated-state-law` (State primary law incorporated by a federal choice-of-law inquiry); propositions: `INCORPORATED_STATE_PRIMARY_TEXT`. Condition: A national federal choice-of-law proposition requires an exact state-law fact for comparison.

### `civpro-topic-preliminary-injunctions-tro` — Preliminary injunctions and temporary restraining orders

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-topic-preliminary-injunctions-tro`
- Locator: p. 12, III.A
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-preliminary-injunctions-tro`

- Description: Temporary restraining orders and preliminary injunctions as status-quo devices, including the preliminary-to-permanent relationship.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `FACTOR`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Allowed Rule Obligation kinds: `RULE`, `FACTOR`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Typed slots:
  - `civpro-preliminary-injunctions-tro-rule` — `RULE`; minimum `1`
  - `civpro-preliminary-injunctions-tro-factor` — `FACTOR`; minimum `1`; relationships: `civpro-preliminary-injunctions-tro-rule` → `HAS_FACTOR`
  - `civpro-preliminary-injunctions-tro-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-preliminary-injunctions-tro-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-preliminary-injunctions-tro-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-preliminary-injunctions-tro-rule` → `HAS_LIMITATION`
  - `civpro-preliminary-injunctions-tro-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-preliminary-injunctions-tro-rule` → `HAS_REMEDY`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.
  - `REQUIRED` → `authority-scotus-pleading-injunction` (U.S. Supreme Court pleading and preliminary-injunction authority); propositions: `CONTROLLING_HOLDING`.

### `civpro-topic-pleadings-amended-pleadings` — Pleadings and amended pleadings

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-topic-pleadings-amended-pleadings`
- Locator: p. 12, III.B
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-pleading-standards-responsive`

- Description: Complaint and answer pleading standards and responsive pleadings within the official pleading topic.
- Requirement type: `GOVERNING_RULE`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Typed slots:
  - `civpro-pleading-standards-responsive-rule` — `RULE`; minimum `1`
  - `civpro-pleading-standards-responsive-element` — `ELEMENT`; minimum `1`; relationships: `civpro-pleading-standards-responsive-rule` → `HAS_ELEMENT`
  - `civpro-pleading-standards-responsive-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-pleading-standards-responsive-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-pleading-standards-responsive-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-pleading-standards-responsive-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.
  - `REQUIRED` → `authority-scotus-pleading-injunction` (U.S. Supreme Court pleading and preliminary-injunction authority); propositions: `CONTROLLING_HOLDING`.

#### `civpro-amendments-relation-back`

- Description: Amended pleadings and relation back.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Typed slots:
  - `civpro-amendments-relation-back-rule` — `RULE`; minimum `1`
  - `civpro-amendments-relation-back-element` — `ELEMENT`; minimum `1`; relationships: `civpro-amendments-relation-back-rule` → `HAS_ELEMENT`
  - `civpro-amendments-relation-back-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-amendments-relation-back-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-amendments-relation-back-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-amendments-relation-back-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.
  - `CONDITIONAL` → `authority-scotus-pleading-injunction` (U.S. Supreme Court pleading and preliminary-injunction authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a controlling relation-back proposition not responsibly established by rule text alone.

### `civpro-topic-rule-11` — Rule 11

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-topic-rule-11`
- Locator: p. 12, III.C
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-rule-11`

- Description: Rule 11 inquiry, support, purpose, timing, procedure, and bounded sanctions consequences.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Typed slots:
  - `civpro-rule-11-rule` — `RULE`; minimum `1`
  - `civpro-rule-11-element` — `ELEMENT`; minimum `1`; relationships: `civpro-rule-11-rule` → `HAS_ELEMENT`
  - `civpro-rule-11-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-rule-11-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-rule-11-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-rule-11-rule` → `HAS_LIMITATION`
  - `civpro-rule-11-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-rule-11-rule` → `HAS_REMEDY`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-joinder-claims-parties` — Joinder of multiple claims, joinder of parties, counterclaims, crossclaims, third-party practice, and severance

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-d-joinder` → `civpro-topic-joinder-claims-parties`
- Locator: p. 12, III.D.1
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-joinder-claims`

- Description: Joinder of multiple claims.
- Requirement type: `ELEMENTS_FACTORS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Typed slots:
  - `civpro-joinder-claims-rule` — `RULE`; minimum `1`
  - `civpro-joinder-claims-element` — `ELEMENT`; minimum `1`; relationships: `civpro-joinder-claims-rule` → `HAS_ELEMENT`
  - `civpro-joinder-claims-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-joinder-claims-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

#### `civpro-joinder-parties`

- Description: Joinder of parties.
- Requirement type: `ELEMENTS_FACTORS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Typed slots:
  - `civpro-joinder-parties-rule` — `RULE`; minimum `1`
  - `civpro-joinder-parties-element` — `ELEMENT`; minimum `1`; relationships: `civpro-joinder-parties-rule` → `HAS_ELEMENT`
  - `civpro-joinder-parties-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-joinder-parties-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

#### `civpro-counterclaims-crossclaims`

- Description: Counterclaims and crossclaims with their distinct procedural classifications.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`, `LIMITATION`
- Typed slots:
  - `civpro-counterclaims-crossclaims-rule` — `RULE`; minimum `1`
  - `civpro-counterclaims-crossclaims-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-counterclaims-crossclaims-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-counterclaims-crossclaims-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-counterclaims-crossclaims-rule` → `HAS_DISTINCTION`
  - `civpro-counterclaims-crossclaims-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-counterclaims-crossclaims-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

#### `civpro-impleader`

- Description: Third-party practice and impleader.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Typed slots:
  - `civpro-impleader-rule` — `RULE`; minimum `1`
  - `civpro-impleader-element` — `ELEMENT`; minimum `1`; relationships: `civpro-impleader-rule` → `HAS_ELEMENT`
  - `civpro-impleader-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-impleader-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-impleader-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-impleader-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

#### `civpro-severance`

- Description: The court's overriding power to sever within the official joinder topic.
- Requirement type: `CONSEQUENCES_REMEDIES`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `FACTOR`, `REMEDY`
- Allowed Rule Obligation kinds: `RULE`, `FACTOR`, `REMEDY`
- Typed slots:
  - `civpro-severance-rule` — `RULE`; minimum `1`
  - `civpro-severance-factor` — `FACTOR`; minimum `1`; relationships: `civpro-severance-rule` → `HAS_FACTOR`
  - `civpro-severance-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-severance-rule` → `HAS_REMEDY`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-intervention-rule-24` — Intervention under Rule 24

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-d-joinder` → `civpro-topic-intervention-rule-24`
- Locator: p. 12, III.D.2
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-intervention`

- Description: Intervention as of right and permissive intervention, including circumstances barring intervention.
- Requirement type: `EXCEPTIONS_LIMITATIONS`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`, `DISTINCTION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`, `DISTINCTION`
- Typed slots:
  - `civpro-intervention-rule` — `RULE`; minimum `1`
  - `civpro-intervention-element` — `ELEMENT`; minimum `1`; relationships: `civpro-intervention-rule` → `HAS_ELEMENT`
  - `civpro-intervention-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-intervention-rule` → `HAS_LIMITATION`
  - `civpro-intervention-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-intervention-rule` → `HAS_DISTINCTION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-discovery-scope-limits` — Scope and limits of discovery

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-e-discovery` → `civpro-topic-discovery-scope-limits`
- Locator: p. 12, III.E.1
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-discovery-scope-limits`

- Description: Scope and limits of discovery.
- Requirement type: `EXCEPTIONS_LIMITATIONS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `LIMITATION`
- Typed slots:
  - `civpro-discovery-scope-limits-rule` — `RULE`; minimum `1`
  - `civpro-discovery-scope-limits-element` — `ELEMENT`; minimum `1`; relationships: `civpro-discovery-scope-limits-rule` → `HAS_ELEMENT`
  - `civpro-discovery-scope-limits-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-discovery-scope-limits-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-discovery-rule-26f` — Rule 26(f) conference and planning for discovery

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-e-discovery` → `civpro-topic-discovery-rule-26f`
- Locator: p. 12, III.E.2
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-discovery-rule-26f`

- Description: Rule 26(f) conference and proposed discovery planning.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`
- Typed slots:
  - `civpro-discovery-rule-26f-rule` — `RULE`; minimum `1`
  - `civpro-discovery-rule-26f-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-discovery-rule-26f-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-discovery-rule-26f-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-discovery-rule-26f-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-discovery-tools-ediscovery` — Discovery tools and mechanisms, including e-discovery

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-e-discovery` → `civpro-topic-discovery-tools-ediscovery`
- Locator: p. 12, III.E.3
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-discovery-tools-ediscovery`

- Description: Discovery tools and mechanisms, including electronically stored information.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `DISTINCTION`, `LIMITATION`
- Typed slots:
  - `civpro-discovery-tools-ediscovery-rule` — `RULE`; minimum `1`
  - `civpro-discovery-tools-ediscovery-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-discovery-tools-ediscovery-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-discovery-tools-ediscovery-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-discovery-tools-ediscovery-rule` → `HAS_DISTINCTION`
  - `civpro-discovery-tools-ediscovery-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-discovery-tools-ediscovery-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-discovery-motions` — Discovery motions

- Hierarchy: `subject-civil-procedure` → `civpro-section-iii-pretrial-procedures` → `civpro-subsection-iii-e-discovery` → `civpro-topic-discovery-motions`
- Locator: p. 12, III.E.4
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-litigation`

#### `civpro-discovery-motions`

- Description: Protective-order, privilege-claim, and compel-motion procedure, plus recognition—not exhaustive memorization—of possible sanctions.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Typed slots:
  - `civpro-discovery-motions-rule` — `RULE`; minimum `1`
  - `civpro-discovery-motions-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-discovery-motions-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-discovery-motions-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-discovery-motions-rule` → `HAS_LIMITATION`
  - `civpro-discovery-motions-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-discovery-motions-rule` → `HAS_REMEDY`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-jury-trial-preservation` — IV. Preserving the right to a jury trial

- Hierarchy: `subject-civil-procedure` → `civpro-topic-jury-trial-preservation`
- Locator: p. 12, IV
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-motions-judgments`

#### `civpro-jury-preservation-waiver`

- Description: Preserving the jury-trial right and waiver consequences, excluding JMOL and generic verdict doctrine.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`
- Typed slots:
  - `civpro-jury-preservation-waiver-rule` — `RULE`; minimum `1`
  - `civpro-jury-preservation-waiver-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-jury-preservation-waiver-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-jury-preservation-waiver-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-jury-preservation-waiver-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-us-constitution-seventh` (U.S. Constitution, Seventh Amendment); propositions: `CONSTITUTIONAL_TEXT`.
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.
  - `CONDITIONAL` → `authority-scotus-jury` (U.S. Supreme Court jury-trial authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a constitutional jury proposition not established by text and rules alone.

### `civpro-topic-rule-12-dismissal` — Motion to dismiss under Rule 12

- Hierarchy: `subject-civil-procedure` → `civpro-section-v-dispositive-motions` → `civpro-topic-rule-12-dismissal`
- Locator: p. 13, V.A
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-motions-judgments`

#### `civpro-rule-12-dismissal`

- Description: Rule 12 dismissal timing, procedure, grounds, and failure-to-state-a-claim standard.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `DEFENSE`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `DEFENSE`, `LIMITATION`
- Typed slots:
  - `civpro-rule-12-dismissal-rule` — `RULE`; minimum `1`
  - `civpro-rule-12-dismissal-element` — `ELEMENT`; minimum `1`; relationships: `civpro-rule-12-dismissal-rule` → `HAS_ELEMENT`
  - `civpro-rule-12-dismissal-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-rule-12-dismissal-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-rule-12-dismissal-defense` — `DEFENSE`; minimum `1`; relationships: `civpro-rule-12-dismissal-rule` → `HAS_DEFENSE`
  - `civpro-rule-12-dismissal-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-rule-12-dismissal-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.
  - `CONDITIONAL` → `authority-scotus-pleading-injunction` (U.S. Supreme Court pleading and preliminary-injunction authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a controlling federal pleading or summary-judgment standard requiring case support.

### `civpro-topic-judgment-pleadings` — Motion for judgment on the pleadings

- Hierarchy: `subject-civil-procedure` → `civpro-section-v-dispositive-motions` → `civpro-topic-judgment-pleadings`
- Locator: p. 13, V.B
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-motions-judgments`

#### `civpro-judgment-pleadings`

- Description: Motion for judgment on the pleadings.
- Requirement type: `GOVERNING_RULE`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Typed slots:
  - `civpro-judgment-pleadings-rule` — `RULE`; minimum `1`
  - `civpro-judgment-pleadings-element` — `ELEMENT`; minimum `1`; relationships: `civpro-judgment-pleadings-rule` → `HAS_ELEMENT`
  - `civpro-judgment-pleadings-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-judgment-pleadings-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-judgment-pleadings-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-judgment-pleadings-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-summary-judgment` — Summary judgment motion

- Hierarchy: `subject-civil-procedure` → `civpro-section-v-dispositive-motions` → `civpro-topic-summary-judgment`
- Locator: p. 13, V.C
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-motions-judgments`

#### `civpro-summary-judgment`

- Description: Summary-judgment timing, procedure, standards, and Rule 12 conversion.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`
- Typed slots:
  - `civpro-summary-judgment-rule` — `RULE`; minimum `1`
  - `civpro-summary-judgment-element` — `ELEMENT`; minimum `1`; relationships: `civpro-summary-judgment-rule` → `HAS_ELEMENT`
  - `civpro-summary-judgment-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-summary-judgment-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-summary-judgment-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-summary-judgment-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.
  - `CONDITIONAL` → `authority-scotus-pleading-injunction` (U.S. Supreme Court pleading and preliminary-injunction authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a controlling federal pleading or summary-judgment standard requiring case support.

### `civpro-topic-jmol` — Motion for judgment as a matter of law

- Hierarchy: `subject-civil-procedure` → `civpro-section-v-dispositive-motions` → `civpro-topic-jmol`
- Locator: p. 13, V.D
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-motions-judgments`

#### `civpro-jmol`

- Description: Judgment as a matter of law, including directed-verdict and post-verdict branches, separate from jury preservation.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Typed slots:
  - `civpro-jmol-rule` — `RULE`; minimum `1`
  - `civpro-jmol-element` — `ELEMENT`; minimum `1`; relationships: `civpro-jmol-rule` → `HAS_ELEMENT`
  - `civpro-jmol-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-jmol-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-jmol-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-jmol-rule` → `HAS_LIMITATION`
  - `civpro-jmol-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-jmol-rule` → `HAS_REMEDY`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.
  - `CONDITIONAL` → `authority-scotus-jury` (U.S. Supreme Court jury-trial authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a constitutional or controlling case-driven JMOL proposition.

### `civpro-topic-default-default-judgment` — Entry of default and default judgment

- Hierarchy: `subject-civil-procedure` → `civpro-section-vi-judgments` → `civpro-topic-default-default-judgment`
- Locator: p. 13, VI.A
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-motions-judgments`

#### `civpro-default-default-judgment`

- Description: Entry of default and default judgment.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Allowed Rule Obligation kinds: `RULE`, `PROCEDURAL_STEP`, `LIMITATION`, `REMEDY`
- Typed slots:
  - `civpro-default-default-judgment-rule` — `RULE`; minimum `1`
  - `civpro-default-default-judgment-procedural-step` — `PROCEDURAL_STEP`; minimum `1`; relationships: `civpro-default-default-judgment-rule` → `HAS_PROCEDURAL_STEP`
  - `civpro-default-default-judgment-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-default-default-judgment-rule` → `HAS_LIMITATION`
  - `civpro-default-default-judgment-remedy` — `REMEDY`; minimum `1`; relationships: `civpro-default-default-judgment-rule` → `HAS_REMEDY`
- Authority mappings:
  - `REQUIRED` → `authority-frcp-current` (Federal Rules of Civil Procedure); propositions: `CONTROLLING_RULE_TEXT`.

### `civpro-topic-effect-judgment-preclusion` — Effect of judgment

- Hierarchy: `subject-civil-procedure` → `civpro-section-vi-judgments` → `civpro-topic-effect-judgment-preclusion`
- Locator: p. 13, VI.B
- Treatment: `STARRED` / `RECALLED_REQUIRED`
- Planning aggregate: `civil-procedure-motions-judgments`

#### `civpro-claim-preclusion`

- Description: Claim-preclusion elements and limits within effect of judgment.
- Requirement type: `ELEMENTS_FACTORS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `LIMITATION`
- Typed slots:
  - `civpro-claim-preclusion-rule` — `RULE`; minimum `1`
  - `civpro-claim-preclusion-element` — `ELEMENT`; minimum `1`; relationships: `civpro-claim-preclusion-rule` → `HAS_ELEMENT`
  - `civpro-claim-preclusion-exception` — `EXCEPTION`; minimum `1`; relationships: `civpro-claim-preclusion-rule` → `HAS_EXCEPTION`
  - `civpro-claim-preclusion-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-claim-preclusion-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-scotus-preclusion` (U.S. Supreme Court preclusion authority); propositions: `CONTROLLING_HOLDING`.
  - `CONDITIONAL` → `authority-28-usc-preclusion` (Title 28 judgment-recognition provisions); propositions: `GOVERNING_STATUTORY_TEXT`. Condition: A candidate requires a federal judgment-recognition statute.

#### `civpro-issue-preclusion`

- Description: Issue-preclusion elements, limits, and distinctions from claim preclusion.
- Requirement type: `DISTINCTIONS_DEFINITIONS`
- Treatment inherited from terminal topic: `RECALL`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `DISTINCTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `DISTINCTION`, `LIMITATION`
- Typed slots:
  - `civpro-issue-preclusion-rule` — `RULE`; minimum `1`
  - `civpro-issue-preclusion-element` — `ELEMENT`; minimum `1`; relationships: `civpro-issue-preclusion-rule` → `HAS_ELEMENT`
  - `civpro-issue-preclusion-exception` — `EXCEPTION`; minimum `1`; relationships: `civpro-issue-preclusion-rule` → `HAS_EXCEPTION`
  - `civpro-issue-preclusion-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-issue-preclusion-rule` → `HAS_DISTINCTION`
  - `civpro-issue-preclusion-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-issue-preclusion-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-scotus-preclusion` (U.S. Supreme Court preclusion authority); propositions: `CONTROLLING_HOLDING`.
  - `CONDITIONAL` → `authority-28-usc-preclusion` (Title 28 judgment-recognition provisions); propositions: `GOVERNING_STATUTORY_TEXT`. Condition: A candidate requires a federal judgment-recognition statute.

### `civpro-topic-final-judgment-rule` — Final judgment rule

- Hierarchy: `subject-civil-procedure` → `civpro-section-vii-appealability-review` → `civpro-topic-final-judgment-rule`
- Locator: p. 13, VII.A
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-appeals`

#### `civpro-final-judgment-rule`

- Description: Final-judgment appealability rule and supported exceptions.
- Requirement type: `EXCEPTIONS_LIMITATIONS`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`
- Typed slots:
  - `civpro-final-judgment-rule-rule` — `RULE`; minimum `1`
  - `civpro-final-judgment-rule-element` — `ELEMENT`; minimum `1`; relationships: `civpro-final-judgment-rule-rule` → `HAS_ELEMENT`
  - `civpro-final-judgment-rule-exception` — `EXCEPTION`; minimum `1`; relationships: `civpro-final-judgment-rule-rule` → `HAS_EXCEPTION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-appellate` (Title 28 appellate-jurisdiction provisions); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `CONDITIONAL` → `authority-scotus-appellate` (U.S. Supreme Court appealability and review authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a case-driven appealability or review proposition not established by statute alone.
  - `CONDITIONAL` → `authority-frap-conditional` (Federal Rules of Appellate Procedure); propositions: `CONTROLLING_RULE_TEXT`. Condition: The exact candidate proposition genuinely depends on an appellate procedural rule.

### `civpro-topic-interlocutory-review` — Availability of interlocutory review

- Hierarchy: `subject-civil-procedure` → `civpro-section-vii-appealability-review` → `civpro-topic-interlocutory-review`
- Locator: p. 13, VII.B
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-appeals`

#### `civpro-interlocutory-review`

- Description: Availability and distinct routes of interlocutory review within the official perimeter.
- Requirement type: `PROCEDURAL_BRANCHING`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `DISTINCTION`
- Allowed Rule Obligation kinds: `RULE`, `ELEMENT`, `EXCEPTION`, `DISTINCTION`
- Typed slots:
  - `civpro-interlocutory-review-rule` — `RULE`; minimum `1`
  - `civpro-interlocutory-review-element` — `ELEMENT`; minimum `1`; relationships: `civpro-interlocutory-review-rule` → `HAS_ELEMENT`
  - `civpro-interlocutory-review-exception` — `EXCEPTION`; minimum `1`; relationships: `civpro-interlocutory-review-rule` → `HAS_EXCEPTION`
  - `civpro-interlocutory-review-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-interlocutory-review-rule` → `HAS_DISTINCTION`
- Authority mappings:
  - `REQUIRED` → `authority-28-usc-appellate` (Title 28 appellate-jurisdiction provisions); propositions: `GOVERNING_STATUTORY_TEXT`.
  - `CONDITIONAL` → `authority-scotus-appellate` (U.S. Supreme Court appealability and review authority); propositions: `CONTROLLING_HOLDING`. Condition: A candidate states a case-driven appealability or review proposition not established by statute alone.
  - `CONDITIONAL` → `authority-frap-conditional` (Federal Rules of Appellate Procedure); propositions: `CONTROLLING_RULE_TEXT`. Condition: The exact candidate proposition genuinely depends on an appellate procedural rule.

### `civpro-topic-standards-review` — Standard of review on appeal

- Hierarchy: `subject-civil-procedure` → `civpro-section-vii-appealability-review` → `civpro-topic-standards-review`
- Locator: p. 13, VII.C
- Treatment: `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Planning aggregate: `civil-procedure-appeals`

#### `civpro-standards-review`

- Description: Standards of review and distinctions among the specified levels of appellate deference.
- Requirement type: `DISTINCTIONS_DEFINITIONS`
- Treatment inherited from terminal topic: `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`
- Required for subject completeness: `true`
- Required Rule Obligation kinds: `RULE`, `DISTINCTION`, `LIMITATION`
- Allowed Rule Obligation kinds: `RULE`, `DISTINCTION`, `LIMITATION`
- Typed slots:
  - `civpro-standards-review-rule` — `RULE`; minimum `1`
  - `civpro-standards-review-distinction` — `DISTINCTION`; minimum `1`; relationships: `civpro-standards-review-rule` → `HAS_DISTINCTION`
  - `civpro-standards-review-limitation` — `LIMITATION`; minimum `1`; relationships: `civpro-standards-review-rule` → `HAS_LIMITATION`
- Authority mappings:
  - `REQUIRED` → `authority-scotus-appellate` (U.S. Supreme Court appealability and review authority); propositions: `CONTROLLING_HOLDING`.
  - `CONDITIONAL` → `authority-frap-conditional` (Federal Rules of Appellate Procedure); propositions: `CONTROLLING_RULE_TEXT`. Condition: The exact candidate proposition genuinely depends on an appellate procedural rule.

## Authority acquisition, conditionality, freshness, and drift

There are 22 authority plans: 1 acquired and 21 planned. A planned family is not evidence and cannot support certification.

| Authority plan | Level | Status | Case proposition plan | Intended boundary |
|---|---|---|---|---|
| `authority-us-constitution-article-iii` | `CONTROLLING_CONSTITUTION` | `PLANNED` | `false` | Article III |
| `authority-us-constitution-due-process` | `CONTROLLING_CONSTITUTION` | `PLANNED` | `false` | Fifth and Fourteenth Amendment Due Process Clauses |
| `authority-us-constitution-seventh` | `CONTROLLING_CONSTITUTION` | `PLANNED` | `false` | Seventh Amendment |
| `authority-28-usc-jurisdiction-removal` | `CONTROLLING_STATUTE` | `PLANNED` | `false` | Current Title 28 district-court jurisdiction, removal, and remand provisions |
| `authority-28-usc-venue-transfer` | `CONTROLLING_STATUTE` | `PLANNED` | `false` | Current Title 28 venue and transfer provisions |
| `authority-rules-of-decision-act` | `CONTROLLING_STATUTE` | `PLANNED` | `false` | 28 U.S.C. § 1652 |
| `authority-rules-enabling-act` | `CONTROLLING_STATUTE` | `PLANNED` | `false` | 28 U.S.C. §§ 2071–2077 as applicable |
| `authority-28-usc-preclusion` | `CONTROLLING_STATUTE` | `PLANNED` | `false` | Current Title 28 judgment-recognition provisions where applicable |
| `authority-28-usc-appellate` | `CONTROLLING_STATUTE` | `PLANNED` | `false` | Current Title 28 appellate-jurisdiction provisions |
| `authority-frcp-current` | `CONTROLLING_RULE` | `ACQUIRED` | `false` | Federal Rules of Civil Procedure, amended through December 1, 2025 |
| `authority-frap-conditional` | `CONTROLLING_RULE` | `PLANNED` | `false` | Current Federal Rules of Appellate Procedure only for propositions that genuinely require them |
| `authority-incorporated-state-law` | `OTHER_PRIMARY` | `PLANNED` | `false` | Exact state primary source only when a national federal rule makes the comparison necessary |
| `authority-scotus-jurisdiction` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court subject-matter-jurisdiction authority |
| `authority-scotus-personal-jurisdiction` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court personal-jurisdiction authority |
| `authority-scotus-notice` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court notice authority |
| `authority-scotus-venue` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court venue, transfer, or forum non conveniens authority |
| `authority-scotus-erie` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court Erie/Hanna authority |
| `authority-scotus-pleading-injunction` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court pleading or preliminary-injunction authority |
| `authority-scotus-preclusion` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court claim- and issue-preclusion authority |
| `authority-scotus-jury` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court jury-trial authority |
| `authority-scotus-appellate` | `BINDING_SUPREME_COURT` | `PLANNED` | `true` | Requirement-specific controlling Supreme Court appealability or review authority |
| `authority-optional-secondary-reconciliation` | `OPTIONAL_SECONDARY` | `PLANNED` | `false` | Optional current secondary reconciliation source |

Every primary family requires version/effective-date verification and deterministic drift analysis before candidate certification. Every case plan requires exact case identity, court, decision date, reliable source URI, proposition locator, current authority status, and later-treatment review. Case law is requirement-specific: text may suffice for one proposition while controlling holdings are required or conditional for another. Optional secondary reconciliation can never replace primary authority.

### Erie/Hanna conditional cluster

- `civpro-erie-substance-procedure` requires the Rules of Decision Act and requirement-specific controlling Supreme Court support; Article III is conditional only when a candidate expressly relies on constitutional allocation.
- `civpro-erie-federal-rule-on-point` requires controlling Supreme Court support. FRCP is conditional on a federal rule being directly on point; Rules Enabling Act support is conditional on validity/scope analysis; Rules of Decision Act support is conditional on the no-direct-rule branch.
- `civpro-erie-choice-of-law` requires Rules of Decision Act and controlling Supreme Court support. Exact state primary law is conditional only when the national federal inquiry makes a state-law comparison necessary.
- No single generic obligation can satisfy all three branches, and no branch universally requires all authority families at once.

### National federal/state boundary

Federal doctrine directing incorporation or comparison of state law remains national NextGen core. Exact state-law facts may be conditional primary evidence only when a federal proposition requires them. Standalone California, New York, or other jurisdiction-specific procedure remains prohibited from national-core candidate truth.

## Existing Rule 4 pilot attribution

- Snapshot: `8ffc025a-ddac-5765-b7b2-130c84282c83`
- Compile SHA-256: `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`
- Certification SHA-256: `60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0`
- Classification: `PILOT_ONLY` / `PARTIAL_LEAF_COVERAGE`
- Official terminal topic attribution: `civpro-topic-service-process-notice`
- Required-perimeter-relevant candidate evidence: `frcp4-waiver-request`, `frcp4-waiver-expense-consequence`, `frcp4-domestic-individual-service`
- Supplemental candidate evidence: `frcp4-service-plaintiff-responsibility`, `frcp4-service-server-qualification`, `frcp4-service-time-limit`, `frcp4-good-cause-extension`, `frcp4-untimely-service-response`
- Rule 4(m) timing/consequences remain certified historical production evidence but are not required for Civil Procedure subject completeness.
- The snapshot does not complete service/notice, Rule 4, Civil Procedure, or the national curriculum, and no obligation, review, compile, or snapshot is reopened or mutated.

## Current completeness state

- Official terminal topics: `27`
- Planning aggregates: `6`
- Coverage requirements: `43`
- Required typed slots: `157`
- Authority plans: `22` (`1` acquired; `21` planned)
- Certified V2 requirement slots: `0`
- V2 human-review status: `PENDING`
- `subject_complete: false`
- `subject_certified: false`
- `national_complete: false`

Future `SUBJECT_CERTIFIED` requires every active terminal topic, every required slot, all applicable current primary authority, completed human review, deterministic reconciliation, zero blocking omission/conflict/jurisdiction/authority gaps, exact captured checksums, and a separate explicit certification operation. Aggregate or percentage coverage is insufficient.

## Open reviewer judgments

For each terminal topic and requirement, record `APPROVE`, `REJECT`, or a precise required revision. Specifically determine:

1. Whether the 27-topic identities, exact parent hierarchy, locators, and 14-starred/13-unstarred classifications faithfully normalize the accepted NCBE source.
2. Whether each planning aggregate is useful without being mistaken for official terminal truth.
3. Whether the 43 requirements and 157 slots achieve complete structural coverage without artificial uniformity or doctrinal excess.
4. Whether federal question, diversity, supplemental, concurrent/removal, and personal jurisdiction are separated at the correct level; whether concurrent jurisdiction is explicit enough.
5. Whether personal-jurisdiction planning appropriately covers specific/general jurisdiction, long-arm authority, consent, waiver, and constitutional limits without exceeding the source.
6. Whether service methods, waiver, and constitutional notice match the exact perimeter; whether the required-versus-supplemental Rule 4 evidence classifications are correct.
7. Whether venue selection, improper-venue cure, transfer, and forum non conveniens are appropriately distinct and nationally scoped.
8. Whether the three Erie/Hanna branches and their conditional constitutional/statutory/rule/state/case authority combinations are correct.
9. Whether the TRO/preliminary-injunction, pleading/amendment, Rule 11, joinder, intervention, and discovery decompositions match the official pretrial perimeter.
10. Whether discovery-sanctions coverage correctly requires recognition of possible sanctions without an exhaustive memorized taxonomy.
11. Whether jury preservation and waiver are complete while correctly excluding JMOL and generic verdict doctrine.
12. Whether Rule 12 dismissal, judgment on the pleadings, summary judgment, and JMOL remain distinct and carry correct topic-level treatment.
13. Whether default/default judgment and separate claim/issue-preclusion requirements exhaust the official judgments perimeter without importing Rule 59/60 posttrial relief.
14. Whether final judgment, interlocutory review, and standards of review exhaust the official appellate perimeter without broad procedure, preservation, or generic remedies.
15. Whether FRAP is correctly conditional and whether every case-law family is required, conditional, or unnecessary at the correct requirement level.
16. Whether any requirement should be split, combined, renamed, narrowed, or removed before substantive candidate compilation begins.

## Attestation boundary

A future V2 review record must identify the reviewer and qualification, the exact V2 packet SHA-256, resolution, rationale, attestation, and review time through `record_subject_plan_review`. Approval would cover this corrected planning structure only. It would not approve substantive candidate statements, complete Civil Procedure doctrine, another subject, assessment inventory, learner mastery/readiness, or national NextGen curriculum completeness.
