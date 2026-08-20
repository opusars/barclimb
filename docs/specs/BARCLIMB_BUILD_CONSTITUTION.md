# BarClimb Build Constitution

**Status:** Authoritative v1 build contract  
**Date:** August 12, 2026  
**Purpose:** This document is the controlling product, architecture, UX, AI, data, monetization, privacy, SEO, testing, deployment, and operations specification for the first production BarClimb application. Codex and human developers may choose implementation details only where this document expressly leaves discretion. They may not silently change product behavior.

---

## 0. Executive build rule

BarClimb is not “done” when routes exist, tests happen to pass, or screens render. It is done only when the integrated product works end-to-end in staging with real non-production provider connections, meets responsive/accessibility/theme requirements, survives failure states, preserves curriculum and learner-data integrity, and passes the milestone gates in this Constitution.

## 0.1 Contract precedence and integration rule

The four authoritative specifications under `docs/specs/` are one integrated contract. Where duplicated language conflicts, the more specific and later-amended requirement controls, provided it does not weaken security, privacy, assessment validity, learner-data integrity, curriculum completeness, store-policy compliance, or the multi-client invariants in §120. Codex must surface unresolved contradictions rather than choosing silently.

Public, Free, and Plus experiences may differ in capability and personalization, but they use shared canonical learner, assessment, curriculum, entitlement, publication, and community truth.

The application must be capable of generating revenue at launch through three distinct mechanisms:

1. **BarClimb+ subscriptions** through Stripe.
2. **Google AdSense** as the default external fill for ad-eligible free/public inventory when the site/account is approved and consent permits serving.
3. **BarClimb Direct Sponsorships** sold through the application to approved businesses, law schools, and other appropriate sponsors, with paid direct campaigns taking priority over AdSense in the inventory they purchased.

No engineering decision may compromise assessment validity, learner privacy, public-content quality, or exam simulation fidelity merely to increase ad inventory or AI usage.

---

# PART I — PRODUCT CONSTITUTION

## 1. Product identity

BarClimb is an independent NextGen bar-exam preparation platform centered on assessment rather than courses. It is not an NCBE product and must never imply affiliation, endorsement, or official status.

Primary logged-in navigation:

- **Practice**
- **Simulate**
- **Progress**

Secondary destinations:

- Search
- History
- Account

The app has no mandatory coach-first home screen and no required course/chapter progression. Contextual AI help is embedded in assessments through **Ask BarClimb**.

## 2. Primary modes

### 2.1 Practice

User chooses one assessment family:

- Standalone MCQ
- Integrated Question Set (IQS)
- Performance Task (PT)

Practice offers deliberately limited customization using progressive disclosure.

Common controls:

- Subject: Recommended / Random / specific subject
- Difficulty: Adaptive / Foundational / Exam-level / Stretch

IQS additional control:

- Format: Surprise Me / Balanced / Writing Emphasis / Skills Emphasis

PT additional control:

- Format: Surprise Me / Standard PT / Legal Research PT

Advanced doctrine/rule selection is available behind **Choose a specific topic** and is not shown by default.

### 2.2 Simulate

Simulation offers:

- Full Exam
- Official-length Session
- Mini Simulation

Simulation uses the exam blueprint effective for the learner’s expected exam date. It is timed, grading and tutoring are hidden until submission, and the assembled exam is fully validated and version-pinned before the timer begins.

No live OpenAI call may be required to continue a simulation after the user presses **Begin**.

### 2.3 Progress

Progress answers four questions:

1. How ready am I?
2. What have I actually covered?
3. What can I currently do well or poorly?
4. What should I practice next?

Dashboard shows only the minimum useful metrics. Drill-down exposes subject → doctrine → rule → issue and skill evidence.

---

## 3. Onboarding

Onboarding must be completable in under one minute.

Required fields:

- Exam program (default NextGen UBE)
- Expected exam date or “Not scheduled yet”
- Experience level: Haven’t started / Studying / Previously took a bar exam

V1 is national NextGen UBE only. Onboarding must not ask for jurisdiction, and jurisdiction must not affect v1 recommendations, analytics, assessment generation, or readiness. Any dormant jurisdiction field exists only for an explicitly specified future product version.

Then the primary CTA is **Start Practicing**.

No mandatory diagnostic. An optional baseline session can be recommended later.

---

## 4. Free, visitor, and paid access

All quotas are server-side configurable; React may display limits but may not define them.

### 4.1 Visitor

- Unlimited reading of public indexable content.
- Selected interactive public MCQs.
- One limited public IQS experience where enabled.
- Ads may display.
- No persistent learner analytics unless the visitor intentionally creates an account.

### 4.2 Free account — launch defaults

- 15 standalone MCQs per day.
- 2 IQSs per week.
- 1 validated PT per month.
- 1 Mini Simulation per week.
- Basic history.
- Subject-level analytics.
- Limited contextual Ask BarClimb.
- Ads on eligible surfaces.

### 4.3 BarClimb+

Launch commercial defaults:

- Launch target: $29.99/month, server-configurable and subject to validated unit economics.
- Launch target: $149/six-month plan, server-configurable and subject to validated unit economics.

Includes:

- Expanded reasonable-use practice.
- Adaptive generation where inventory cannot satisfy the need.
- Expanded IQS/PT access.
- Full simulations.
- Rule/issue/skill analytics.
- Coverage, Performance, Confidence, Retention, and Readiness Index.
- Full History.
- Contextual AI.
- No advertising.

The product must not advertise mathematically unlimited AI usage; internal fair-use and abuse limits remain enforceable.

---

# PART II — CURRICULUM AND ASSESSMENT MODEL

## 5. Curriculum principle: graph, not outline

BarClimb must maintain a machine-readable curriculum graph rather than a prewritten commercial outline.

Canonical node types:

- SUBJECT
- DOCTRINE
- RULE
- EXCEPTION
- ISSUE_PATTERN
- SKILL
- FACT_ARCHETYPE
- CONCEPT

Canonical edge types:

- PARENT_OF
- REQUIRES
- EXCEPTION_TO
- LIMITS
- CONTRASTS_WITH
- PREREQUISITE_FOR
- RELATED_TO
- COMMONLY_CONFUSED_WITH
- TESTED_THROUGH
- SUPPORTED_BY

AI may propose nodes and edges but may never silently activate them. Proposed graph changes must carry source provenance and enter a review/validation lifecycle.

## 6. Coverage dimensions

Learner analytics must separately track:

- Subject coverage
- Doctrine coverage
- Rule coverage
- Issue-pattern coverage
- Skill coverage
- Response-format coverage
- Fact-archetype diversity
- Difficulty diversity
- Timed versus untimed evidence

Twenty near-identical MCQs may improve Performance but cannot produce full Coverage.

## 7. Assessment composition model

Canonical assessment family enum:

- STANDALONE_MCQ
- IQS
- PT_STANDARD
- PT_LEGAL_RESEARCH

Canonical response type enum:

- MCQ_SINGLE
- MCQ_MULTI
- SHORT_CONSTRUCTED
- MEDIUM_CONSTRUCTED
- LONG_CONSTRUCTED
- DRAFT
- EDIT
- COUNSEL

Core objects:

- **Matter** — shared factual/legal universe.
- **AssessmentResource** — case, statute, contract, email, testimony, report, pleading, etc.
- **AssessmentUnit** — one scored task.
- **AssessmentSet / AssessmentVersion** — one complete deliverable assessment.

Standalone MCQ = one AssessmentUnit without a larger matter package.  
IQS = Matter + optional Resources + multiple AssessmentUnits.  
Standard PT = Matter + File/Library + substantial task.  
Legal Research PT = Matter + Resources + mixed AssessmentUnits.

---

## 8. Generation must follow a permanent specification

No AI call may generate an assessment before deterministic software decides what the assessment is intended to measure.

Base `GenerationSpecification` required fields:

```text
schema_version
exam_program_id
exam_blueprint_version_id
generation_reason
assessment_family
primary_subject_id
primary_doctrine_ids[]
primary_rule_ids[]
secondary_rule_ids[]
issue_pattern_ids[]
skill_ids[]
difficulty
target_duration_seconds
response_type_composition[]
resource_requirements[]
fact_archetype_id
excluded_fact_archetype_ids[]
excluded_assessment_ids[]
learner_adaptation
inventory_objective
legal_source_requirements[]
validation_profile
publication_eligibility
created_at
spec_hash
```

The specification becomes immutable once generation starts. Repairs create new generation attempt metadata, not a silent mutation of the original spec.

---

## 9. Learner planner and inventory planner

### 9.1 Learner Assessment Planner

Optimizes only for the learner:

- coverage deficit
- performance weakness
- uncertainty
- retention need
- blueprint importance
- response-format diversity
- fact-pattern novelty

Advertising, sponsorship, SEO demand, and content-growth objectives may not affect learner recommendations.

### 9.2 Inventory Planner

Runs independently and optimizes the platform library:

- blueprint-important content gaps
- too few validated items
- weak fact diversity
- weak response-format diversity
- insufficient IQS/PT coverage
- high usage demand
- valuable public-content opportunities that are educationally substantive

It operates under a configurable daily/weekly AI budget.

### 9.3 Assessment Selector

Final runtime sequence:

```text
Need Resolver
→ Desired Assessment Specification
→ Inventory Search
→ Select existing suitable item OR Generate
→ Validate if generated
→ Deliver
```

Existing item scoring weights at launch:

- Pedagogical fit: 40%
- Learner novelty: 20%
- Item reliability: 15%
- Fact-pattern diversity contribution: 10%
- Format diversity contribution: 5%
- Retention usefulness: 5%
- Inventory/public usefulness: 5%

If no existing assessment clears the configurable suitability threshold, generation is allowed.

---

## 10. Inventory growth targets

Reuse must reduce unnecessary AI cost but may never suppress meaningful library growth.

Bootstrap targets for a meaningful rule/issue where the blueprint supports it:

- 8–12 distinct standalone MCQs across difficulty and fact archetypes.
- 3+ meaningful IQSs where integrated testing is appropriate.
- PT coverage where the doctrine/skill combination naturally supports it.

Launch minimum corpus:

- 500 validated MCQs across all tested subjects.
- 50 validated IQSs with materially varied compositions.
- 10 standard PTs.
- 5 Legal Research PTs.
- Every tested subject represented by substantive public hubs and multiple assessment pages.

Inventory counts alone do not create launch readiness; curriculum breadth and reliability gates also apply.

---

