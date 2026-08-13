# BarClimb Build Constitution

**Status:** Authoritative v1 build contract  
**Date:** August 12, 2026  
**Purpose:** This document is the controlling product, architecture, UX, AI, data, monetization, privacy, SEO, testing, deployment, and operations specification for the first production BarClimb application. Codex and human developers may choose implementation details only where this document expressly leaves discretion. They may not silently change product behavior.

---

## 0. Executive build rule

BarClimb is not “done” when routes exist, tests happen to pass, or screens render. It is done only when the integrated product works end-to-end in staging with real non-production provider connections, meets responsive/accessibility/theme requirements, survives failure states, preserves curriculum and learner-data integrity, and passes the milestone gates in this Constitution.

## 0.1 Contract precedence and integration rule

The four authoritative specifications are one integrated contract:

1. `BARCLIMB_BUILD_CONSTITUTION.md`
2. `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md`
3. `BARCLIMB_PRODUCT_EXPERIENCE_NETWORK_SPEC.md`
4. `BARCLIMB_NATIVE_PLATFORM_SPEC.md`

Where duplicated language conflicts, the **more specific and later-dated/amended requirement controls**, provided it does not weaken security, privacy, assessment validity, learner-data integrity, curriculum completeness, or store-policy compliance. Codex must surface unresolved contradictions before implementation rather than choosing silently.

Cross-scenario behavior must be implemented through shared canonical domain models and server-authoritative projections; public, Free, and Plus experiences may differ in capability and personalization, but they may not maintain incompatible copies of learner, assessment, curriculum, entitlement, publication, or community truth.

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
- Jurisdiction where useful
- Expected exam date or “Not scheduled yet”
- Experience level: Haven’t started / Studying / Previously took a bar exam

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
- jurisdiction nullable
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

Provider-agnostic subscription identity:

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

Normalized immutable event envelope for STRIPE/APPLE/GOOGLE:

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
- anonymous attempt claim: `anon_claim:{anonymous_attempt_id}:user:{user_id}`
- StudySession planning: `study_plan:{user_id}:{planner_version}:{input_watermark}` when deterministic for a request
- Review suggestion acceptance: `review_suggestion:{suggestion_id}:user:{user_id}:accept`
- RepairPlan adaptation: `repair:{plan_id}:evidence_watermark:{max_evidence_id}`
- Apple/Google purchase lifecycle: provider transaction/purchase-token event identifier + account state gate
- notification delivery: `notification:{notification_id}:channel:{channel}:destination:{destination_hash}`

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

## 63.1 StudySession lifecycle

```text
PLANNED → ACTIVE ↔ PAUSED → COMPLETED
                     ↘ ABANDONED
PLANNED/PAUSED/ACTIVE → DISMISSED when safe
```

Completed StudySession evidence is never rolled back by replanning. Replanning affects only future/uncompleted steps.

## 63.2 RepairPlan lifecycle

```text
PLANNED → ACTIVE → ADAPTING → ACTIVE → COMPLETED
             ↘ PAUSED             ↘ ABANDONED/DISMISSED
```

Adaptation events are append/audit records and may not rewrite historical grades.

## 63.3 Subscription/entitlement lifecycle

Provider events normalize to server-authoritative effective states such as:

```text
INACTIVE → ACTIVE ↔ GRACE/BILLING_RETRY → ACTIVE
                         ↘ PAST_DUE → EXPIRED
ACTIVE → CANCELED_PENDING_EXPIRY → EXPIRED
ACTIVE/GRACE → REVOKED/REFUNDED when provider-verified
```

Effective capability transitions occur at documented safe boundaries and never delete learner work.

## 63.4 Community moderation lifecycle

Content may move through VISIBLE / LIMITED / HIDDEN_PENDING_REVIEW / REMOVED, with moderator actions and appeals auditable. User-account restrictions are separate from content state.

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

Server-side permission/capability rules:

### Anonymous
- may read canonical public pages, eligible public community content, and public profiles;
- may use bounded Instant Practice/public trial inventory and bounded public Ask;
- may not create persistent learner analytics until a valid claim after signup;
- may not publish, comment, react, follow, bookmark, join Circles, or view private learner data;
- may see eligible advertising.

