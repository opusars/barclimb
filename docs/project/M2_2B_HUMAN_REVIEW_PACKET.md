# M2.2b Human Review Packet V2 — FRCP Rule 4 Pilot

Status: **PENDING SECOND HUMAN SUBSTANTIVE REVIEW**

This corrected packet supersedes V1 for review but does not overwrite its history. V1 and its correction-required disposition are preserved in `M2_2B_HUMAN_REVIEW_PACKET_V1.md`. No human identity or final approval has been recorded, and certification remains blocked.

## Changes after first human review

- Candidate 1: substantive statement preserved; both misleading `HAS_PROCEDURAL_STEP` relationships removed.
- Candidate 2: substantive statement preserved; kind changed from `PROCEDURAL_STEP` to `LIMITATION`.
- Candidate 3: corrected to preserve the Rule 4(h) entity-addressee distinction and remaining Rule 4(d)(1)(B)–(G) requirements.
- Candidate 4: added the omitted condition that the waiver was requested by a plaintiff located within the United States and retained the defendant-location, good-cause, and expense predicates.
- Candidate 5: replaced “federal delivery methods” with the exact forum-state/service-state and listed Rule 4(e)(2) formulation.
- Candidates 6–8: statements and relationships preserved unchanged.

## Reviewer authority and evidence

The second reviewer must be a named human staff reviewer competent to review federal civil procedure. Record reviewer identity/role, review date, confirmation that the official authority was reviewed, and an `APPROVE` or `REJECT` decision with rationale for every candidate. This packet alone is not runtime approval; approved decisions must later be recorded through `record_obligation_review`.

## Official perimeter mapping

- Scope: `NCBE_NEXTGEN_SCOPE_2026_07_2027_02`
- Scope checksum: `2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f`
- Target leaf: `civil-procedure-service-process-notice`
- Official label: “Service of process and notice”
- NCBE locator: Content Scope, p. 11, I.C
- Treatment: unstarred; may be tested with or without legal resources. Without resources, recognition that the topic is at issue is expected.

## Substantive primary authority

- Authority ID: `USCOURTS_FRCP`
- Authority: Federal Rules of Civil Procedure, amended through December 1, 2025
- Canonical citation: `Fed. R. Civ. P. 4 (Dec. 1, 2025)`
- Issuer: Supreme Court of the United States and Congress; official pamphlet published by the House Committee on the Judiciary
- URI: <https://www.uscourts.gov/sites/default/files/document/federal-rules-of-civil-procedure.pdf>
- SHA-256: `bd8705fc038d87e4fe222a7ea2e4324222c9430e2373fce56826bd2dfa2f8baf`
- Storage: `TRANSIENT_HASH_ONLY`; no PDF bytes are committed or served.

## Candidate 1

- ID: `frcp4-service-plaintiff-responsibility`
- Kind: `RULE`
- Statement: The plaintiff is responsible for having the summons and complaint served within the time allowed by Rule 4(m) and must furnish the necessary copies to the person who makes service.
- Normalized: `the plaintiff is responsible for having the summons and complaint served within the time allowed by rule 4(m) and must furnish the necessary copies to the person who makes service.`
- Scope: `civil-procedure-service-process-notice`
- Locator: Rule 4(c)(1); pamphlet pp. 2–3
- Proposition: Plaintiff responsibility for service and copies.
- Mapping rationale: Rule 4(c)(1) directly concerns service of process.
- Relationships: none. The two V1 procedural-step relationships were removed.
- Status: `INCLUDED`; `REVIEW_REQUIRED`.
- Reviewer judgment: confirm the combined service/copies proposition remains sufficiently atomic.

## Candidate 2

- ID: `frcp4-service-server-qualification`
- Kind: `LIMITATION` (corrected from `PROCEDURAL_STEP`)
- Statement: A summons and complaint may be served by a person who is at least 18 years old and is not a party.
- Normalized: `a summons and complaint may be served by a person who is at least 18 years old and is not a party.`
- Scope: `civil-procedure-service-process-notice`
- Locator: Rule 4(c)(2); pamphlet p. 3
- Proposition: Nonparty adult server qualification.
- Mapping rationale: Rule 4(c)(2) limits who may serve process.
- Relationships: none.
- Status: `INCLUDED`; `REVIEW_REQUIRED`.
- Reviewer judgment: confirm `LIMITATION` accurately represents the server-qualification constraint.