# PART III — AI GENERATION, VALIDATION, AND GRADING

## 11. Canonical generation pipeline

```text
Assessment Need Resolver
→ Coverage Planner
→ Generation Specification
→ Inventory Search
→ [reuse if suitable]
→ AI Draft Generator
→ Structural Validator
→ Independent Legal Solver
→ Adversarial Reviewer
→ Repair (maximum 2 cycles)
→ Rubric Finalizer
→ Validated Private Assessment
→ Availability / publication lifecycle
```

A learner may never receive raw first-pass generated content.

## 12. Validation gates

### 12.1 Structural Validator

Must deterministically confirm:

- schema validity
- required fields
- permitted response types
- resource references resolve
- answer-option counts
- no duplicate option IDs
- target length/time bounds
- required rubric presence
- no impossible dependency

Structural validation is pass/fail.

### 12.2 Independent Legal Solver

Receives the problem without the generator’s answer key and independently resolves it.

For MCQs, its conclusion must agree with the canonical key at high confidence. Disagreement triggers repair or rejection.

### 12.3 Adversarial Reviewer

Must explicitly test:

- legal accuracy
- scope compliance
- internal contradiction
- factual sufficiency
- ambiguity
- multiple plausible MCQ answers
- weak distractors
- hidden assumptions
- rubric mismatch
- resource inconsistency
- grading unfairness
- stale or unsupported authority

### 12.4 Repair

Maximum two repair cycles. If still below validation threshold, assessment status becomes `REJECTED` and is never delivered.

---

## 13. AI service boundary

All OpenAI usage flows through a single backend service abstraction. Views/components may not call OpenAI directly.

Required logical services:

- AssessmentGenerator
- IndependentSolver
- AssessmentReviewer
- AssessmentRepairer
- RubricFinalizer
- ConstructedResponseGrader
- GradeVerifier
- ContextTutor
- CurriculumCompiler
- PublicationBuilder
- AggregateInsightGenerator
- PrivacyScrubber

Every AI invocation records:

- provider
- model
- prompt version
- schema version
- input hash
- output hash where appropriate
- latency
- token/input/output usage
- estimated cost
- status
- retry count
- related domain object

Machine-consumed responses must use schema-constrained structured output where supported. Human-facing narrative may be generated only after structured core data is valid.

## 14. AI failure behavior

- Generation failure: inventory fallback first; otherwise retry safely or show a recoverable user message.
- Grading delay: submission remains safe; result can finish asynchronously.
- Validation failure: never deliver the failed item.
- Context tutor failure: core assessment remains usable.
- Simulation: must remain completable without OpenAI after start.

---

## 15. Scoring contract

### 15.1 MCQ

Deterministic scoring against the validated canonical answer key. AI does not decide correctness at learner submission time.

### 15.2 Constructed responses

Candidate rubric dimensions:

- LEGAL_ACCURACY
- ISSUE_IDENTIFICATION
- RULE_IDENTIFICATION
- FACT_SELECTION_USE
- ANALYSIS_REASONING
- TASK_COMPLETION
- AUTHORITY_USE
- ORGANIZATION
- CLIENT_COMMUNICATION
- WRITTEN_COMMUNICATION
- DRAFTING_PRECISION

Each task selects only relevant dimensions with explicit weights totaling 1.0.

Required grading output:

```text
rubric_version
criterion_results[]
overall_score
grading_confidence
strengths[]
omissions[]
legal_errors[]
fact_use_findings[]
feedback
improved_approach
optional_model_response
learner_evidence[]
```

Each criterion result:

```text
criterion_id
raw_score
max_score
normalized_score
reason
student_response_evidence[]
```

If grading confidence falls below threshold, the backend must trigger an independent verification/regrade before marking the grade final.

---

# PART IV — LEARNER INTELLIGENCE

## 16. Evidence model

Every completed unit emits atomic `LearnerEvidence` records mapped to relevant curriculum nodes and dimensions.

Evidence properties include:

- learner
- attempt
- assessment version
- curriculum node
- competency dimension
- normalized score `S_e` in [0,1]
- item reliability
- grading confidence
- difficulty
- timed/untimed
- fact-archetype novelty
- response-format novelty
- timestamp
- evidence weight

## 17. Exposure ledger

`LearnerAssessmentExposure` must track:

- SEEN
- STARTED
- ABANDONED
- SUBMITTED
- ANSWER_REVEALED
- REVIEWED
- REPEATED

with timestamps and assessment version. Selection logic must strongly avoid items whose answer has already been revealed unless intentional spaced repetition is requested.

## 18. Evidence weight v1

For evidence `e`:

```text
W_e = reliability_factor
    × grading_confidence_factor
    × difficulty_factor
    × timing_factor
    × novelty_factor
    × recency_factor
```

Difficulty factors:

- FOUNDATIONAL = 0.85
- EXAM = 1.00
- STRETCH = 1.10

Timing:

- timed = 1.00
- untimed = 0.90

Novelty:

- novel archetype/representation = 1.00
- very recent materially similar exposure may decay toward 0.50

Recency uses exponential decay with a 180-day half-life for current Performance. Retention is calculated separately.

## 19. Performance

Bayesian-style shrinkage prevents one correct answer from becoming “100% mastery.”

Prior mean = 0.50  
Prior evidence weight = 2.0

```text
Performance = 100 × ((2 × 0.50 + Σ(W_e × S_e)) / (2 + ΣW_e))
```

## 20. Coverage

Rule-level Coverage v1 weights:

- child rule/exception/issue coverage = 35%
- issue-pattern diversity = 20%
- fact-archetype diversity = 15%
- response-format diversity = 15%
- skill diversity = 15%

Each component is achieved meaningful distinct targets / required targets, capped at 1.0. Required targets are derived from the curriculum graph and applicable blueprint, not arbitrary question counts.

## 21. Confidence

Base confidence:

```text
base = 1 - exp(-effective_evidence_weight / 6)
```

Multiply by a diversity factor composed of:

- fact diversity
- format diversity
- item reliability
- grading confidence

Return 0–100.

## 22. Retention

Only evidence meaningfully separated from prior exposure materially improves Retention.

Intervals:

- <24h: minimal retention evidence
- 1–6d: early
- 7–20d: meaningful
- 21–59d: strong
- 60+d: long-term

Successful delayed retrieval is weighted more heavily than same-session repetition.

## 23. Readiness Index

For each applicable blueprint competency:

```text
Competency = 0.50 × Performance
           + 0.20 × Retention
           + 0.20 × Coverage
           + 0.10 × Confidence
```

Then blueprint-weight competencies into the Readiness Index.

Display a separate **Evidence Completeness** measure. If evidence completeness is below the configured threshold, the app must say there is insufficient evidence for a stable Readiness Index rather than fabricate precision.

This is an instructional index, not a probability of passing.

## 24. Mastery labels

Launch thresholds:

- UNASSESSED: Coverage < 5
- INSUFFICIENT_EVIDENCE: Confidence < 40
- DEVELOPING: Performance < 70 or Retention < 55
- PROFICIENT: P ≥ 70, Coverage ≥ 60, Confidence ≥ 65, Retention ≥ 55
- STRONG: P ≥ 85, Coverage ≥ 75, Confidence ≥ 80, Retention ≥ 70
- AT_RISK: previously Proficient/Strong with material recent deterioration

Thresholds are versioned configuration and may later be empirically recalibrated.

## 25. Learner-algorithm test vectors

The codebase must include golden deterministic tests at minimum:

### Vector A — one correct exam-level timed MCQ

Input: one reliable item, score 1.0, reliability 0.90, confidence 1.0, exam difficulty, timed, novel, current.  
Expected: Performance rises above 50 but remains materially below 100; Confidence remains low; status remains INSUFFICIENT_EVIDENCE.

### Vector B — repeated same archetype

Input: five correct questions with materially identical fact archetype in same session.  
Expected: Performance rises; Coverage fact-diversity component remains low; Confidence lower than five diverse items.

### Vector C — diverse delayed success

Input: correct MCQ + short response + later IQS written application across distinct archetypes and 14-day interval.  
Expected: Coverage, Confidence, and Retention all rise materially more than same-session repetitions.

### Vector D — high historic performance but stale retention

Input: previously strong evidence, no reassessment for long interval, then weak recent response.  
Expected: current Performance and/or Retention decline; status may become AT_RISK.

### Vector E — 100% current answers but low coverage

Expected: UI may show strong current performance with “insufficient evidence” or lower Coverage; it must not label mastery Strong solely from accuracy.

Exact numerical expected values must be frozen in `LEARNER_MODEL.md` once implementation uses concrete factor functions.

---

# PART V — RELIABILITY, CHALLENGES, AND LEGAL FRESHNESS

## 26. Reliability lifecycle

User-facing labels:

- Emerging
- Developing
- Reliable
- Established

Internal lifecycle:

- EXPERIMENTAL
- DEVELOPING
- RELIABLE
- ESTABLISHED
- UNDER_REVIEW
- RETIRED

Initial validated assessment begins around internal reliability 55.

Reliability formula v1 weights:

- system validation = 30%
- statistical stability = 20%
- item discrimination = 15%
- usefulness feedback = 10%
- challenge record = 10%
- scoring/grading consistency = 10%
- completion anomaly = 5%

Minimum attempt gates:

- EXPERIMENTAL: <25 meaningful attempts
- DEVELOPING: 25–99
- RELIABLE: ≥100 and reliability ≥75
- ESTABLISHED: ≥500 and reliability ≥85 with no unresolved serious quality signal

Votes may influence reliability but may never determine legal validity.

## 27. Legal freshness

Separate enum:

- CURRENT
- REVIEW_DUE
- REVALIDATION_REQUIRED
- STALE
- SUPERSEDED

An item may be highly reliable but barred from scored simulations if freshness is not CURRENT.

Source changes trigger impact scans through graph provenance.

## 28. Voting and challenge flow

Public/practice feedback:

- 👍 Helpful
- 👎 Problem

A negative vote opens structured categories:

- incorrect law
- ambiguous
- multiple answers
- insufficient facts
- confusing wording
- grading wrong
- inconsistent resource
- outdated
- other

Challenge lifecycle:

```text
OPEN
→ AUTO_REVALIDATING
→ RESOLVED_NO_CHANGE
or RESOLVED_UPDATED
or ASSESSMENT_RETIRED
```

Serious thresholds may immediately remove the assessment from scored simulations pending review.

## 29. Regrade

Constructed grades support **Request Regrade**.