### Free learner
- owns persistent learner analytics, History, baseline Progress, and configured Practice/IQS/PT access;
- may read and, with consent/eligibility, publish own public response;
- may comment/reply/react/follow/bookmark and join/create enabled Circles;
- may use limited contextual Ask and configured previews of advanced analysis;
- does not receive Full Simulation unless an explicit promotion/feature rule grants it;
- may see eligible advertising.

### Plus learner
- has all ordinary learner/community permissions available to Free;
- receives expanded/fair-use Practice, PT/LRPT, Full Simulation, advanced analysis/repair/planning, and expanded contextual Ask according to effective capabilities;
- is globally ad/upsell-free while authenticated;
- receives **no** advantage in scoring, mastery math, public ranking, reaction weight, reputation, moderation, or content distribution.

### Sponsor
- may manage authorized sponsor organization/campaign resources;
- may read public pages/community like any public visitor;
- may never access learner intelligence, private responses, social graph, readiness, or private targeting data.

### Staff
- access is role-scoped and least-privilege;
- authorized staff may perform review/admin/test actions required by their role;
- learner/private-content access is restricted to legitimate support/review/admin need and audited;
- canonical answers before normal authorization state are limited to authorized staff/test systems.

Across all roles:
- eligible published learner responses are public according to publication state; private learner responses/history/readiness remain owner-private except audited authorized staff need;
- canonical content publication/retirement and sponsor creative approval require staff authority;
- all permissions are enforced server-side;
- effective capability may narrow access further due to quota, content lifecycle, region/provider state, moderation restriction, billing grace/expiry, or feature flags;
- clients never grant access merely because a control is visible.

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

Upgrade UI must clearly compare Free and Plus and invoke the platform-appropriate purchase path: Stripe Checkout on web, StoreKit on iOS, and Google Play Billing on Android. Purchase-source details may differ, but Django remains authoritative for entitlement.

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
- anonymous Instant Practice
- public Ask BarClimb
- public publishing
- community comments/reactions/follows
- Study Circles
- Study Sessions/My BarClimb orchestration version
- Weakness Repair / Simulation Repair
- advanced History patterns / writing trajectory
- authenticated public-page private overlays
- AdSense web
- AdMob native
- direct ads
- sponsor self-service
- native client capability rollout where necessary
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
- inspect effective HomeProjection/recommendation rationale
- inspect/manage StudySession/RepairPlan anomalies without falsifying learner evidence
- configure Suggested Review/Study Session policy thresholds
- inspect anonymous discovery claims and anti-replay anomalies
- inspect search-index health and private-overlay cache headers
- inspect effective entitlement/capability by account/purchase source
- manage notification delivery/preferences troubleshooting
- manage community moderation/reputation model versions
- inspect Web/iOS/Android feature parity/flags

---

# PART XXVIII — REPOSITORY CONSTITUTION

## 99. Required authoritative documents

The **four controlling product specifications** committed under `docs/specs/` are:

- `BARCLIMB_BUILD_CONSTITUTION.md`
- `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md`
- `BARCLIMB_PRODUCT_EXPERIENCE_NETWORK_SPEC.md`
- `BARCLIMB_NATIVE_PLATFORM_SPEC.md`

The repository additionally maintains implementation-facing documents derived from, and subordinate to, those specs as the codebase emerges, including at minimum:

- `ARCHITECTURE.md`
- `DATA_MODEL.md`
- `API_CONTRACT.md` / generated OpenAPI artifact
- `CURRICULUM_GRAPH.md`
- `LEARNER_MODEL.md`
- `ASSESSMENT_ENGINE.md`
- `AI_CONTRACTS.md`
- `SECURITY.md`
- `TESTING.md`
- `ENVIRONMENT.md`
- `DEPLOYMENT.md`

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

# PART XXIX — BUILD MILESTONES

The ten acceptance milestones are organized into six launch trains. Work may proceed in parallel only when dependencies are satisfied and continuity records remain accurate. Native, community, coverage, and commerce are launch requirements, not post-launch roadmap items.

## 101. Milestone 1 — Multi-client foundation + continuity

Deliver:

- repository continuity package and CI validator
- Django/DRF/PostgreSQL foundation
- Celery/managed KVS
- local/review/staging Heroku pipeline
- React web shell
- React Native/Expo iOS and Android shells
- shared TypeScript API/domain/schema/design-token packages
- email + username + password auth; verification/reset
- secure web session/CSRF and native credential storage
- theme/design-system primitives
- S3 abstraction, Sentry, privacy/consent skeleton
- deep-link skeleton
- Apple/Google developer-project setup
- native technical-risk spikes: MCQ renderer, IQS resources, PT editor, offline/recovery, StoreKit/Play product query