## Candidate 3

- ID: `frcp4-waiver-request`
- Kind: `PROCEDURAL_STEP`
- Statement: A plaintiff requesting waiver of service must make the request in writing and address it to the individual defendant or, for a defendant subject to Rule 4(h), to an officer, managing or general agent, or other agent authorized by appointment or law to receive service of process, and must satisfy Rule 4(d)(1)’s remaining notice, copy, return-means, consequence, date, and response-time requirements.
- Normalized: `a plaintiff requesting waiver of service must make the request in writing and address it to the individual defendant or, for a defendant subject to rule 4(h), to an officer, managing or general agent, or other agent authorized by appointment or law to receive service of process, and must satisfy rule 4(d)(1)’s remaining notice, copy, return-means, consequence, date, and response-time requirements.`
- Scope: `civil-procedure-service-process-notice`
- Locator: Rule 4(d)(1)(A)–(G); pamphlet p. 3
- Proposition: Written waiver request; individual and Rule 4(h) addressee distinction; notice, copy, return-means, consequence, date, and response-time requirements.
- Mapping rationale: Rule 4(d)(1)(A) distinguishes the proper addressee for an individual from specified Rule 4(h) entity representatives; Rule 4(d)(1)(B)–(G) governs the remaining requirements.
- Relationships: none; waiver remains an alternative rather than a required formal-service sequence.
- Status: `INCLUDED`; `REVIEW_REQUIRED`.
- Reviewer judgment: confirm the corrected aggregate faithfully preserves the addressee distinction and all referenced requirement categories without implying a generic representative for every individual.

## Candidate 4

- ID: `frcp4-waiver-expense-consequence`
- Kind: `REMEDY`
- Statement: If a defendant located within the United States fails without good cause to sign and return a waiver requested by a plaintiff located within the United States, the court must impose the expenses later incurred in making service and the reasonable expenses, including attorney’s fees, of any motion required to collect those service expenses.
- Normalized: `if a defendant located within the united states fails without good cause to sign and return a waiver requested by a plaintiff located within the united states, the court must impose the expenses later incurred in making service and the reasonable expenses, including attorney’s fees, of any motion required to collect those service expenses.`
- Scope: `civil-procedure-service-process-notice`
- Locator: Rule 4(d)(2); pamphlet p. 3
- Proposition: Expense shifting, including attorney’s fees, after a United States defendant without good cause fails to return a waiver requested by a United States plaintiff.
- Mapping rationale: Rule 4(d)(2) conditions expense shifting on United States location of both the requesting plaintiff and nonwaiving defendant and identifies both expense categories.
- Relationships: none.
- Status: `INCLUDED`; `REVIEW_REQUIRED`.
- Reviewer judgment: confirm both location predicates, lack of good cause, and both recoverable-expense categories are accurately preserved.

## Candidate 5

- ID: `frcp4-domestic-individual-service`
- Kind: `DISTINCTION`
- Statement: An individual served within a United States judicial district may be served by a method allowed by the law of the state where the district court sits or the state where service is made, or by one of the methods listed in Rule 4(e)(2).
- Normalized: `an individual served within a united states judicial district may be served by a method allowed by the law of the state where the district court sits or the state where service is made, or by one of the methods listed in rule 4(e)(2).`
- Scope: `civil-procedure-service-process-notice`
- Locator: Rule 4(e)(1)–(2); pamphlet p. 4
- Proposition: Domestic individual service through applicable forum-state or service-state law or a listed Rule 4(e)(2) method.
- Mapping rationale: Rule 4(e) distinguishes methods allowed by the law of the state where the district court sits or service is made from the methods listed in Rule 4(e)(2).
- Relationships: none.
- Status: `INCLUDED`; `REVIEW_REQUIRED`.
- Reviewer judgment: confirm the precise formulation and national-core treatment of a federal rule that incorporates state-law methods.