A fresh grader receives the response and rubric without the original grade. Material disagreement triggers reconciliation. Original and revised grades remain auditable.

---

# PART VI — PUBLICATION, SEO, AND SHARING

## 30. Publishing flywheel

Validated practice interactions may create durable public educational assets.

Publishing lifecycle:

```text
VALIDATED_PRIVATE
→ PUBLICATION_ELIGIBLE
→ PRIVACY_REVIEW
→ CONTENT_REVIEW
→ PUBLIC_NOINDEX
→ PUBLIC_INDEXABLE
```

Exceptional:

- UNDER_REVIEW
- RETIRED_REDIRECT
- RETIRED_GONE

Student response publication requires explicit permission. Question publication does not require publishing the learner response.

Public pages may include:

- original BarClimb question
- resources
- canonical answer/explanation
- anonymous permitted student response
- AI rubric assessment
- strengths and omissions
- improved response
- rule/issue tested
- common mistakes
- aggregate BarClimb insight
- reliability label and attempt count
- related practice
- share action

## 31. SEO taxonomy

Canonical root:

- `/nextgen/`

Examples:

- `/nextgen/mcq/`
- `/nextgen/iqs/`
- `/nextgen/performance-tasks/`
- `/nextgen/contracts/`
- `/nextgen/contracts/modification/`
- `/nextgen/contracts/modification/preexisting-duty/`
- distinct assessment URLs beneath the relevant taxonomy

One canonical hub per substantive doctrine/rule. Do not create thin keyword variants.

Public SEO pages are Django-rendered HTML. React may mount interactive islands but indexability cannot depend on an empty JavaScript shell.

## 32. SEO requirements

Every indexable page requires:

- unique title
- useful meta description
- canonical URL
- crawlable internal links
- Open Graph/social metadata
- breadcrumb structured data where appropriate
- index state
- substantive publisher content independent of ads

Required infrastructure:

- `robots.txt`
- sitemap index
- subject sitemap
- doctrine sitemap
- assessment sitemap
- Search Console verification
- redirect rules for merged/retired pages

Internal search-result pages are `noindex` by default.

## 33. Shareability

Public pages provide:

- copy link
- native share where supported
- social preview image/metadata

Private learner results may generate a privacy-safe share card containing type, subject, score/performance, and date but never the actual written answer unless explicitly chosen.

---

# PART VII — ADVERTISING AND DIRECT SPONSORSHIP

## 34. Advertising invariant

Advertising may monetize free/public use but may never affect:

- generation targets
- grading
- learner evidence
- readiness
- curriculum selection
- recommendations
- question content

Advertising receives only the minimum contextual information required for placement. Learner intelligence never receives advertiser preferences.

## 35. Ad decision order

For every ad-eligible slot:

```text
if BarClimb+ → NO AD
else if surface not ad-eligible → NO AD
else if eligible paid direct campaign → DIRECT SPONSOR
else if AdSense enabled/approved/consent-permitted → ADSENSE
else → HOUSE AD
```

Direct, AdSense, and house creatives never stack in the same slot.

## 36. AdSense

AdSense is the default external fill when approved and enabled.

Requirements:

- policy-compliant placement
- reserved layout space to reduce CLS
- no ads disguised as answers/navigation
- no ads inside login/error/dead-end screens
- CMP/consent integration where required
- `ads.txt` deployment/configuration

AdSense approval is an external dependency and cannot block launch. Direct campaigns and house ads must work independently.

## 37. Direct sponsor marketplace

Public destination:

- `/advertise/`

Sponsor workflow:

```text
Create sponsor account
→ Organization profile
→ Choose campaign product
→ Choose targeting/context
→ Choose dates
→ Upload approved-format creative
→ Preview mobile/desktop
→ Submit
→ Automated checks
→ Human approval
→ Stripe Checkout
→ SCHEDULED
→ ACTIVE
→ reporting
→ COMPLETED
```

Direct sponsorship is a launch requirement.

## 38. Sponsor products

Launch products:

- SITEWIDE_SPONSOR
- SUBJECT_SPONSOR
- ASSESSMENT_SPONSOR
- SIMULATION_SPONSOR
- FEATURED_HUB_SPONSOR

Direct campaigns are fixed-price packages, not CPC auctions at launch.

## 39. Direct targeting restrictions

Allowed contextual targeting:

- page family
- subject
- assessment family
- device class
- coarse geography only if later legally/business justified

Prohibited targeting:

- learner score
- weakness
- readiness
- answers
- coverage
- email/account identity
- private history

Sponsors receive aggregate campaign metrics only.

## 40. Creative rules

Direct creatives are controlled BarClimb components containing only approved fields such as:

- image
- advertiser name
- headline
- short body
- CTA
- approved destination URL

No advertiser JavaScript, arbitrary HTML, pixels, or executable code.

All direct ads display standardized **Sponsored** or **Advertisement** labels.

## 41. Ad placement rules

### Public SEO pages

- top/intro-adjacent slot after meaningful publisher content
- natural inline slot(s)
- desktop rail where appropriate
- lower-page slot

### MCQ practice

Ads may appear between question groups or on setup/results, never adjacent to answer choices in a misleading way.

### IQS

Ads may appear between completed units or after grading; never inside the legal matter/resources.

### PT

Ads may appear before start or after submission/results; never inside File/Library/editor.

### Simulation

No ad during a live timed section. Free users may see sponsorship/ad inventory before a section, during an actual break, or after completion.

## 42. Sponsor campaign states

- DRAFT
- SUBMITTED
- AUTOMATED_REVIEW
- PENDING_APPROVAL
- APPROVED_AWAITING_PAYMENT
- PAID
- SCHEDULED
- ACTIVE
- COMPLETED
- REJECTED
- PAUSED
- CANCELLED
- EXHAUSTED
- REFUND_REQUIRED

Campaign delivery is paced to avoid consuming inventory too early. Underdelivery must be surfaced to admin for extension, credit, or refund.

---

# PART VIII — PRIVACY, CONSENT, AND USER RIGHTS

## 43. Privacy principles

- collect minimum identity data
- never send unnecessary identity/payment data to OpenAI
- separate learner analytics from business analytics
- require explicit permission for public anonymous use of learner responses
- support response withdrawal
- honor applicable opt-out/privacy signals
- no hidden advertiser access to learner data

## 44. Theme and preference storage

Theme enum:

- SYSTEM
- LIGHT
- DARK

Default = SYSTEM.

Authenticated users: persisted server-side.  
Anonymous visitors: local/browser preference, treated as functional/necessary preference storage.

No visible flash of the wrong theme on page load.

## 45. Cookie categories

- STRICTLY_NECESSARY
- FUNCTIONAL
- ANALYTICS
- ADVERTISING
- AD_PERSONALIZATION

Cookie controls must support Accept Optional / Reject Optional / Customize with no dark-pattern asymmetry.

Permanent footer link: **Cookie Settings**.

## 46. Privacy/GPC

System must be capable of honoring Global Privacy Control where applicable and recording the observed state. Consent version and source must be auditable.

## 47. User privacy controls

Account area includes:

- publication consent
- email preferences
- cookie/privacy preferences
- request data export
- request correction
- request deletion
- request removal of published response

## 48. Data retention defaults

- Anonymous session: maximum 30 days unless converted.
- Security logs: target 12 months unless incident/legal need requires longer.
- Raw AI prompt/response bodies: minimize retention; operational metadata may persist longer.
- Learner history: retained while account exists unless deletion applies.
- Sponsor/accounting data: retained as required for legitimate business/tax/legal needs.
- Ad impression/click detail: aggregate where possible; avoid indefinite learner-associated records.

---

# PART IX — UI, DESIGN SYSTEM, AND RESPONSIVENESS

## 49. UI philosophy

Modern transactional-app feel inspired by the clarity, action-first interaction, and progressive disclosure of contemporary high-volume consumer web applications. Do not copy Domino’s branding or colors.

Principles:

- action first
- large clear primary choices
- progressive disclosure
- minimal chrome
- dense legal content only where useful
- strong perceived speed
- quiet simulation mode
- modern light and dark modes
- mobile-first interaction quality without reducing desktop workspace

## 50. App shell

Desktop:

`BarClimb | Practice | Simulate | Progress | Search | Account`

Mobile:

- compact top bar
- bottom nav: Practice / Simulate / Progress
- Search and Account in header/menu

No persistent large side navigation at launch.

## 51. Screen behavior

### Home

1. Recommended Next
2. large Practice / Simulate / Progress actions
3. lightweight recent activity/exam date

### MCQ

- centered readable question column
- large touch-safe answers
- predictable submit CTA
- post-submit explanation and Ask BarClimb

### IQS desktop

- Matter/resources pane
- Question/response pane

Tablet: collapsible resources.  
Mobile: tabs/switcher Matter / Resources / Question.

### PT desktop

- resizable Resources | Writing Workspace

Tablet: dual pane when viable.  
Mobile: Task / Resources / Response switcher.

### Simulation

- minimal chrome
- server-authoritative timer display
- progress
- flag
- navigator
- submit

## 52. Design tokens

Spacing scale based on 4px:

- 4, 8, 12, 16, 24, 32, 48, 64

Radius:

- controls: 8px
- panels/cards: 12px
- large marketing surfaces: 16px

Motion:

- fast: 120–180ms
- normal: 180–260ms

Button variants:

- PRIMARY
- SECONDARY
- GHOST
- DANGER

All must implement default, hover, active, focus, disabled, and loading states.

Typography baseline: Inter when available with robust system sans-serif fallback. Legal reading regions prioritize comfortable line length and line height.

## 53. Responsive acceptance widths

Critical screens must be verified at:

- 320px
- 375px
- 390px
- 768px
- 1024px
- 1440px

Pass conditions:

- no page horizontal overflow
- no clipped CTA
- no timer overlap
- no unreadable resource pane
- no ad covering content
- no grading overflow
- no broken theme
- touch-safe controls

## 54. Accessibility

Target WCAG 2.2 AA.

Mandatory:

- keyboard operation
- semantic markup
- visible focus
- sufficient contrast
- no color-only status communication
- screen-reader labels
- reduced-motion support
- zoom/reflow compatibility
- accessible timer announcements without disruptive repetition

---

# PART X — DATA MODEL

## 55. Django domain modules

```text
accounts/
curriculum/
assessments/
learning/
simulations/
quality/
publishing/
advertising/
privacy/
ai/
billing/
communications/
analytics/
common/
```