Gate: clean checkout/ZIP recovery succeeds; staging web and internal native builds authenticate against the same backend; responsive/native shells and critical spikes pass.

## 102. Milestone 2 — Curriculum core + automated coverage assurance

Deliver:

- ExamProgram/ExamComponent/Blueprint versions for NextGen Core
- immutable official source artifacts and scope manifest
- ExamLawProfile and source-discovery policy
- doctrine/skill/ethics graph
- automated Rule Obligation Compiler
- authority resolution and lawful multi-source reconciliation
- private outline import/reconciliation pipeline
- omission/excess/conflict detection
- subject-level certification and coverage dashboards
- strict source/scope/rule validators

Gate: current official scope is 100% structurally imported/mapped with required metadata; rule-catalog compilation is reproducible; mandatory coverage validators pass on golden fixtures. Sourcebook reconciliation is optional enhanced validation, never a launch prerequisite.

## 103. Milestone 3 — Assessment + OpenAI + presentation contracts

Deliver:

- GenerationSpecification and immutable assessment domain
- inventory search/selector
- OpenAI service and prompt registry
- generation, independent solver, adversarial reviewer, repair, rubric finalizer
- Assessment Presentation Schema and UI Capability Manifest
- web/native renderer proofs
- AssessmentScopeTarget verification
- golden MCQ/IQS/PT/LRPT corpus
- real staging OpenAI
- continuous validated inventory seeding begins here

Gate: no raw/unvalidated content can become AVAILABLE; all launch clients render the golden fixture matrix; independently confirmed scope targets are required before inventory credit.

## 104. Milestone 4 — Cross-platform Practice + discovery loop

Deliver:

- MCQ/IQS/PT/LRPT Practice on web/iOS/Android
- attempt/workspace/annotation persistence and autosave
- anonymous Instant Practice using canonical AssessmentVersions
- anonymous discovery claim after signup
- grading/results and contextual Ask BarClimb
- History baseline
- public learning-page interactive islands
- cross-device resume and offline-safe ordinary practice

Gate: anonymous SEO → Instant Practice → signup claim and authenticated Practice flows pass on staging; long-form recovery and ownership/concurrency tests pass.

## 105. Milestone 5 — Learner intelligence + My BarClimb orchestration

Deliver:

- evidence/exposure ledger
- Performance/Coverage/Confidence/Retention/Readiness + Evidence Completeness
- Recommendation engine
- server-authoritative HomeProjection / My BarClimb state
- Quick/Standard/Deep Study Sessions
- Review Queue + Suggested Review
- Weakness Repair / Repair Plans
- Session Impact / What Changed
- adaptive Path to Exam / This Week planning
- Progress and authenticated universal Search/private overlays
- longitudinal and writing-trajectory analytics where evidence permits

Gate: deterministic learner test vectors pass; all orchestration decisions are inspectable, advisory, entitlement-aware, and consistent across web/iOS/Android.

## 106. Milestone 6 — Cross-platform Simulation

Deliver:

- blueprint assembly/preassembly/version pinning
- server-authoritative timers and section transitions
- simulation fidelity UI on all launch clients
- immutable submission/scoring/results
- Simulation → Repair Plan workflow
- no-live-AI-after-Begin invariant

Gate: full staging simulation completes with OpenAI disabled after Begin on supported clients; restart/reconnect timing and submission recovery pass.

## 107. Milestone 7 — Quality + publication foundation

Deliver:

- challenge/regrade/reliability/legal-freshness systems
- inventory planner and source-impact revalidation
- publication lifecycle, consent/withdrawal, privacy scrub
- aggregate insight generation
- canonical SEO publishing primitives and trust signals
- search index foundation

Gate: intentionally flawed/stale items are detected and removed from scored eligibility/public trust surfaces; publication withdrawal and legal-freshness propagation pass.

## 108. Milestone 8 — Learning network + growth loops

Deliver:

- username-first public profiles
- published responses/contributions
- qualified views
- educational reactions
- threaded discussion/replies
- follows/bookmarks
- contribution reputation/achievements/Momentum
- Community Pulse
- invite-only Study Circles
- creator analytics
- sharing/deep links/push loops
- report/block/mute/moderation/appeals