## Candidate 6

- ID: `frcp4-service-time-limit`
- Kind: `LIMITATION`
- Statement: Rule 4(m) generally requires service within 90 days after the complaint is filed, subject to the rule's extension and inapplicability provisions.
- Normalized: `rule 4(m) generally requires service within 90 days after the complaint is filed, subject to the rule's extension and inapplicability provisions.`
- Scope: `civil-procedure-service-process-notice`
- Locator: Rule 4(m); pamphlet p. 8
- Proposition: General 90-day service period and qualification.
- Mapping rationale: Rule 4(m) directly limits the time for service.
- Relationships: `HAS_EXCEPTION` → `frcp4-good-cause-extension` (ordering 1); `HAS_REMEDY` → `frcp4-untimely-service-response` (ordering 2).
- Status: `INCLUDED`; `REVIEW_REQUIRED`.
- Reviewer judgment: statement preserved as first-review approved; pilot intentionally does not expand every Rule 4(m) qualification.

## Candidate 7

- ID: `frcp4-good-cause-extension`
- Kind: `EXCEPTION`
- Statement: If the plaintiff shows good cause for failure to serve within Rule 4(m)'s period, the court must extend the time for service for an appropriate period.
- Normalized: `if the plaintiff shows good cause for failure to serve within rule 4(m)'s period, the court must extend the time for service for an appropriate period.`
- Scope: `civil-procedure-service-process-notice`
- Locator: Rule 4(m); pamphlet p. 8
- Proposition: Good-cause extension.
- Mapping rationale: Rule 4(m) expressly requires an extension upon good cause.
- Relationships: target of Candidate 6's `HAS_EXCEPTION` relationship.
- Status: `INCLUDED`; `REVIEW_REQUIRED`.
- Reviewer judgment: statement and relationship preserved as first-review approved.

## Candidate 8

- ID: `frcp4-untimely-service-response`
- Kind: `REMEDY`
- Statement: After notice to the plaintiff, the court must dismiss without prejudice against an unserved defendant or order service within a specified time when Rule 4(m)'s period expires.
- Normalized: `after notice to the plaintiff, the court must dismiss without prejudice against an unserved defendant or order service within a specified time when rule 4(m)'s period expires.`
- Scope: `civil-procedure-service-process-notice`
- Locator: Rule 4(m); pamphlet p. 8
- Proposition: Dismissal without prejudice or service order after notice.
- Mapping rationale: Rule 4(m) states the court's alternatives after notice.
- Relationships: target of Candidate 6's `HAS_REMEDY` relationship.
- Status: `INCLUDED`; `REVIEW_REQUIRED`.
- Reviewer judgment: statement and relationship preserved as first-review approved.

## Deterministic V2 gate status

- Compile: `BARCLIMB_PILOT_FRCP_RULE4_2025_V2`
- Compiler: `BARCLIMB_RULE_COMPILER_V2`
- Policy: `BARCLIMB_FRCP_RULE4_SERVICE_PILOT@2025_V2`
- Coverage class: `PILOT_ONLY`
- Compile checksum: `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`
- Candidate/obligation count: 8/8
- Duplicate, omission, excess, conflict, ambiguity, provenance-deficiency, jurisdiction, and blocking issue counts: all 0
- Structured primary authority: present for all 8
- Target leaves sufficiently covered: 1 of 1
- Active official-scope testable leaves: 20
- `national_complete`: `false`
- All eight decisions: `REVIEW_REQUIRED`
- Compile lifecycle: `RECONCILED`
- Certification: **BLOCKED**, exactly because all eight V2 human attestations are absent
- Certification snapshot: none

## Explicit boundary

Approval would authorize certification only of these eight V2 obligations for `civil-procedure-service-process-notice`. It would not approve complete Rule 4 doctrine, the rest of Civil Procedure, another subject, the national NextGen curriculum, assessment content, learner evidence, mastery, or readiness.