## 56. Canonical models and constraints

The following are minimum required models. Field names may be extended but not replaced without updating this Constitution and `DATA_MODEL.md`.

### accounts.User

Use Django’s supported user abstraction with email-based login behavior implemented consistently. Do not create a second identity table for sponsors; use roles/memberships.

### accounts.LearnerProfile

Fields:

- user OneToOne
- exam_program FK
- jurisdiction nullable string/code — dormant future-extension field; v1 onboarding does not ask for jurisdiction and national NextGen planning must not depend on it
- expected_exam_date nullable date
- experience_level enum
- timezone
- theme enum default SYSTEM
- onboarding_completed bool
- created_at / updated_at

Indexes: expected_exam_date where useful.

### curriculum.ExamProgram

- key unique
- name
- active

### curriculum.ExamBlueprintVersion

- program FK
- version unique per program
- effective_from
- effective_until nullable
- status enum DRAFT/ACTIVE/RETIRED
- requirements JSON validated by schema
- source_provenance JSON

Unique constraint: `(program, version)`.

### curriculum.LegalSource

- id UUID
- source_type
- title
- authority
- source_url/citation
- effective_from/effective_until
- checksum
- status
- retrieved_at
- supersedes nullable self-FK
- metadata JSON

Index: checksum, status, effective dates.

### curriculum.DoctrineNode

- id UUID
- stable_key unique
- node_type enum
- canonical_name
- short_name
- jurisdiction nullable — future exam-scope extension only; national NextGen v1 content, assessment generation, analytics, and readiness do not depend on it
- lifecycle_state
- created_at

### curriculum.DoctrineNodeVersion

- node FK
- version integer
- description
- scope_status
- source_provenance JSON
- compiler_metadata JSON
- effective_from/effective_until

Unique `(node, version)`.

### curriculum.DoctrineEdge

- source_node FK
- target_node FK
- relationship enum
- provenance JSON
- confidence decimal
- status PROPOSED/ACTIVE/REJECTED/RETIRED

Unique active semantic edge across `(source_node,target_node,relationship)`.

### assessments.Assessment

Stable identity:

- id UUID
- assessment_family enum
- canonical_slug nullable unique where public identity applies
- created_at

### assessments.AssessmentVersion

Immutable content snapshot:

- assessment FK
- version integer
- generation_spec FK nullable for human-seeded fixtures
- blueprint_version FK
- legal_freshness enum
- lifecycle_state enum
- title
- rendered_content JSON
- canonical_answer JSON
- created_at

Unique `(assessment, version)`.

No update-in-place after learner delivery; corrections create new version.

### assessments.Matter

- assessment_version OneToOne/FK
- title
- facts structured text/JSON
- matter_type

### assessments.AssessmentResource

- assessment_version FK
- order
- resource_type
- title
- body text nullable
- object_storage_key nullable
- metadata JSON

Unique `(assessment_version, order)`.

### assessments.AssessmentUnit

- assessment_version FK
- order
- response_type
- prompt
- max_score
- target_seconds nullable
- metadata JSON

Unique `(assessment_version, order)`.

### assessments.AnswerOption

- unit FK
- stable_key
- order
- text
- is_correct bool stored only server-side/authorized serializers

Unique `(unit, stable_key)` and `(unit, order)`.

### assessments.GenerationSpecification

- id UUID
- schema_version
- exam_program FK
- blueprint_version FK
- generation_reason
- assessment_family
- specification JSON validated by family schema
- spec_hash unique
- created_at
- immutable bool/default true

### assessments.Rubric

- assessment_version FK
- version
- total_points
- schema JSON

Unique `(assessment_version, version)`.

### assessments.RubricCriterion

- rubric FK
- stable_key
- dimension enum
- weight decimal
- max_points
- description
- scoring_guidance JSON

Rubric weights must sum to 1.0 within numeric tolerance.

### assessments.ValidationRun

- assessment_version FK
- validation_type
- status
- ai_invocation nullable FK
- findings JSON
- confidence
- created_at

### assessments.AssessmentReliability

One current row per AssessmentVersion:

- assessment_version OneToOne
- numeric_score
- state enum
- meaningful_attempts
- challenge_count
- unresolved_serious_challenge bool
- last_calculated_at

### learning.Attempt

- id UUID
- learner FK
- assessment_version FK
- mode PRACTICE/SIMULATION/PUBLIC_TRIAL
- status enum
- started_at
- submitted_at nullable
- timed bool
- server_deadline nullable
- version integer for optimistic concurrency
- grading_status

Index learner/date, assessment/version.

### learning.AttemptResponse

- attempt FK
- unit FK
- response_text nullable
- selected_option_keys JSON nullable
- draft_version integer
- saved_at
- submitted bool

Unique `(attempt, unit)`.

### learning.Grade

- attempt FK
- rubric FK nullable
- overall_score
- normalized_score
- confidence
- status
- grading_version
- created_at

Multiple grade records may exist for regrades; one designated current/final.

### learning.GradeCriterionResult

- grade FK
- criterion FK
- raw_score
- normalized_score
- reason
- evidence_spans JSON

### learning.LearnerEvidence

- learner FK
- attempt FK
- assessment_version FK
- doctrine_node FK
- competency_dimension
- normalized_score
- evidence_weight
- item_reliability
- grading_confidence
- difficulty
- timed
- fact_archetype_key nullable
- response_type
- occurred_at

Index `(learner, doctrine_node, competency_dimension, occurred_at)`.

### learning.LearnerState

Materialized current estimate:

- learner FK
- doctrine_node FK
- performance
- coverage
- confidence
- retention
- mastery_state
- evidence_completeness
- model_version
- calculated_at

Unique `(learner, doctrine_node)`.

### learning.LearnerAssessmentExposure

- learner FK
- assessment_version FK
- state enum
- first_seen_at
- last_seen_at
- answer_revealed_at nullable
- repeat_count

Unique `(learner, assessment_version)`.

### learning.Recommendation

- learner FK
- recommendation_type
- target_specification JSON
- rationale_data JSON
- status ACTIVE/ACCEPTED/DISMISSED/EXPIRED
- created_at
- expires_at nullable

### simulations.Simulation

- learner FK
- blueprint_version FK
- simulation_type FULL/SESSION/MINI
- status
- assembled_at
- started_at
- completed_at
- current_section
- server_deadline state
- version

### simulations.SimulationAssessment

- simulation FK
- assessment_version FK
- section_number
- order

Unique `(simulation, section_number, order)`.

### quality.Vote

- user FK
- assessment_version FK
- value HELPFUL/PROBLEM
- created_at

Unique `(user, assessment_version)` current vote.

### quality.Challenge

- reporter FK nullable for anonymous allowed cases
- assessment_version FK
- attempt nullable FK
- category
- details
- state
- severity
- resolution JSON
- created_at/updated_at

### quality.RegradeRequest

- requester FK
- grade FK
- state
- resulting_grade nullable FK
- created_at

### publishing.Publication

- assessment FK
- canonical_path unique
- publication_state enum
- current_publication_version FK nullable
- index_state enum
- published_at

### publishing.PublicationVersion

- publication FK
- source_assessment_version FK
- rendered_html/content fields
- privacy_scan_status
- content_quality_status
- canonical_metadata JSON
- created_at

### publishing.PublishedResponse

- publication_version FK
- source_attempt FK
- consent_record FK
- anonymized_response
- withdrawn_at nullable

### publishing.AggregateInsight

- doctrine_node FK
- insight_type
- statement
- supporting_metrics JSON
- minimum_sample_size
- generated_at
- validation_status

### advertising.SponsorOrganization

- name
- website
- status
- billing_contact
- created_at

### advertising.SponsorMembership

- organization FK
- user FK
- role

Unique `(organization,user)`.

### advertising.AdPlacement

- key unique
- surface
- description
- allowed_formats JSON
- active

### advertising.SponsorProduct

- key unique
- name
- placement_rules JSON
- active

### advertising.SponsorRate

- product FK
- currency
- amount
- impression_cap nullable
- active_from/active_until

### advertising.SponsorCampaign

- organization FK
- product FK
- state
- targeting JSON validated against permitted targeting schema
- start_at/end_at
- purchased_impressions nullable
- delivered_impressions
- stripe_checkout_session_id nullable unique
- stripe_payment_intent_id nullable
- created_at

### advertising.SponsorCreative

- campaign FK
- state
- advertiser_name
- headline
- body
- cta
- destination_url
- object_storage_key nullable
- review_notes

### advertising.AdImpression / AdClick

Store minimal event data, campaign/placement, coarse device/context, timestamp; do not store learner educational state.

### privacy.ConsentRecord

- user nullable FK
- anonymous_id nullable
- consent_version
- necessary bool
- functional bool
- analytics bool
- advertising bool
- ad_personalization bool
- gpc_observed bool
- region_basis
- created_at

### privacy.PublicationConsent

- user FK
- version
- allow_anonymous_public_use bool
- granted_at
- withdrawn_at nullable

### privacy.DataRightsRequest

- user FK
- request_type ACCESS/CORRECT/DELETE/EXPORT/PUBLICATION_REMOVE
- state
- submitted_at
- completed_at
- notes

### ai.PromptDefinition / PromptVersion

Prompt family stable identity and immutable versions.

### ai.AIInvocation

- service_name
- provider
- model
- prompt_version FK
- schema_version
- input_hash
- output_hash
- token counts
- estimated_cost
- latency_ms
- status
- retry_count
- domain_reference_type/id
- created_at

### billing.Plan

- key unique
- name
- entitlements JSON
- active

### billing.Subscription

- user FK
- plan FK
- purchase_source STRIPE/APPLE/GOOGLE
- external_customer_id nullable
- external_subscription_id nullable
- external_original_transaction_or_purchase_token nullable
- external_product_id
- status
- current_period_start/end
- cancel_at_period_end
- grace_or_billing_retry_state nullable
- revoked_or_refunded_at nullable
- last_provider_event_at
- verified_at

Uniqueness constraints must prevent one provider subscription/original transaction from attaching to multiple BarClimb accounts without explicit audited recovery. Provider-specific details may live in normalized child records when appropriate.

### billing.Entitlement

- user FK
- key
- value JSON
- source
- effective_from/effective_until

### billing.ProviderEvent

- provider
- external_event_id unique within provider
- event_type
- external_subscription/original-transaction reference nullable
- created_at_provider
- received_at
- processed_at nullable
- processing_status
- payload_hash
- signature/verification_status