Gate: UGC safety and anti-gaming tests pass; subscription status cannot affect public rank/reaction weight/reputation; community activity cannot alter mastery.

## 109. Milestone 9 — Public platform + cross-platform commerce

Deliver:

- full Django SSR SEO hierarchy
- search-intent-aware public pages
- authenticated private overlays on canonical pages
- sitemap/canonicals/Search Console readiness
- Stripe web subscriptions
- StoreKit/App Store server lifecycle
- Google Play Billing/server lifecycle
- unified Django entitlement
- SendGrid
- direct sponsor marketplace
- AdSense web / AdMob native external fill where approved
- house/no-ad fallbacks

Gate: web/iOS/Android purchase/restore/cancel/grace/refund tests converge on the same entitlement; Plus is ad/upsell-free globally; public pages remain useful with ads disabled.

## 110. Milestone 10 — Coverage completion + stores + hardening + coordinated launch

Deliver:

- 100% required official scope + CORE Rule Obligations at launch coverage threshold
- final coverage release snapshot
- launch inventory completion
- security/abuse/load/accessibility/browser/device audits
- production providers and budget alarms
- App Store and Play production candidates/listings
- privacy/account deletion/moderation support
- release/rollback/data-recovery drills
- final golden user journeys for Visitor, Free, and Plus

Gate: Production Launch Checklist passes; iOS and Android satisfy the documented coordinated launch window; cold-recovery drill succeeds from latest repository ZIP.

# PART XXX — DEFINITION OF DONE

## 111. Feature definition of done

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

No “backend complete, UI later” or “desktop done, mobile later” may be called feature-complete.

---

# PART XXXI — LAUNCH AND CASH-GENERATION GATES

## 112. Revenue readiness

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

## 113. Production Launch Checklist

All must pass:

1. all ten milestone gates
2. production Heroku pipeline configured
3. database backup/recovery procedure tested
4. production S3 permissions verified
5. OpenAI production limits/budget alarms configured
6. Stripe live webhook test completed
7. SendGrid domain authentication and live delivery test completed
8. Sentry production environment configured with privacy scrubbing
9. privacy/cookie settings verified
10. Terms, Privacy Policy, Cookie Policy, advertising/sponsor terms available
11. minimum launch inventory achieved
12. no subject materially empty
13. public SEO hubs substantive and internally linked
14. direct sponsor house campaign works even if AdSense is off
15. paid upgrade and restoration tested
16. support contact tested
17. accessibility manual spot audit complete
18. mobile Safari critical flows complete
19. simulation complete with OpenAI disabled after start
20. rollback drill documented

---

# PART XXXII — ADVERSARIAL BUILD REVIEW AND FINAL SPEC UPDATES

## 114. Issues discovered in final review

A final adversarial review identified five risks that would have produced a “working” but commercially weak application if left implicit. They are now incorporated as requirements:

### 113.1 External ad approval risk

**Risk:** assuming AdSense revenue exists on launch day.  
**Resolution:** AdSense is default external fill when approved, but house ads and BarClimb Direct are fully operational independently. Launch does not depend on Google approval.

### 113.2 Conversion not engineered

**Risk:** excellent study engine with no defined free→paid funnel.  
**Resolution:** upgrade moments, quota behavior, conversion events, and checkout handoff are now explicit (§85–86).

### 113.3 Direct sponsor marketplace dependent on organic discovery

**Risk:** sponsor self-service exists but generates no sponsor revenue.  
**Resolution:** admin-assisted campaign creation and outbound-sales support are mandatory (§87). The product can sell sponsorship directly from launch.

### 113.4 Launch content too thin

**Risk:** AI engine works, but public site lacks enough trusted content for users, SEO, and AdSense review.  
**Resolution:** launch inventory minimums and curriculum breadth gates are mandatory (§10, §112).

### 113.5 Release process creates fragile production

**Risk:** Codex produces features but no safe release/rollback discipline.  
**Resolution:** staging, feature flags, release checks, migration discipline, and rollback contracts are mandatory (§95–97).

## 115. Remaining non-engineering uncertainties

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

## 116. Required first 90-day metrics

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

**READY TO BUILD: YES — subject to creating the repository copies of the contracts and beginning Milestone 1 only after this Constitution is committed as the authoritative source of truth.**

The specification is sufficiently complete that Codex should not need to invent a major product decision, data lifecycle, learner algorithm, monetization mechanism, provider integration strategy, responsive behavior, or definition of completion.