Provider-specific receipt/transaction metadata may be stored in private normalized child records. Raw sensitive provider payload retention must be minimized. A dedicated `StripeEvent` table is allowed as an implementation detail but may not make Stripe the canonical subscription model.

### communications.EmailPreference

- user FK
- category
- enabled

### communications.EmailDelivery

- user nullable FK
- template_key
- provider_message_id nullable
- status
- sent_at

### analytics.ProductEvent

- user nullable FK
- anonymous_id nullable
- event_name
- properties JSON restricted to non-learner-sensitive business analytics
- occurred_at

---

# PART XI — API CONTRACT

## 57. API rules

- Versioned REST base `/api/v1/`.
- Session-cookie authentication for logged-in browser app.
- CSRF protection.
- Object ownership checks on every learner-owned resource.
- Server is authoritative for entitlements, timers, lifecycle state, grades, and recommendations.
- React never sends “mastery” or “needs” as authoritative learner state.

## 58. Core endpoints

### Identity/account

- `GET /api/v1/me/`
- `PATCH /api/v1/me/`
- `GET /api/v1/me/privacy/`
- `PATCH /api/v1/me/privacy/`

### Practice

- `GET /api/v1/practice/options/`
- `POST /api/v1/practice/plan/`
- `POST /api/v1/practice/start/`

`practice/plan` returns resolved spec preview and whether an existing assessment is immediately available; it must not reveal answer keys.

### Assessments

- `GET /api/v1/assessments/{id}/`

Serializer permissions must exclude canonical answer/rubric internals before submission.

### Attempts

- `POST /api/v1/attempts/`
- `GET /api/v1/attempts/{id}/`
- `PUT /api/v1/attempts/{id}/responses/{unit_id}/`
- `POST /api/v1/attempts/{id}/submit/`
- `GET /api/v1/attempts/{id}/results/`

Writes include optimistic-concurrency version.

### Context AI

- `POST /api/v1/attempts/{id}/ask/`

Must enforce quota and scope conversation to current assessment context plus permitted learner evidence.

### Quality

- `POST /api/v1/assessments/{id}/vote/`
- `POST /api/v1/assessments/{id}/challenge/`
- `POST /api/v1/grades/{id}/regrade/`

### Progress

- `GET /api/v1/progress/`
- `GET /api/v1/progress/subjects/`
- `GET /api/v1/progress/nodes/{id}/`
- `GET /api/v1/recommendations/next/`

### History

- `GET /api/v1/history/`
- `GET /api/v1/history/{attempt_id}/`

### Simulation

- `POST /api/v1/simulations/plan/`
- `POST /api/v1/simulations/start/`
- `GET /api/v1/simulations/{id}/`
- `PUT /api/v1/simulations/{id}/responses/{unit_id}/`
- `POST /api/v1/simulations/{id}/section/submit/`
- `POST /api/v1/simulations/{id}/submit/`
- `GET /api/v1/simulations/{id}/results/`

### Billing

- `POST /api/v1/billing/checkout/`
- `POST /api/v1/billing/portal/`
- `POST /api/v1/webhooks/stripe/`

### Sponsor

- `GET/POST /api/v1/sponsor/organizations/`
- `GET/POST /api/v1/sponsor/campaigns/`
- `PATCH /api/v1/sponsor/campaigns/{id}/`
- `POST /api/v1/sponsor/campaigns/{id}/submit/`
- `POST /api/v1/sponsor/campaigns/{id}/checkout/`
- `GET /api/v1/sponsor/campaigns/{id}/report/`
- `POST /api/v1/sponsor/creatives/upload-url/`

### Privacy rights

- `POST /api/v1/privacy/requests/`
- `GET /api/v1/privacy/requests/`

---

# PART XII — BACKGROUND JOBS AND IDEMPOTENCY

## 59. Celery task families

- `curriculum.ingest_source`
- `curriculum.compile_candidates`
- `curriculum.impact_scan`
- `assessments.generate`
- `assessments.independent_solve`
- `assessments.adversarial_review`
- `assessments.repair`
- `assessments.finalize_rubric`
- `assessments.revalidate`
- `learning.grade_constructed`
- `learning.verify_grade`
- `learning.materialize_evidence`
- `learning.recalculate_state`
- `learning.generate_recommendation`
- `publishing.evaluate_candidate`
- `publishing.privacy_scrub`
- `publishing.render_page`
- `publishing.generate_aggregate_insights`
- `advertising.recalculate_pacing`
- `advertising.complete_campaigns`
- `communications.send_email`
- `privacy.execute_export`
- `privacy.execute_deletion`
- `inventory.plan_growth`

## 60. Idempotency key rules

Every externally replayable or expensive side effect must have deterministic idempotency.

Examples:

- assessment generation: `generation_spec:{spec_hash}:attempt:{repair_index}`
- grade: `attempt:{attempt_id}:rubric:{rubric_version}:grader:{grading_version}`
- learner-state recalculation: `learner:{id}:node:{id}:evidence_watermark:{max_evidence_id}`
- Stripe webhook: provider `event.id` unique
- sponsor checkout fulfillment: `stripe_event:{event_id}` plus campaign state gate
- email: `template:{key}:user:{id}:domain_event:{event_id}` when event-driven

Retryable jobs use exponential backoff and bounded retries. A lost worker acknowledgement may never double-charge, duplicate publication, or pay twice for the same AI result.

---

# PART XIII — STATE MACHINES

## 61. Assessment lifecycle

```text
DRAFT
→ VALIDATING
→ VALIDATED_PRIVATE
→ AVAILABLE
→ PUBLICATION_ELIGIBLE
→ PUBLISHED
```

Exceptional:

- UNDER_REVIEW
- REVALIDATION_REQUIRED
- RETIRED
- REJECTED

Invalid transitions must raise domain errors, not silently coerce state.

## 62. Attempt lifecycle

```text
CREATED
→ IN_PROGRESS
→ SUBMITTED
→ GRADING (constructed only)
→ GRADED
→ FINAL
```

Alternative:

- ABANDONED

Submitted responses are immutable except through explicit regrade/versioned correction mechanics.

## 63. Simulation lifecycle

```text
CREATED
→ ASSEMBLED
→ IN_PROGRESS
→ SECTION_BREAK
→ IN_PROGRESS
→ SUBMITTED
→ SCORING
→ COMPLETE
```

Expired server deadline triggers automatic section/exam submission according to blueprint/session rules.

## 64. Publication lifecycle

```text
PRIVATE
→ ELIGIBLE
→ PRIVACY_REVIEW
→ CONTENT_REVIEW
→ PUBLIC_NOINDEX
→ PUBLIC_INDEXABLE
```

Exceptional:

- UNDER_REVIEW
- RETIRED_REDIRECT
- RETIRED_GONE

## 65. Sponsor campaign lifecycle

As defined in §42. Payment and activation are webhook-authoritative.

---

# PART XIV — PERMISSION MATRIX

## 66. Roles

- ANONYMOUS
- LEARNER_FREE
- LEARNER_PLUS
- SPONSOR_MEMBER
- SPONSOR_ADMIN
- STAFF_REVIEWER
- STAFF_ADMIN
- SUPERUSER

## 67. Permission principles

| Capability | Anonymous | Free | Plus | Sponsor | Staff |
|---|---:|---:|---:|---:|---:|
| Read public pages | Yes | Yes | Yes | Yes | Yes |
| Public trial MCQ | Limited | Yes | Yes | N/A | Yes |
| Persistent practice | No | Quota | Expanded | No | Test/Admin |
| Full advanced analytics | No | No | Yes | No | Support-limited |
| View another learner response | No | No | No | No | Only authorized support/admin need |
| Sponsor campaign create | No | No | No | Yes | Yes |
| View learner intelligence for targeting | No | Own only | Own only | Never | Restricted support/admin |
| Approve sponsor creative | No | No | No | No | Yes |
| Publish/retire content | No | No | No | No | Yes |
| View canonical answers before submission | No | No | No | No | Authorized staff/tests only |

Support/admin access to learner content must be auditable and least-privilege.

---

# PART XV — FRONTEND COMPONENT CONTRACT

## 68. React application areas

```text
app/
practice/
simulation/
progress/
history/
search/
account/
billing/
privacy/
sponsor/
components/
design-system/
api/
theme/
```

## 69. Required design-system primitives

- AppShell
- TopNav
- MobileBottomNav
- Button
- IconButton
- LinkButton
- Card/Panel
- Modal/Dialog
- Drawer/Sheet
- Tabs
- SegmentedControl
- Select
- Checkbox/Radio
- TextInput
- TextArea/EditorShell
- Badge
- Tooltip
- Toast
- Skeleton
- EmptyState
- ErrorState
- ProgressBar
- Metric
- ThemeSwitcher
- ConsentBanner/PreferenceCenter
- AdSlot
- SponsoredCreative

## 70. Assessment components

- AssessmentHeader
- Timer
- SaveStatus
- QuestionNavigator
- FlagControl
- MatterView
- ResourceList
- ResourceViewer
- MCQSingle
- MCQMulti
- ConstructedResponseEditor
- DraftEditor
- IQSWorkspace
- PTWorkspace
- SubmissionConfirm
- ResultSummary
- CriterionBreakdown
- ExplanationPanel
- AskBarClimbPanel
- ChallengeDialog
- RegradeDialog

## 71. Progress components

- ReadinessCard
- EvidenceCompleteness
- SubjectCoverageList
- DoctrineDrilldown
- RuleDrilldown
- SkillBreakdown
- Coverage/Performance/Confidence/Retention indicators
- RecommendationCard

No component may assume light mode, desktop-only space, or paid entitlement.

---

# PART XVI — AUTOSAVE, OFFLINE, AND CONCURRENCY

## 72. Autosave

- 750ms debounce after typing stops.
- periodic safety save for long writing.
- UI states: Saving / Saved / Offline / Retrying.
- server returns new attempt version on write.

Long responses maintain a local browser recovery copy in addition to server persistence.

## 73. Optimistic concurrency

Writes include expected attempt version. On stale version:

1. client receives 409 with authoritative current state/version;
2. safe non-conflicting response content may be reconciled;
3. destructive conflict requires visible recovery choice, never silent data loss.

Simulation timer and submission state are always server-authoritative.

---

# PART XVII — PROVIDERS AND DEPLOYMENT

## 74. Version baseline at build kickoff

Pin exact patch versions in lockfiles at kickoff while staying within these approved lines unless a blocking compatibility/security issue requires a documented change:

- Python 3.13.x
- Django 5.2 LTS latest security patch
- Django REST Framework 3.16.x
- React 19.2.x
- TypeScript 5.x compatible with chosen toolchain
- Celery 5.6.x
- PostgreSQL supported by chosen Heroku Postgres plan

Dependencies are pinned; unattended major upgrades are prohibited.

## 75. Heroku topology

Processes:

```text
web: Django/ASGI-or-WSGI production server as selected and documented
worker: Celery worker
release: python manage.py migrate && required safe release checks
```

Optional scheduled jobs use Heroku Scheduler or a dedicated beat process only when justified.

Environments:

- local
- review app
- staging
- production

Staging must be a persistent near-production environment.

## 76. Object storage

Amazon S3 is required only for durable file/object assets:

- sponsor creative images
- exports
- uploaded/downloadable assessment resource files
- generated media/documents where applicable

Structured assessment/learner data remains in PostgreSQL.

Local development uses local filesystem storage; staging/production use S3 through Django storage abstraction.

## 77. OpenAI

- real API exercised in staging during assessment-engine development
- mocks/fixtures used for deterministic unit tests
- central service abstraction only
- structured outputs for machine-consumed artifacts
- configurable model mapping per AI service
- cost/latency/error telemetry

Production may not launch if the real staging generation + validation + grading golden flows have not passed.

## 78. Stripe

Use Stripe Checkout/Billing and verified webhooks.

Required flows:

- monthly subscription
- six-month subscription
- customer portal
- cancel/reactivate
- payment failure
- entitlement expiration
- direct sponsor one-time Checkout
- refund/admin correction
- duplicate/replayed webhook

Browser redirect success is never the source of truth.

## 79. SendGrid

Required:

- staging integration
- domain authentication before production
- template identifiers/config
- bounce/failure handling where available

## 80. Sentry and logs

Use Sentry for Django/React exceptions and appropriate performance traces. Scrub learner responses and PII from third-party telemetry.

Heroku structured logs remain primary operational log stream.

---

# PART XVIII — ENVIRONMENT VARIABLE CONTRACT

## 81. Required configuration groups

A committed `.env.example` and `ENVIRONMENT.md` must enumerate at minimum:

### Django

- DJANGO_SETTINGS_MODULE
- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- APP_ENV
- ALLOWED_HOSTS
- CSRF_TRUSTED_ORIGINS
- PUBLIC_BASE_URL

### Database/cache

- DATABASE_URL
- REDIS_URL / managed KVS URL

### OpenAI

- OPENAI_API_KEY
- OPENAI_PROJECT_ID where used
- OPENAI_GENERATION_MODEL
- OPENAI_SOLVER_MODEL
- OPENAI_REVIEW_MODEL
- OPENAI_GRADING_MODEL
- OPENAI_TUTOR_MODEL
- AI_DAILY_BUDGET_USD

### Stripe

- STRIPE_SECRET_KEY
- STRIPE_PUBLISHABLE_KEY
- STRIPE_WEBHOOK_SECRET
- STRIPE_PLUS_MONTHLY_PRICE_ID
- STRIPE_PLUS_SIX_MONTH_PRICE_ID

### SendGrid

- SENDGRID_API_KEY
- DEFAULT_FROM_EMAIL
- SUPPORT_EMAIL

### S3

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME
- AWS_REGION

### Ads

- ADSENSE_ENABLED
- ADSENSE_CLIENT_ID
- ADSENSE_SLOT_* as required
- DIRECT_ADS_ENABLED

### Sentry

- SENTRY_DSN
- SENTRY_ENVIRONMENT

Secrets never enter source control.

---

# PART XIX — EMAILS AND COMMUNICATIONS

## 82. Launch email templates

Account:

- Verify email
- Welcome
- Password reset

Learning:

- Constructed response graded when delayed
- Optional weekly progress digest
- Exam-date reminders

Billing:

- subscription confirmation
- payment problem
- cancellation confirmation

Sponsor:

- campaign submitted
- creative approved/rejected
- payment confirmed
- campaign started/completed
- underdelivery action

Privacy:

- request received/completed
- deletion confirmation

Email failure may never alter authoritative billing or learning state.

---

# PART XX — OBSERVABILITY AND BUSINESS ANALYTICS

## 83. Required telemetry

Monitor:

- API latency
- 4xx/5xx rate
- Celery queue depth
- failed/retried jobs
- AI latency/error/cost
- generation rejection rate
- grading latency
- Stripe webhook failures
- email failures
- sponsor underdelivery
- challenge spikes
- DB connection/health

## 84. First-party product analytics

Canonical product events include:

- signup_completed
- onboarding_completed
- practice_started
- assessment_started
- assessment_submitted
- iqs_completed
- pt_completed
- simulation_started
- simulation_completed
- recommendation_accepted
- upgrade_viewed
- upgrade_started
- subscription_started
- subscription_cancelled
- sponsor_campaign_created
- sponsor_campaign_paid
- sponsor_campaign_completed

Product-event payloads may not contain learner answer text or private competency detail.

---

# PART XXI — CONVERSION AND REVENUE OPERATIONS

## 85. Upgrade UX

Free users must understand value before encountering pressure to upgrade.

Allowed upgrade moments:

- when quota is reached
- after receiving a useful result
- when opening locked advanced analytics
- when selecting a paid-only full simulation/PT capability
- in house-ad inventory

Prohibited:

- interrupting a live timed section
- hiding already-earned grading results behind a surprise paywall
- deceptive countdowns or false scarcity

Upgrade UI must clearly compare Free and Plus and invoke the platform-appropriate purchase path: Stripe Checkout on Web, StoreKit on iOS, and Google Play Billing on Android. Purchase-source details may differ, but Django remains authoritative for entitlement.

## 86. Conversion instrumentation

Track funnel:

```text
public visitor
→ interactive trial
→ signup
→ first completed assessment
→ 3 completed assessments
→ upgrade view
→ checkout start
→ paid
```

Also track churn/cancellation and return usage. Funnel instrumentation must exist before marketing spend.

## 87. Sponsor sales operations

Direct sponsor system must be commercially operable even with zero automation beyond the product flow.

Admin must be able to:

- create sponsor organization manually
- create campaign on behalf of sponsor
- issue/record Stripe payment link/Checkout
- approve creative
- pause/extend/refund
- export campaign report

This ensures direct revenue can be sold through outbound sales immediately, not only discovered via self-service.

## 88. Support and feedback

Launch requires:

- visible support/contact path
- in-app report/problem flow
- sponsor support path
- billing support path
- privacy request path

Support tickets may initially flow to a controlled support email rather than requiring a full help-desk product.

---

# PART XXII — SECURITY

## 89. Threat categories

Security implementation and tests must cover:

- credential/session attacks
- CSRF
- cross-user object access
- admin privilege escalation
- prompt injection
- model-output XSS
- AI-cost abuse
- mass assessment scraping
- sponsor malicious URL/creative
- unsafe upload
- SSRF/link abuse
- fake Stripe success
- webhook spoof/replay
- S3 public leakage
- PII logging leakage

## 90. Required controls

- secure HttpOnly session cookies
- SameSite policy appropriate to architecture
- CSRF protection
- strict authorization
- rate limiting
- content sanitization
- CSP
- safe external-link handling
- upload MIME/size validation
- private S3 default
- Stripe signature verification
- idempotency
- feature flags for risky subsystems
- audit logging for sensitive admin actions

---

# PART XXIII — PERFORMANCE

## 91. Performance budgets

Launch targets:

- ordinary non-AI API p95 < 500ms under expected launch load
- public HTML optimized for Core Web Vitals, especially stable layout
- ad containers reserve layout space
- cached/inventory practice starts feel immediate
- long AI operations asynchronous
- public pages ship minimal client JavaScript

A feature that works but creates visibly poor responsiveness or avoidable layout shift fails Definition of Done.

---

# PART XXIV — TESTING

## 92. Test layers

### Unit

- learner formulas
- coverage planner
- recommendation ranking
- inventory selector
- reliability
- legal freshness
- state transitions
- entitlement logic
- ad decisioning
- pacing
- privacy eligibility

### Schema/contract

Every AI schema must test valid, invalid, missing, extra, malformed, and repair scenarios.

Every API endpoint tests authentication/authorization and invalid state transitions.

### Integration

- real DB
- Celery eager/worker pathways as appropriate
- OpenAI mock contract and controlled staging real calls
- Stripe webhook replay
- S3 upload flow
- SendGrid sandbox/staging

### E2E golden flows

1. Anonymous MCQ → signup → saved progress.
2. Free MCQ practice → quota → upgrade CTA.
3. IQS → constructed grade → evidence → recommendation.
4. PT → autosave/recovery → grade.
5. Challenge → revalidation.
6. Regrade → reconciliation.
7. Simulation start → no OpenAI dependency → completion.
8. Subscription purchase → webhook → Plus entitlement → ads disappear.
9. Cancellation/failed payment → entitlement transitions.
10. Sponsor create → approve → pay → active direct ad → report.
11. Published page → vote/problem → under review.
12. Published learner response withdrawal.
13. Privacy export/deletion.
14. Theme system/light/dark/system.
15. Offline/reconnect/stale version recovery.

### Concurrency/idempotency

- duplicate submit
- duplicate Stripe webhook
- worker retry
- duplicate generation request
- stale autosave conflict
- two-tab attempt edit

---

# PART XXV — BROWSER, ACCESSIBILITY, AND MANUAL QA

## 93. Supported clients

Launch support target:

- latest two practical major versions: Chrome, Safari, Firefox, Edge
- iPhone Safari
- Android Chrome
- iPad Safari
- Android tablet Chrome

Manual Safari testing required before production launch.

## 94. Manual UX acceptance

A human must complete every golden workflow on staging. Automated tests do not replace manual verification of:

- reading comfort
- touch usability
- responsiveness
- split panes
- theme quality
- ad placement
- upgrade flow
- sponsor flow
- timer behavior
- error/recovery clarity

---

# PART XXVI — RELEASE, ROLLBACK, AND FEATURE FLAGS

## 95. Release discipline

Every production release must:

- pass CI
- pass applicable staging E2E
- have migrations reviewed
- have release notes
- have rollback instructions when stateful risk exists
- avoid unbounded background migrations in release phase

## 96. Feature flags

Server-managed feature flags required for at least:

- PT generation
- LRPT generation
- public publishing
- AdSense
- direct ads
- sponsor self-service
- new learner-model version
- new grading engine
- new prompt versions
- experimental UI