The remaining decisions during implementation should be ordinary engineering choices—library-level details, query optimization, component internals, and low-level code organization—provided they conform to this Constitution.

**Commercial verdict:** The application is architected to be cash-generating from launch through subscription, AdSense when approved, and direct sponsorship. No responsible specification can guarantee revenue before traffic, conversion, sponsor demand, and assessment trust are observed. The app is now designed to measure and optimize those variables instead of merely hoping for them.


# PART XXXV — FINAL CROSS-SCENARIO APPLICATION ARCHITECTURE

This amendment is authoritative over older duplicated model/API/UI language. It exists to guarantee that the three primary journeys—anonymous SEO discovery, authenticated Free study, and authenticated Plus study—are supported by one coherent application rather than parallel ad-hoc implementations.

## 117. Projection architecture: server owns page meaning

Complex learner-facing surfaces use server-composed, versioned **projections**. A projection is not a second source of truth; it composes canonical domain state into one response appropriate for a surface. React/React Native may render projections but may not independently reimplement learner planning, entitlement, coverage, publication eligibility, ad eligibility, or private/public visibility rules.

Required projections:

### `HomeProjectionV1`
Contains:
- authoritative Recommended Next and rationale token/summary;
- deterministic Resume candidate and precedence reason;
- readiness/evidence-completeness snapshot;
- active StudySession/RepairPlan state;
- Review Queue/Suggested Review summary;
- Path-to-Exam/This-Week summary where available;
- restrained Community Pulse references;
- effective capabilities/entitlement;
- notification summary;
- no private data belonging to another learner.

### `PublicLearningPageProjectionV1`
Canonical public SSR content remains cacheable and identity-independent. Authenticated/private additions are fetched separately from a **private no-store overlay** and may include:
- learner status for the mapped nodes;
- prior attempts/history references;
- retention/review state;
- Recommended Practice action;
- Plus-only deeper insight where entitled.

Private overlays must never be embedded into shared CDN/page caches, sitemap HTML, OpenGraph metadata, structured data, or anonymous SSR fragments.

### `SearchProjectionV1`
Supports public and authenticated result groups:
- Learn
- Practice
- official scope/doctrine
- skills/ethics
- community/public responses
- authenticated History
- authenticated learner status
- authenticated Review/Suggested Review
- contextually eligible Ask BarClimb action.

Search ranking may use public relevance and private learner utility in separate stages; private learner weakness may never alter public SEO ranking or leak into another user's results.

### `ProgressProjectionV1`
Server-calculated subject/doctrine/rule/skill state with Performance/Coverage/Confidence/Retention, Evidence Completeness, mastery state, testing expectation, and recommended action. Clients may simplify presentation but not recalculate labels.

### `AttemptWorkspaceProjectionV1` / `GradeProjectionV1`
Version-pinned assessment presentation + authoritative workspace/grade state. Answer keys/rubric internals are withheld according to lifecycle/mode permissions.

### `EntitlementCapabilityProjectionV1`
Maps plan/purchase/grace state into effective capabilities. UI checks capabilities such as `can_start_full_simulation`, `can_start_pt`, `can_use_advanced_ask`, `ads_suppressed`, rather than scattering plan-name conditionals across clients.

## 118. Canonical domain additions required by the journeys

The following models are required in addition to earlier canonical models. Equivalent normalized implementations require a documented contract update.

### `learning.StudyPreference`
- user OneToOne
- exam_target/window reference
- typical_session_minutes nullable
- study_days_per_week nullable
- reminder preferences reference
- updated_at

Preferences guide but never override learner evidence or explicit user choice.

### `learning.StudySession`
- user
- kind QUICK/STANDARD/DEEP/CUSTOM/REPAIR/SIMULATION_REPAIR
- target_minutes nullable
- source RECOMMENDED/USER_SELECTED/REPAIR/REVIEW
- state PLANNED/ACTIVE/PAUSED/COMPLETED/ABANDONED/DISMISSED
- planner_version
- started_at/completed_at
- impact_snapshot nullable after completion

### `learning.StudySessionItem`
Ordered link to assessment, review action, rule recall, or other registered learning action; includes status and rationale. Items may be replanned only under documented state rules; completed evidence is immutable.