Risky functionality may deploy dark before activation.

## 97. Rollback

Code rollback must not assume database rollback is safe. Contract/migration changes should use expand/contract patterns when necessary. Assessment and rubric versions remain immutable, reducing semantic rollback risk.

---

# PART XXVII — ADMIN AND OPERATIONS

## 98. Django Admin required actions

- approve/reject curriculum proposals
- inspect source provenance
- trigger source impact scan
- force assessment revalidation
- retire assessment
- publish/unpublish
- resolve challenges
- change configurable free limits
- change inventory targets/budgets
- toggle feature flags
- inspect AI cost/invocations
- retry failed jobs
- inspect learner-state anomalies
- manage subscription correction with audit trail
- manage sponsor/rates/campaigns
- approve/reject creative
- pause/extend/refund campaign
- manage publication consent/removal
- select active exam blueprint

---

# PART XXVIII — REPOSITORY CONSTITUTION

## 99. Required authoritative documents

The four controlling product specifications committed under `docs/specs/` are:

- `BARCLIMB_BUILD_CONSTITUTION.md`
- `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md`
- `BARCLIMB_PRODUCT_EXPERIENCE_NETWORK_SPEC.md`
- `BARCLIMB_NATIVE_PLATFORM_SPEC.md`

The repository additionally maintains implementation-facing documents derived from, and subordinate to, those specs, including as they become applicable:

- `PRODUCT_SPEC.md`
- `ARCHITECTURE.md`
- `DATA_MODEL.md`
- `CURRICULUM_GRAPH.md`
- `LEARNER_MODEL.md`
- `ASSESSMENT_ENGINE.md`
- `AI_CONTRACTS.md`
- `GRADING.md`
- `API_CONTRACT.md`
- `PUBLICATION_AND_SEO.md`
- `ADVERTISING.md`
- `DESIGN_SYSTEM.md`
- `PRIVACY_ARCHITECTURE.md`
- `SECURITY.md`
- `TESTING.md`
- `ENVIRONMENT.md`
- `DEPLOYMENT.md`
- `RELEASE_NOTES.md`
- `PROJECT_HANDOFF.md`

The chat-independent continuity package is mandatory:

- `RECOVERY_START_HERE.md`
- `AGENTS.md`
- `SPEC_MANIFEST.json`
- `docs/project/PROJECT_STATE.json`
- `PROJECT_HANDOFF.md`
- `BUILD_HISTORY.md`
- `DECISION_LOG.md`
- `TEST_LEDGER.md`
- `PROVIDER_STATUS.md`
- `CLIENT_PARITY.md`
- `RELEASE_NOTES.md`
- `RECOVERY_PLAYBOOK.md`
- continuity validator + CI job.

Implementation docs may explain concrete code but may not silently override the four product specs.

## 100. Codex operating rules

1. Read authoritative docs before architecture changes.
2. Never silently change a product requirement.
3. Update docs in the same commit when a contract changes.
4. Run relevant tests before committing.
5. Record exact tests/results.
6. Never declare completion with failing applicable tests.
7. Never bypass validation merely to satisfy a test.
8. Review migrations before commit.
9. Do not casually rewrite historical migrations.
10. Never weaken authorization to make UI work.
11. Frontend state never overrides server authority.
12. Replayable side effects require idempotency.
13. Each material milestone gets coherent commits.
14. `PROJECT_HANDOFF.md` must permit continuation without conversation history.

---

# PART XXIX — BUILD MILESTONES AND RELEASE TRAINS

## 101. Release strategy and terminology

BarClimb uses a **Web-first commercial release strategy with first-class native architecture from the beginning**.

- **Web GA** — the first public commercial release of BarClimb on `barclimb.com`, using the Django backend and React Web client. Web GA may occur before public App Store or Google Play availability.
- **Native GA — iOS** — the first public App Store release of the iOS client after the native release gate passes.
- **Native GA — Android** — the first public Google Play release of the Android client after the native release gate passes.
- **Product architecture** — one server-authoritative BarClimb system shared by Web, iOS, and Android. Web-first release sequencing never authorizes a Web-only domain model, assessment engine, learner model, entitlement system, publication system, or URL taxonomy.

Web GA is the first revenue milestone. Native development remains active throughout the build and must prove high-risk assumptions early enough that Web architecture cannot drift into a later native rewrite.

A native store/account/signing delay is **not a Web GA blocker** when the documented native architecture, capability contracts, shared backend semantics, internal-build/deep-link foundations, and unresolved external dependencies are honestly recorded. Conversely, Web GA does not permit BarClimb to claim iOS or Android availability before the corresponding store release is actually available.

## 102. Launch trains

### Train A — Foundation and native-risk proof
Milestones 1–2.

### Train B — Complete learner loop
Milestones 3–5.

### Train C — Exam fidelity
Milestone 6.

### Train D — Trust and learning network
Milestones 7–8.

### Train E — Distribution and Web commerce
Milestone 9.

### Train F — Web GA hardening and native-release preparation
Milestone 10.

After Web GA, iOS and Android proceed through their separate Native GA gates under the Native Platform Specification. Native release work may overlap later Web milestones when it does not destabilize the Web GA critical path.

## 103. Milestone 1 — Multi-client foundation + continuity

Deliver:

- repository continuity package and CI validator
- Django/DRF/PostgreSQL foundation
- React Web shell
- React Native/Expo iOS and Android shells
- shared TypeScript contract packages
- Celery/managed-KVS runtime foundation
- auth/session/CSRF and native credential architecture
- local/review/staging runtime topology
- theme/design-system primitives
- S3 abstraction and Sentry/privacy skeletons at the appropriate foundation depth
- deep-link/native-routing skeleton and internal-build risk proof
- Apple/Google project prerequisites begun early enough to expose external blockers

Gate: clean recovery works; staging foundation is usable; Web and native shells target one backend contract; critical native risks are either proven or recorded as explicit external blockers. Public store release is not required for Web GA at this milestone.

## 104. Milestone 2 — Curriculum core + automated coverage assurance

Deliver the official-source registry, scope manifest, doctrine graph, Rule Obligation compiler/catalog, source discovery/reconciliation, certifications, drift/impact analysis, and strict validation/admin audit required by the Learning & Assessment Specification.

Gate: official scope maps bidirectionally; CORE obligations have required authority/reconciliation evidence; deterministic compilation/certification checks pass.

## 105. Milestone 3 — Assessment/OpenAI + presentation contracts

Deliver Generation Specifications, assessment domain/inventory, central AI services, solver/reviewer/repair/rubric flows, presentation-schema validation, assessment-scope confirmation, golden fixtures, and real staging OpenAI behavior.

Gate: generated MCQ/IQS/PT/LRPT fixtures pass full validation and no raw unvalidated assessment can reach a learner.

## 106. Milestone 4 — Cross-platform Practice + discovery loop

Deliver MCQ/IQS/PT/LRPT Practice, attempts/autosave/history/contextual Ask, schema renderer, annotations, grading renderer, anonymous Instant Practice, and Web/native contract parity at the implementation level reached by each client.

**Web GA requirement:** all launch Practice families and critical interactions must be complete on Web.

**Native preparation requirement:** the same presentation schema, API contracts, capability registry, and persistence semantics must remain native-compatible; missing native UI capability is tracked explicitly in the client capability manifest and cannot be papered over with a Web-only schema.

Gate: complete Web Practice workflows pass in staging; native renderer risk paths remain proven and tracked toward Native GA.

## 107. Milestone 5 — Learner intelligence + My BarClimb

Deliver exposure/evidence math, recommendations, Progress, server-authored projections, Study Sessions, Review/Suggested Review, Repair Plans, Search/private overlays, and signed-in orchestration.

Gate: golden vectors pass exact learner-state/recommendation outputs; Web signed-in journeys are complete for Web GA; projection contracts remain client-neutral for native consumption.

## 108. Milestone 6 — Simulation

Deliver blueprint assembly, preassembly/version pinning, server timers, section transitions, exam-software profile, scoring/results, and no-AI-after-start invariant.

Gate: full Web staging simulation survives OpenAI disabled after Begin. Native simulation remains a Native GA requirement and must consume the same assembled simulation contract rather than a fork.

## 109. Milestone 7 — Quality + publication foundation

Deliver votes/challenges/regrades, reliability/legal freshness, inventory planning, publication foundation, aggregate insights, and public-response consent/withdrawal.

Gate: intentionally flawed seeded content is detected/reviewed and removed from eligibility; publication truth remains client-independent.

## 110. Milestone 8 — Learning network + growth loops

Deliver public profiles, responses, qualified views, learning signals, discussions, reputation, Circles, sharing, moderation, and Web notification surfaces; preserve native notification/deep-link/community contracts for Native GA.

Gate: Web network safety/moderation and core community E2E pass. Native UGC moderation UI and push behavior are separate Native GA blockers, not Web GA blockers.

## 111. Milestone 9 — Public platform + Web commerce

Deliver SEO/search/sharing/sitemaps/privacy/CMP, Stripe Web subscriptions, provider-neutral entitlements, direct sponsor marketplace, Web ad stack, SendGrid, and public acquisition loops.

Web Stripe may never become the entitlement source of truth. `purchase_source=STRIPE` resolves through the same Subscription/Entitlement domain later used by Apple and Google purchase sources.

Gate: Web Plus purchase/entitlement works, ads disappear for authenticated Plus, sponsor flow works from verified Web payment events, public pages remain substantive with ads disabled, and native clients can later consume the same entitlement capability projection without domain migration.

## 112. Milestone 10 — Coverage completion + Web GA hardening + native-release preparation

Deliver:

- security/accessibility/cost/load/failure/cross-device/SEO hardening
- launch inventory completion and CoverageReleaseSnapshot
- production Web provider configuration
- Web billing/privacy/support/rollback readiness
- moderation readiness for public Web community
- final Web golden journeys
- native internal/release-candidate preparation at the strongest available level
- explicit Native GA remaining-work ledger for iOS and Android
- continuity cold-recovery drill

Gate: **Web GA Launch Checklist (§115) passes.** iOS/Android public store approval is not required for Web GA. Any unresolved native work must remain visible in `CLIENT_PARITY.md`, provider/store ledgers, and the Native GA checklist; Web GA may not downgrade those obligations.

---

# PART XXX — DEFINITION OF DONE

## 113. Feature definition of done

A feature is complete only when all applicable gates pass:

- functionality end-to-end
- data integrity
- provider staging integration
- unit tests
- API/integration tests
- E2E
- responsive 320–1440
- light mode
- dark mode
- accessibility
- loading/error/empty/failure states
- security/authorization
- privacy/consent
- performance budget
- documentation
- staging deployment
- manual browser verification
- handoff updated

No “backend complete, UI later” may be called feature-complete. For a Web-GA-scoped feature, Web UI may complete before the native concrete UI only when the portable domain/API/presentation contract is already native-compatible and the remaining native work is explicitly tracked for Native GA; “mobile later” may never justify a Web-only contract that requires later redesign.

---

# PART XXXI — LAUNCH AND CASH-GENERATION GATES

## 114. Revenue readiness

The application is technically revenue-ready only if:

### Subscription

- live Stripe products/prices exist
- live webhook verified
- checkout → entitlement works
- cancellation/failure paths work
- ads disappear for Plus

### AdSense

- AdSense integration is technically correct
- policy/CMP configuration is ready
- site approval is obtained OR house/direct fallback operates

AdSense approval is not required to launch the application, but AdSense revenue cannot be assumed until Google approves the site/account.

### Direct sponsorship

- `/advertise/` is live
- sponsor onboarding works
- admin can manually create campaigns for outbound sales
- Stripe one-time checkout works
- campaign pacing/reporting works
- creative approval is operational

## 115. Web GA Production Launch Checklist

All applicable Web GA items must pass:

1. all ten acceptance milestones through the Web GA gate
2. production Heroku Web pipeline configured
3. database backup/recovery procedure tested
4. production S3 permissions verified where Web GA uses S3
5. OpenAI production limits/budget alarms configured
6. Stripe live Web webhook test completed
7. SendGrid domain authentication and live delivery test completed
8. Sentry production environment configured with privacy scrubbing
9. privacy/cookie settings verified
10. Terms, Privacy Policy, Cookie Policy, Community Standards, and advertising/sponsor terms available as applicable
11. minimum launch inventory and strict curriculum coverage gates achieved
12. no subject materially empty
13. public SEO hubs substantive and internally linked
14. direct sponsor/house fallback works even if external ad approval is unavailable
15. Web paid upgrade/cancellation/grace/downgrade paths tested
16. support contact tested
17. accessibility manual audit of critical Web flows complete
18. mobile Safari and responsive critical Web flows complete
19. Web simulation completes with OpenAI disabled after start
20. rollback drill documented
21. public Web UGC moderation/report/block flows operational
22. native architecture invariants, capability manifests, deep-link contracts, provider-neutral entitlement model, and current iOS/Android parity gaps are documented and not regressed
23. no marketing or product surface falsely claims App Store/Google Play availability before the applicable Native GA

**Not Web GA blockers by themselves:** App Store approval, Google Play approval, native store billing/restore completion, or native public release, provided the native architecture-preservation requirements and early-risk proofs in this Constitution are satisfied and remaining work is explicitly tracked.

## 116. Native GA release gates

Each native platform has an independent public release gate defined by the Native Platform Specification. iOS/Android release requires its own critical assessment parity, device/runtime recovery, deep links, push, UGC safety, privacy/deletion, provider-neutral entitlement consumption, platform billing/restore where offered, observability, store metadata/review readiness, and production release verification.

---

# PART XXXII — ADVERSARIAL BUILD REVIEW AND FINAL SPEC UPDATES

## 117. Issues discovered in final review

A final adversarial review identified five risks that would have produced a “working” but commercially weak application if left implicit. They are now incorporated as requirements:

### 117.1 External ad approval risk

**Risk:** assuming AdSense revenue exists on launch day.  
**Resolution:** AdSense is default external fill when approved, but house ads and BarClimb Direct are fully operational independently. Launch does not depend on Google approval.

### 117.2 Conversion not engineered

**Risk:** excellent study engine with no defined free→paid funnel.  
**Resolution:** upgrade moments, quota behavior, conversion events, and checkout handoff are now explicit (§85–86).

### 117.3 Direct sponsor marketplace dependent on organic discovery

**Risk:** sponsor self-service exists but generates no sponsor revenue.  
**Resolution:** admin-assisted campaign creation and outbound-sales support are mandatory (§87). The product can sell sponsorship directly from launch.

### 117.4 Launch content too thin

**Risk:** AI engine works, but public site lacks enough trusted content for users, SEO, and AdSense review.  
**Resolution:** launch inventory minimums and curriculum breadth gates are mandatory (§10, §115).

### 117.5 Release process creates fragile production

**Risk:** Codex produces features but no safe release/rollback discipline.  
**Resolution:** staging, feature flags, release checks, migration discipline, and rollback contracts are mandatory (§95–97).

## 118. Remaining non-engineering uncertainties

No build specification can guarantee “printing cash.” Revenue depends on variables outside software correctness, including:

- acquiring qualified traffic
- Google AdSense approval and RPMs
- conversion rate from free to Plus
- willingness of sponsors to buy inventory
- search ranking and time-to-index
- pricing sensitivity
- perceived assessment quality
- actual bar-prep outcomes and trust

The app is therefore **ready to build as a revenue-capable product**, not guaranteed to produce a specific revenue level.

These uncertainties are handled through instrumentation and launch operations rather than additional architectural complexity.

---

# PART XXXIII — BUSINESS VALIDATION AFTER LAUNCH

## 119. Required first 90-day metrics

Track at minimum:

### Acquisition

- organic sessions
- public assessment page entrances
- share-origin traffic
- signup conversion from public interactive trial

### Activation

- first assessment completion
- three-assessment completion
- week-one return rate

### Learning usage

- MCQ/IQS/PT completion
- recommendations accepted
- simulation starts/completions

### Monetization

- free→Plus conversion
- checkout conversion
- paid churn
- ARPPU
- AdSense revenue/RPM when active
- direct sponsor revenue
- sponsor renewal/repeat purchase

### Cost

- AI cost per free active user
- AI cost per paid active user
- AI cost per generated reusable assessment
- gross contribution by plan

No pricing or quota change should be made without looking at both learning value and unit economics.

---

# PART XXXIV — VERIFIED PLATFORM ASSUMPTIONS (AUGUST 2026)

These are implementation assumptions verified against current official documentation and should be rechecked at build kickoff if materially delayed:

- Django 5.2 is an LTS line; use the latest security patch in that line at kickoff.
- React official docs report 19.2 as current.
- Celery official docs report the 5.6 line as current stable.
- Django REST Framework 3.16 supports Django 5.2/Python 3.13.
- Stripe subscription lifecycle must be webhook-aware and webhooks must be signature-verified.
- Heroku supports config vars, separate process types, pipelines/review apps, and release-phase commands.
- Google AdSense requires publisher-policy-compliant placements and does not guarantee site approval.

Provider assumptions belong in `ENVIRONMENT.md`/`ARCHITECTURE.md` and are not an excuse to bypass pinned dependency review.

---

# FINAL BUILD VERDICT

**BUILD/RELEASE STRATEGY VERDICT: READY TO CONTINUE — Web GA may be prioritized as the first commercial release while native architecture remains first-class and iOS/Android proceed through their separate Native GA gates.**

The specification is sufficiently complete that implementation agents should not need to invent a major product decision, data lifecycle, learner algorithm, monetization mechanism, provider integration strategy, release-sequencing rule, responsive behavior, or definition of completion.

The remaining decisions during implementation should be ordinary engineering choices—library-level details, query optimization, component internals, and low-level code organization—provided they conform to this Constitution.

**Commercial verdict:** The application is architected to be cash-generating from launch through subscription, AdSense when approved, and direct sponsorship. No responsible specification can guarantee revenue before traffic, conversion, sponsor demand, and assessment trust are observed. The app is now designed to measure and optimize those variables instead of merely hoping for them.


# PART XXXV — WEB-FIRST RELEASE AMENDMENT (2026-08-15)

## 120. Governing release-sequencing amendment

This section is a later product decision and controls over older language that implies Web, iOS, and Android must become publicly available on the same date. The product remains multi-client by architecture; only public distribution sequencing changes.

### 120.1 Web-first does not mean Web-only

The following canonical invariants apply before and after every release gate:

- one Django/server-authoritative backend and account/identity model;
- one curriculum and Rule Obligation system;
- one immutable AssessmentVersion truth and one learner-evidence/readiness system;
- one publication/community identity and moderation system;
- one provider-neutral Subscription/Entitlement truth into which Stripe, Apple, and Google purchase lifecycles map;
- canonical HTTPS identifiers and URLs that remain useful on Web and can later resolve through Universal/App Links;
- renderer-independent assessment/domain schemas and server responses expressed as portable contracts rather than Web-rendered UI;
- portable attempt/workspace, annotation, recovery, and cross-device state;
- explicit Web/iOS/Android capability and parity manifests.

The following are forbidden even before Native GA:

- DOM-shaped assessment/domain schemas that native must later translate or replace;
- Web session semantics as the only account model;
- Stripe IDs or Web checkout state as entitlement truth;
- browser-only learner persistence;
- Web-generated HTML as the authenticated API contract;
- canonical URLs that cannot resolve to future Universal/App Links;
- desktop-only PT/IQS data models;
- Web-only community, moderation, publication, privacy, deletion, or notification semantics;
- release decisions that delete or postpone already-required native technical-risk proofs merely to accelerate Web GA.

### 120.2 What may be sequenced later

The following concrete native deliverables may complete after Web GA without compromising the architecture when their contracts already exist and gaps are tracked:

- final native UI polish/parity;
- store screenshots/listings/review submissions;
- TestFlight/Play production rollout;
- StoreKit/Google Play purchase and restore production verification;
- final push-notification production setup;
- platform-specific accessibility/device-matrix completion;
- native public community moderation UI completion;
- native full-simulation release certification.

### 120.3 Release-status truth

Web, iOS, and Android each expose an explicit release status. “BarClimb is live” may refer to Web GA only when the context clearly points to the website. Marketing must not imply native availability until that platform is actually released.

### 120.4 Three-scenario Web GA gate

Web GA must prove these primary journeys without creating parallel domain truth:

1. anonymous SEO visitor → substantive public learning → Instant Practice → signup and ownership-safe claim;
2. authenticated learner → My BarClimb → Practice, Progress, Search, History, and Repair;
3. Plus learner → ad-free deeper practice, simulation, analytics, contextual Ask, repair, and planning.

The same canonical contracts must remain consumable by iOS and Android as those clients advance to their independent Native GA gates.