### `learning.ReviewQueueItem`
- user
- typed target (rule/assessment/public explanation/model response as allowed)
- source MANUAL/SUGGESTED_ACCEPTED/AUTO_OPT_IN
- state ACTIVE/COMPLETED/DISMISSED/ARCHIVED
- due_at nullable
- reason code
- created_at/completed_at

`Suggested Review` is computed separately and does not populate the durable queue without acceptance or explicit opt-in.

### `learning.RepairPlan` and `learning.RepairPlanStep`
Bounded adaptive sequence tied to one or more diagnosed learner deficits. Store diagnosis basis, planner/model version, targeted nodes/skills, state, ordered steps, adaptation events, and completion outcome. Repair plans may update recommendations but never rewrite historical grades/evidence.

### `learning.LearnerPlanSnapshot`
Versioned Path-to-Exam / This-Week projection inputs and generated plan summary. It is advisory, re-plannable, and never a rigid obligation calendar.

### `learning.SessionImpact`
Immutable/computable post-session summary referencing evidence/state deltas actually caused by completed eligible learning evidence. Product engagement events alone cannot create impact.

### `learning.AnonymousDiscoverySession`
Privacy-minimized, short-lived discovery identity supporting Instant Practice continuity before signup. Contains opaque token/hash, timestamps, consent/region state as needed, and claim/expiry state. It must not become a hidden durable learner profile.

### `learning.AnonymousAttemptClaim`
Auditable, idempotent claim/merge record binding eligible anonymous attempts to a newly authenticated account after proof of possession/session continuity. Prevent double claim and cross-user claim.

### `communications.Notification` / `communications.DeviceRegistration`
Canonical notification inbox/delivery state and platform device registrations. Notification preferences are server-authoritative and segmented by learning/results/community/product/marketing categories.

### `search.SearchDocument` or equivalent indexed representation
Search uses PostgreSQL full-text/trigram infrastructure at launch with an explicit indexed representation linking back to canonical subjects/doctrines/rules/skills/ethics/publications/assessments/community objects. The index stores searchable/public fields and canonical IDs; it does not become a second curriculum or publication source of truth. Private History/learner-status groups are joined after authorization and are never copied into the public search index.

### `common.ClientSurfaceCapabilityManifest`
Versioned server-readable manifest recording which launch clients support which registered product surfaces/projection versions/capabilities. Minimum registered surfaces include HOME, PRACTICE, SIMULATION, PROGRESS, SEARCH, HISTORY, REVIEW, REPAIR, NOTIFICATIONS, PUBLIC_OVERLAY, COMMUNITY, CIRCLES, CREATOR_ANALYTICS, ACCOUNT_PRIVACY_BILLING. A feature may not be globally activated when a launch-required client lacks the necessary surface/projection support unless the flag explicitly defines a safe documented phased rollout.

### Community/publication additions
The canonical data model must include the `community/` models defined by the Product Experience & Learning Network Specification: PublicProfile, PublishedContribution, DiscussionThread, Comment, Reaction, ContentView, Follow, Bookmark, UserBlock, ContentReport, ModerationCase/Action, ReputationSnapshot, AchievementDefinition/UserAchievement, StudyCircle/Membership/Share. These are launch domain models, not optional frontend-only records.

## 119. Required API/view surface

All endpoints are under `/api/v1/` unless explicitly public HTML routes. Schemas are versioned and OpenAPI-covered.

### Surface projections
- `GET /home/` → `HomeProjectionV1`
- `GET /me/capabilities/` → effective entitlement/capabilities
- `GET /search/` → `SearchProjectionV1`
- `GET /progress/` and node drilldowns → `ProgressProjectionV1`
- `GET /public/overlay/{target_type}/{target_id}/` → authenticated no-store private overlay

### Anonymous discovery / Instant Practice
- create/recover anonymous discovery session through privacy-safe session mechanism
- `POST /practice/instant/start/`
- canonical attempt response/save/submit endpoints with anonymous ownership token where eligible
- `POST /attempts/claim/` authenticated, idempotent, ownership-safe

Anonymous attempts use the same validated AssessmentVersion and grading contracts but do not enter persistent learner analytics until successfully claimed.

### My BarClimb orchestration
- `POST /study-sessions/plan/`
- `GET /study-sessions/{id}/`
- `POST /study-sessions/{id}/start|pause|complete|dismiss/` or REST-equivalent actions
- `GET /review/`
- `POST /review/items/`
- `DELETE/PATCH /review/items/{id}/`
- `GET /review/suggestions/`
- `POST /review/suggestions/{id}/accept|dismiss/`
- `POST /repair-plans/`
- `GET /repair-plans/{id}/`
- `POST /repair-plans/{id}/next/` as needed by server planner
- `GET/PATCH /study-preferences/`
- `GET /plan/` for Path-to-Exam/This-Week projection
- `GET /history/patterns/` Plus-capability protected and evidence-thresholded
- `GET /progress/writing-trajectory/` Plus-capability protected and rubric-compatible

### Contextual Ask
One central Ask service receives a registered context type + context identifier. Supported contexts include assessment-after-submit, grade, doctrine/public page, Search result, History slice, Progress node, simulation result, and RepairPlan. The server resolves allowable context; clients may not send hidden answer keys or arbitrary private learner data as prompt truth.

### Community and notifications
Community endpoints from the Product Experience spec are required. Add canonical notification read/preferences/device registration APIs shared by web/native.

## 120. Web route/view contract

### Public SSR routes
Django owns canonical indexable HTML for:
- NextGen hub/family/subject/doctrine/rule/skill/ethics pages
- public assessments
- eligible published responses
- aggregate insights
- public profiles/contribution pages where indexable gates pass
- pricing/advertise/legal/help pages.

The first viewport is selected from the page's declared search-intent presentation, not dynamically changed by private learner weakness. Authenticated personalization hydrates only through the private overlay.

### Authenticated app routes
React owns Home, Practice setup/session, Simulation, Progress, History, Search, Review, RepairPlan, notifications, Account/Privacy/Billing, creator analytics, and Circles. Public pages may mount React islands for Instant Practice/community interactions without surrendering canonical SSR content.

## 121. UI composition/capability matrix

Every significant surface must define states for Anonymous, Free, Plus, loading, empty, offline where applicable, error, and restricted capability. The same component should prefer capability-driven rendering over plan-name forks.

### Public learning page
Anonymous: answer search intent immediately → trust signals → Instant Practice → explanation/community → Continue Learning → earned signup.
Free signed-in: all public content + private status/history/review overlay + account-only community writes.
Plus: same public/community rank + deeper private learner overlay/Ask + globally suppressed ads/upsells.

### Home
Anonymous has no app Home. Free and Plus use the same Home composition. Plus has deeper eligible actions and no monetization friction; it does not get a separate dashboard.

### Practice
Same AssessmentRenderer and attempt domain for all eligible users. Free limits are checked before starting expensive/restricted work. Plus exposes advanced goals progressively, not by replacing the simple Recommended flow.

### Progress/Search/History
Free receives useful baseline insight. Plus capabilities may unlock deeper longitudinal/pattern/trajectory analysis, but underlying grades/evidence and public ranking are identical.

### Simulation
Fidelity mode suppresses community, Ask, explanations, recommendations, and ads during active exam sections for every plan. Entitlement controls eligibility to start—not the integrity of an already-started attempt.

## 122. State ownership, caching, sync, and concurrency

- Django/PostgreSQL is authoritative for learner state, entitlement, curriculum, publication/moderation, recommendations, billing lifecycle, and final attempt state.
- Redis/KVS may cache projections/jobs but not become durable truth.
- Public SSR caches are identity-independent. Private overlays are `Cache-Control: private, no-store` or equivalently protected.
- Web service-worker/native offline caches must never expose answer keys early or another learner's private data.
- Cross-device writes use optimistic concurrency/version tokens; explicit conflict resolution protects constructed responses, annotations, StudySession state, Review Queue, and repair progress.
- Portable annotation anchors use versioned resource identity + text/range anchors, never screen coordinates.
- Entitlement downgrade/revocation affects future privileged starts at safe boundaries. It never deletes work, rewrites evidence, or makes an in-progress accepted attempt unrecoverable.

## 123. Privacy and identity boundaries across the three scenarios

- Anonymous discovery is short-lived and not persistent learner analytics.
- Signup claim is explicit and auditable.
- Public canonical content never includes private learner overlays.
- Public identity is username-first; real name is not required for community participation.
- Community writes require authenticated identity; anonymous may read/share and use bounded public Ask/Instant Practice.
- Plus status is private unless the user independently chooses to disclose it; subscription tier cannot influence community rank/reputation.
- Creator analytics expose only the creator's authorized aggregate metrics and never viewer identities or private learner states.

## 124. Product analytics vs learner evidence firewall

Events such as page view, Search, reaction, comment, follow, bookmark, notification open, study-session wrapper completion, upgrade, and share are **product/network analytics**. They cannot directly improve Performance, Coverage, Confidence, Retention, Readiness, or mastery.

Learner state changes only from validated eligible learner evidence under the Learning & Assessment Specification. Community/product activity may create a recommendation opportunity (for example, “test yourself on this concept”) but never mastery credit.

## 125. Admin/operations required for orchestration

Django Admin/staff tooling must additionally expose:
- Home/recommendation rationale inspection
- StudySession/RepairPlan anomaly inspection
- Suggested Review policy parameters
- learner planner/model version and active thresholds
- Search indexing status
- anonymous claim anomaly/audit records
- effective entitlement/capability inspection by account
- notification delivery/preferences troubleshooting
- private-overlay/cache diagnostics
- community moderation/reputation versions
- per-client feature/parity flags.

No staff control may directly falsify a learner score/readiness without an auditable evidence/recalculation path.

## 126. Cross-scenario golden journeys required for GA

### Scenario A — SEO visitor
Search landing → immediate answer → Instant Practice → explanation → community/aggregate insight → second meaningful action (Discovery Activation) → signup → idempotent claim → Home/Progress reflects only claimed eligible evidence.

### Scenario B — signed-in Free learner
Home Recommended Next → StudySession → MCQ/IQS → grading → Session Impact → Progress → Search → canonical public page private overlay → community read/write → Review/Repair choice → cross-device resume.

### Scenario C — Plus learner
Home with no ads/upsells → advanced Practice/Weakness Repair → contextual Ask → deep Progress/History pattern analysis → Full Simulation → Repair Plan → personalized public-page overlay → creator/community participation with neutral ranking → cross-device continuation → billing grace/cancel/downgrade without lost work.

Each journey must run on required web/browser and native matrices with entitlement, privacy, offline/reconnect, error, and authorization variants.

## 127. Final architectural prohibition list

The following are launch-blocking design errors:

- client-side calculation of readiness or entitlement truth;
- separate anonymous/free/Plus assessment implementations;
- separate web/native curriculum or scoring semantics;
- personalized data rendered into public cacheable HTML;
- community popularity affecting mastery;
- Plus status affecting public rank/reputation;
- automatic durable Review Queue pollution from every error;
- Resume permanently outranking a better learner recommendation without documented precedence;
- billing state destroying in-progress learner work;
- Search maintaining a competing doctrine taxonomy;
- public Ask creating canonical law/content without the normal validation/publication pipeline;
- endpoints returning future resource content, answer keys, or private rubric internals before authorized lifecycle state;
- missing recovery/handoff updates after material architecture changes.


## 128. Mandatory integration/security tests for cross-scenario surfaces

Release-blocking tests include:
- shared-cache test proving authenticated private overlay never appears in anonymous/public HTML;
- anonymous attempt claim replay/cross-user theft tests;
- entitlement capability tests across ACTIVE/GRACE/EXPIRED/REVOKED and Stripe/Apple/Google sources;
- Plus ad suppression on authenticated public SSR + React hydration + native cold start;
- search authorization tests proving private history/status never leaks to other users or public results;
- answer-key/resource-release serializer tests for anonymous, Free, Plus, Simulation lifecycle states;
- community rank test proving plan tier has zero ranking/reputation effect;
- StudySession/RepairPlan idempotency and duplicate-evidence tests;
- offline stale-projection tests proving clients do not recalculate readiness/recommendations;
- notification deep-link authorization tests;
- deleted/withdrawn public response cache/index invalidation tests.

## 129. View-model performance budgets

Projection aggregation must not turn Home/Search/Progress into N+1 query farms. Implementation must:
- instrument projection latency and query counts;
- prefetch/cache identity-independent data safely;
- keep private caches user-scoped and short-lived where used;
- allow partial noncritical modules (e.g. Community Pulse) to fail without blocking Recommended Next or assessment work;
- define stale-while-revalidate behavior only for data where staleness is safe and visible.

Home's critical learner action must not wait on ads, community, creator analytics, or nonessential notifications.
Progress drilldowns should be lazy/paginated by hierarchy where needed; Home must not hydrate the entire curriculum graph or full History merely to render a readiness summary. Search result groups must be bounded/paginated.
