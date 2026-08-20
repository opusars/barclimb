# BarClimb Learning & Assessment Specification

**Status:** Authoritative v1 companion specification.

This document consolidates and supersedes the former Assessment Interaction Contract, Curriculum Coverage & Completeness Contract, and Ethics & Focused Practice Contract. It governs curriculum completeness, assessment presentation and interaction, NextGen fidelity, focused ethics practice, learner workspace behavior, grading presentation, and related validation.

If a requirement here conflicts with a higher-level invariant in `BARCLIMB_BUILD_CONSTITUTION.md`, the Build Constitution controls. Otherwise this document is authoritative for learning/assessment behavior.

---

# PART I - ASSESSMENT INTERACTION AND PRESENTATION

**Status:** Authoritative companion to `BARCLIMB_BUILD_CONSTITUTION.md`  
**Version:** 1.0  
**Purpose:** Define exactly how MCQ, Integrated Question Set (IQS), Standard Performance Task (PT), and Legal Research Performance Task (LRPT) content is presented, manipulated, answered, saved, reviewed, graded, and rendered across Practice and Simulation.

## 1. Constitutional invariant

BarClimb uses a **schema-driven assessment renderer**. The backend provides a versioned Assessment Presentation Schema. React renders only registered component types contained in the active UI Capability Manifest.

**AI may compose supported assessment components; AI may never invent UI.**

An `AssessmentVersion` may not become `AVAILABLE` unless all required resource types, response types, layouts, navigation behaviors, and tools are supported by the active capability manifest and pass structural validation.

Practice and Simulation use the **same assessment renderer**. Mode policy changes available tools and feedback; it does not fork the renderer.

## 2. Official-fidelity baseline

The first NextGen capability profile is based on the Official Examinees' Guide to the NextGen UBE, July 2026-February 2027. The official software states that examinees have access to a section countdown timer, navigation status, four-color highlighting, light/dark/high-contrast display adjustment, zoom, marking for review, and answer-choice strike-through for multiple-choice questions. For written IQS/PT work it also provides adjustable split screen, notepad, spell check, copy/paste and cut/paste within the provided environment, undo/redo, basic formatting, and tabbed legal resources.

Source of truth at build time: NCBE official materials. The capability profile is versioned so future exam-software changes do not require ad hoc UI changes.

## 3. Mode policies

### 3.1 `PRACTICE_ENHANCED`

Practice contains all supported exam-fidelity tools plus selected learning conveniences that do not reveal answers before submission.

Allowed practice-only conveniences:

- optional word count for constructed responses;
- optional resource text search;
- optional persistent Practice Notes even for standalone MCQ practice;
- immediate grading/explanation only after the applicable unit/set is submitted;
- Ask BarClimb after submission;
- challenge/regrade controls after grading;
- next-practice recommendation after completion.

Practice-only tools must be visually distinguishable from exam-fidelity tools where confusion is possible.

### 3.2 `SIMULATION_FIDELITY`

Simulation follows the active `ExamSoftwareCapabilityProfile` and applicable blueprint.

- no answer explanations before the section/session ends;
- no Ask BarClimb;
- no learner recommendations;
- no grading during the timed section;
- no ads during a running timed section;
- no practice-only search/word-count/note tools unless the active official capability profile permits them;
- all exam tools remain available according to the capability profile;
- timer, navigation, response state, and submission remain server authoritative.

BarClimb does not claim to reproduce NCBE's secure browser security controls; it reproduces the examination workflow and supported study-relevant interaction patterns as closely as practical.

## 4. UI Capability Manifest

The frontend and backend share a versioned manifest. Initial manifest: `assessment_ui.v1`.

### 4.1 Response types

- `MCQ_SINGLE`
- `MCQ_MULTI`
- `SHORT_CONSTRUCTED`
- `MEDIUM_CONSTRUCTED`
- `LONG_CONSTRUCTED`
- `DRAFT`
- `EDIT`
- `COUNSEL`

### 4.2 Resource types

- `TEXT`
- `EMAIL`
- `CASE`
- `STATUTE`
- `CONTRACT`
- `PLEADING`
- `POLICE_REPORT`
- `TRANSCRIPT`
- `MEMO`
- `TABLE`
- `IMAGE`
- `ATTACHMENT`

Resource types may share underlying renderer primitives but retain semantic type metadata for accessibility, presentation, generation, analytics, and future format-specific behavior.

### 4.3 Layouts

- `FOCUSED` - standalone MCQ and simple single-unit work.
- `INTEGRATED` - IQS resource/question workspace.
- `WORKSPACE` - Standard PT file/library plus long response.
- `RESEARCH_WORKSPACE` - LRPT resources plus mixed units and final writing task.

### 4.4 Navigation policies

- `FREE` - permitted movement among available units.
- `LINEAR` - ordered movement but prior available units remain revisitable unless exam rules prohibit it.
- `PROGRESSIVE` - later units/resources remain unavailable until defined release conditions occur.

### 4.5 Tool capabilities

- `TIMER_TOGGLE`
- `FIVE_MINUTE_TIMER_WARNING`
- `QUESTION_NAVIGATOR`
- `MARK_FOR_REVIEW`
- `HIGHLIGHT_4_COLOR`
- `ANSWER_STRIKETHROUGH`
- `LIGHT_DARK_HIGH_CONTRAST`
- `TEXT_ZOOM`
- `SPLIT_SCREEN`
- `ADJUSTABLE_SPLIT`
- `NOTEPAD`
- `SPELLCHECK`
- `COPY_PASTE`
- `CUT_PASTE`
- `UNDO_REDO`
- `BASIC_FORMATTING`
- `RESOURCE_TABS`
- `RESOURCE_SEARCH_PRACTICE_ONLY`
- `WORD_COUNT_PRACTICE_ONLY`

Unsupported capability references are a hard structural-validation failure.

## 5. Assessment Presentation Schema

Each interactive `AssessmentVersion` exposes:

```json
{
  "presentation_schema_version": "assessment_ui.v1",
  "family": "IQS",
  "layout": "INTEGRATED",
  "navigation_policy": "FREE",
  "capability_profile": "nextgen_j26_f27.v1",
  "matter": {},
  "resources": [],
  "units": [],
  "release_rules": [],
  "display_constraints": {}
}
```

The API returns structured content, never AI-authored HTML for the authenticated assessment renderer. Public SEO pages are server-rendered from the same canonical `AssessmentVersion`.

## 6. Universal examinee tools

### 6.1 Four-color highlighting

Users may highlight selectable text in question prompts and provided resources using exactly four semantic-neutral highlight colors in the fidelity profile.

Requirements:

- select text -> compact highlight toolbar;
- four colors plus Clear;
- highlight persists for the attempt;
- highlight survives navigation, refresh, reconnect, and theme change;
- highlight is accessible in light, dark, and high-contrast modes;
- highlighting never changes grading;
- selection and annotation must not shift canonical text layout materially.

Annotation anchors store canonical text offsets plus exact-quote verification and the source `AssessmentVersion`. Annotations never migrate silently to a changed assessment version.

### 6.2 Zoom / text resizing

Provide accessible text-size adjustment using controlled steps. Initial values:

- 90%
- 100%
- 110%
- 125%
- 150%

The setting affects legal/question text without making controls unusable or producing horizontal page overflow.

### 6.3 Display schemes

Global BarClimb theme preference remains `SYSTEM`, `LIGHT`, or `DARK`.

Assessment presentation additionally supports `HIGH_CONTRAST`. High contrast is an accessibility/exam presentation override and does not replace the persistent global theme preference.

### 6.4 Question navigator

Navigator shows each applicable unit as:

- `UNANSWERED`
- `PARTIALLY_ANSWERED`
- `ANSWERED`
- `MARKED_FOR_REVIEW`

`PARTIALLY_ANSWERED` includes, for example, a select-two question with only one choice selected or a multi-field response with required portions incomplete.

Navigator supports direct movement only when the active navigation policy allows it.

### 6.5 Mark for review

Every eligible question/unit exposes a clearly labeled review flag. It persists server-side and is reflected in the navigator. Marking for review has no scoring effect.

### 6.6 Timer behavior

Practice timer behavior is configurable by the learner when timing is optional.

Simulation follows the capability profile. For the July 2026-February 2027 profile, the countdown may be hidden by the examinee until the five-minute warning, at which point the warning/timer state becomes visible as required by the profile.

Server time is authoritative. Client timer is presentation only.

## 7. Standalone MCQ interaction contract

### 7.1 Choice selection

`MCQ_SINGLE` uses four options unless a future validated specification permits another official form.

`MCQ_MULTI` initial NextGen profile uses six options with exactly two expected selections.

Requirements:

- entire answer row is touch/click target;
- native semantic radio/checkbox behavior or equally accessible implementation;
- selected state is visually distinct in every theme;
- multi-select visibly states required selection count;
- selecting the allowed maximum prevents accidental excess selection or requires replacing a choice through an obvious action;
- no submission until selection rules are satisfied unless user explicitly submits an incomplete section under applicable simulation rules.

### 7.2 Answer-choice strike-through

Each choice has a dedicated **Eliminate** control.

Interaction rules:

- striking a choice does not select or deselect it;
- a struck choice remains selectable if the user changes their mind;
- clear visual strike-through plus secondary eliminated styling;
- screen reader announces eliminated/not eliminated state;
- elimination survives navigation, refresh, reconnect, and theme changes;
- one action restores an eliminated choice;
- eliminated state is not grading evidence and does not affect learner mastery at launch.

On narrow screens the eliminate control remains separate from the answer-selection hit target to prevent accidental selection.

### 7.3 MCQ prompt annotation

Question-stem text supports four-color highlighting. Answer-choice text is not highlightable at launch; choice elimination is the deliberate answer-analysis tool.

### 7.4 Practice result state

After submission in Practice:

- correct/incorrect/partial result;
- earned/available points where appropriate;
- correct answer(s);
- explanation;
- distractor analysis when available;
- rule/issue tested;
- learner impact summary;
- Ask BarClimb;
- Helpful / Problem controls;
- next recommendation.

The user's pre-submit strike-through/highlight state remains visible during review.

## 8. IQS interaction contract

IQS is not a fixed page. It is an ordered set of supported response units sharing a Matter and optional resources.

### 8.1 Desktop

Default `INTEGRATED` layout:

- left/context region: Matter and resource navigator;
- right/work region: active unit and response;
- adjustable split when written-response capability is active;
- active resource switch without page reload;
- independent resource scroll positions preserved locally;
- response never disappears when user changes resources.

### 8.2 Tablet

Use two-pane layout when usable width remains sufficient. Otherwise collapse resource navigation into a drawer/tabbed workspace without shrinking text below accessibility targets.

### 8.3 Mobile

One major workspace at a time:

- `QUESTION`
- `MATTER`
- `RESOURCES`
- `RESPONSE` where response deserves a dedicated view

Switching views must be near-instant and preserve cursor, selection, response text, annotations, and active resource.

### 8.4 Resource release

Resources may define `available_from_unit_id` or explicit release rules. Progressive release updates the resource navigator without reload.

A not-yet-released resource must not be leaked through API payloads if its existence/content could alter the task.

## 9. PT and LRPT interaction contract

### 9.1 Standard PT desktop

Default `WORKSPACE`:

- File/Library navigation;
- active resource viewer;
- long-response editor;
- draggable/resizable divider;
- task instructions persistently recoverable;
- no ad within the workspace.

### 9.2 LRPT

`RESEARCH_WORKSPACE` supports mixed MCQ/short-answer units followed by medium writing while preserving the same resource universe and navigator.

### 9.3 Resource grouping

PT resources support semantic top-level groups such as:

- `CASE_FILE`
- `LIBRARY`

Each group contains tabbed documents. Active group/document state persists locally for the attempt.

### 9.4 Practice-only resource search

Practice may offer `Find in resources`. It searches only material supplied inside the assessment. It is hidden in Simulation unless the active exam capability profile explicitly permits it.

## 10. Constructed-response editor

The editor must feel like a serious legal-writing workspace, not a generic textarea.

Launch capabilities:

- autosave;
- local recovery;
- undo/redo;
- browser spell check;
- cut/copy/paste;
- copy from supplied resources;
- bold;
- italic;
- underline;
- bulleted lists;
- numbered lists;
- indent/outdent;
- tab behavior appropriate to the editor;
- plain, stable pasted-text normalization;
- optional practice-only word count;
- no decorative rich-text features unrelated to exam work.

Paste must not import unsafe HTML, remote images, scripts, hidden tracking, or foreign styles. Normalize to BarClimb's safe supported formatting model.

Editor state must survive resource switching, question switching, refresh, temporary network loss, and recoverable application errors.

## 11. Notepad / scratchpad

### 11.1 Simulation

Written IQS/PT environments expose an ungraded Notepad where the active capability profile permits it.

Notepad:

- autosaves;
- survives resource/unit changes;
- clearly states `Not graded`;
- is excluded from grading payloads and learner evidence;
- is deleted/retained according to attempt retention policy but never treated as submitted answer content.

### 11.2 Practice

Practice may expose `Practice Notes` more broadly, including MCQ practice. It must be visually labeled as a practice convenience when not part of the official fidelity profile.

## 12. Copy/paste boundaries

Practice allows ordinary safe clipboard operation.

Simulation must reproduce supported in-app workflow as closely as practical, but BarClimb does not represent itself as a secure examination browser. Any stricter external-paste restriction must be capability-profile driven, tested across browsers, and must never risk loss of legitimate response text.

All pasted content is sanitized.

## 13. Annotation and workspace persistence

Add canonical models:

### `learning.AttemptAnnotation`

- `id: UUID`
- `attempt_id`
- `assessment_version_id`
- `unit_id nullable`
- `resource_id nullable`
- `annotation_type: HIGHLIGHT`
- `color: H1 | H2 | H3 | H4`
- `start_offset`
- `end_offset`
- `exact_quote`
- `text_hash`
- `created_at`
- `updated_at`

Constraint: exactly one of `unit_id` or `resource_id` identifies the canonical text surface unless a defined surface identifier is used.

### `learning.AttemptChoiceState`

- `attempt_id`
- `unit_id`
- `answer_option_id`
- `is_eliminated`
- timestamps

Unique: `(attempt_id, unit_id, answer_option_id)`.

### `learning.AttemptUnitState`

- `attempt_id`
- `unit_id`
- `answer_status`
- `marked_for_review`
- `first_seen_at`
- `last_seen_at`

Unique: `(attempt_id, unit_id)`.

### `learning.AttemptNotepad`

- `attempt_id`
- `content`
- `version`
- timestamps

One notepad per attempt or per section according to assessment/session specification.

UI-only transient state such as active tab, local scroll position, and divider percentage may be stored client-side and restored locally; grading-critical and exam-state data must be server persisted.

## 14. Workspace API contract

Add to `/api/v1/`:

- `POST /attempts/{attempt_id}/annotations/`
- `PATCH /attempts/{attempt_id}/annotations/{annotation_id}/`
- `DELETE /attempts/{attempt_id}/annotations/{annotation_id}/`
- `PUT /attempts/{attempt_id}/units/{unit_id}/choice-state/{option_id}/`
- `PUT /attempts/{attempt_id}/units/{unit_id}/state/`
- `PUT /attempts/{attempt_id}/notepad/`
- `GET /attempts/{attempt_id}/workspace/`

All mutating endpoints require attempt ownership, expected version/idempotency protection where applicable, and return authoritative saved state/version.

A consolidated workspace hydration response includes current response values, unit state, annotations, choice eliminations, notepad, available resources, release state, timer state, and current attempt version.

## 15. React renderer contract

Required core components:

- `AssessmentRenderer`
- `AssessmentModeProvider`
- `AssessmentHeader`
- `AssessmentToolbar`
- `CountdownTimer`
- `QuestionNavigator`
- `MarkForReviewControl`
- `TextZoomControl`
- `ExamColorSchemeControl`
- `HighlightToolbar`
- `AnnotationLayer`
- `ResourceNavigator`
- `ResourceViewer`
- `SplitPane`
- `Notepad`
- `SaveStatus`
- `SingleSelectQuestion`
- `MultiSelectQuestion`
- `ChoiceEliminateControl`
- `ShortResponseEditor`
- `MediumResponseEditor`
- `LongResponseEditor`
- `DraftingResponseEditor`
- `EditingResponseEditor`
- `CounselingResponseEditor`
- `ConstructedResponseToolbar`
- `GradeRenderer`
- `MCQResult`
- `RubricScorecard`
- `CriterionFeedback`
- `StudentEvidenceHighlight`
- `MissingIssuePanel`
- `ImprovedResponse`
- `ModelResponse`
- `NextPracticeRecommendation`

Component registry maps canonical schema identifiers to these implementations. Unknown identifiers render no learner-facing fallback; the assessment must have been rejected earlier.

## 16. Grade rendering

Grading presentation is response-type aware.

### MCQ

- points earned;
- canonical answer;
- rationale;
- distractor analysis;
- tested doctrine/issue;
- partial-credit explanation for multi-select.

### Constructed response

- overall result;
- rubric criteria and points;
- strengths;
- omissions;
- legal errors;
- fact-use findings;
- excerpts from the learner answer supporting grader conclusions;
- improved approach;
- optional model response;
- recommendation.

The grader's `student_response_evidence[]` maps to stable text ranges in the learner response. The UI visibly distinguishes learner text from AI commentary.

## 17. Accessibility interaction requirements

In addition to WCAG 2.2 AA:

- strike-through state is conveyed semantically, not by line styling alone;
- highlight colors have non-color accessible metadata and remain distinguishable in high contrast;
- split-pane has keyboard-operable resizing or an accessible equivalent;
- resource tabs use proper tab semantics;
- editor toolbar controls have accessible names and pressed states;
- navigator status is announced textually;
- timer warnings use non-disruptive live-region behavior;
- focus returns predictably after dialog/drawer close;
- mobile workspace switching preserves keyboard/focus appropriately;
- all assessment operations are possible without a mouse.

## 18. Responsive interaction requirements

At 320/375/390/768/1024/1440 px:

- no forced horizontal document scrolling for ordinary question text;
- answer rows and eliminate controls remain independently operable;
- highlight toolbar remains within viewport;
- resource switcher never covers the active editor permanently;
- editor toolbar wraps/collapses into an accessible overflow where necessary;
- split-pane is replaced by single-workspace switching before either pane becomes unusable;
- timer and navigator never obscure content;
- mobile virtual keyboard must not hide the active response area or submit/navigation controls without a recovery path.

## 19. Autosave and recovery requirements

Response editor:

- debounce save at 750ms after typing stops;
- periodic safety save during continuous writing;
- local recovery copy;
- visible `Saving`, `Saved`, `Offline`, `Retrying` state.

Annotations, elimination state, mark-for-review, and notepad save independently and optimistically.

On reconnect, client reconciles by version. No operation may silently overwrite newer server response content.

## 20. Interaction analytics boundaries

At launch, BarClimb may record operational events such as:

- resource opened;
- unit viewed;
- choice eliminated;
- highlight created;
- mark-for-review used;
- notepad used;

These interaction signals **do not affect mastery, grading, readiness, or recommendation algorithms in v1** unless a future validated learner-model version explicitly adopts them. This prevents accidental psychometric claims from interface behavior.

## 21. Ads and assessment interaction

- no ad may appear inside a question stem, answer list, legal resource, constructed-response editor, or notepad;
- no ad may visually resemble an answer or resource tab;
- no ad during a running timed Simulation section;
- Practice ads may appear only at defined transition boundaries and may not move the active question/editor when loaded;
- BarClimb+ removes advertising without changing assessment functionality.

## 22. Combinatorial UI fixture suite

Golden UI fixtures are mandatory and are not satisfied by one example of each assessment family.

Minimum fixtures:

1. `MCQ_SINGLE` with highlighting + elimination.
2. `MCQ_MULTI` six choices/select two + partial state.
3. IQS: MCQ -> short response.
4. IQS: statute + case -> multi-select -> counseling response.
5. IQS: email + contract -> editing -> medium response.
6. IQS with progressive resource release.
7. Standard PT with File + Library + long response.
8. LRPT with MCQs + short answer + final medium response.
9. Long-resource stress fixture.
10. Offline/reconnect fixture with annotations + editor + notepad state.

Every fixture must pass:

- desktop;
- tablet;
- mobile;
- Light;
- Dark;
- High Contrast;
- keyboard-only;
- autosave/reload recovery;
- resource switching;
- annotation persistence;
- question navigation;
- screen-reader smoke test on critical controls.

## 23. Practice usability requirements

A normal learner must be able to begin a recommended MCQ from Home in no more than three intentional actions after login.

For repeated practice:

- `Next` must be obvious after review;
- prior explanation must not accidentally carry into next question;
- keyboard focus must move to the new question heading;
- current subject/type context remains visible but unobtrusive;
- user can exit without losing the completed attempt;
- quota/upgrade messaging appears only at natural boundaries.

## 24. Simulation usability requirements

Before `Begin`, all section assets are preassembled and locally/server recoverable.

During a section:

- learner always knows section time state;
- navigator exposes answered/partial/unanswered/review states;
- accidental browser refresh restores the section;
- network interruption does not destroy local response work;
- no AI request is needed to continue;
- warnings never cover response text;
- final submit requires confirmation when time remains;
- automatic expiry submission is deterministic and auditable.

## 25. Definition of Done extension

No assessment feature is complete until:

1. its schema is registered;
2. backend structural validator rejects unsupported combinations;
3. frontend registry renders all supported combinations;
4. Practice and Simulation mode policies are tested separately;
5. annotation/strikeout/notepad/review state survives navigation and refresh;
6. mobile/tablet/desktop behavior passes the required widths;
7. Light/Dark/High Contrast pass;
8. keyboard and screen-reader critical flows pass;
9. error/offline/reconnect flows pass;
10. golden combinatorial fixtures pass;
11. real staging API hydration and save flows pass;
12. no ads or AI feedback invade protected exam workspace boundaries.

## 26. Build rule

Codex may not satisfy this contract by implementing separate bespoke screens for particular IQSs/PTs. The accepted implementation is a shared, versioned renderer and component registry driven by validated presentation schema.

## 32. Native-client parity amendment

The Assessment Presentation Schema and UI Capability Manifest are client-agnostic contracts consumed by Web, iOS, and Android. Web and React Native may use different concrete components. Assessment availability is evaluated against the capability manifest of the client/release train on which the version is eligible to run; the canonical AssessmentVersion itself is not forked by client.

For **Web GA**, every required assessment family must satisfy the complete Web capability profile. A missing native concrete renderer does not block Web GA when the canonical schema/API/persistence contract is already native-compatible and the gap is explicitly tracked. For **Native GA**, that platform may not expose an assessment family until its renderer satisfies the required selection, elimination, highlighting, navigation, resource, editor, autosave, recovery, grading, challenge, and accessibility behaviors. No Web-only assessment schema may be introduced merely because native releases later.

Milestone 1/M1.4 foundation acceptance proves the portable presentation, route, authentication, persistence, and client-capability seams at the depth defined by the Build Constitution and Native Platform Specification. It does not require physical-device assessment-renderer, SecureStore/authentication-lifecycle, or real Universal/App Link evidence when the needed platform account/device is unavailable. Those gaps must be recorded without claiming verification and remain mandatory before the applicable Native GA; this scheduling rule never permits a Web-shaped AssessmentVersion, workspace, annotation, autosave, recovery, grading, or evidence contract.

Public/community controls are outside the timed assessment workspace. Discussion, signals, and creator metrics appear only after submission/publication or on public pages and may never distract a learner during a timed simulation section.

---

# PART II - CURRICULUM COVERAGE AND COMPLETENESS

**Status:** Authoritative v1 companion contract  
**Date:** August 12, 2026  
**Controls:** Official NextGen scope ingestion, doctrine/rule completeness, skills/ethics coverage, inventory coverage, learner coverage semantics, scope versioning, and proof of completeness.  
**Read with:** `BARCLIMB_BUILD_CONSTITUTION.md` and `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md`.

---

## 1. Coverage principle

BarClimb may not claim “complete NextGen coverage” because it has a large number of questions. Completeness is proved against the **official NCBE scope effective for the learner’s exam blueprint**.

For each scope version, BarClimb must be able to answer deterministically:

1. What official topics/tasks/rules are in scope?
2. Which are recall-required/starred versus resource-variable?
3. Which are foundational doctrine versus skills-integrated/contextual domains?
4. Which internal curriculum nodes represent each official scope item?
5. Which validated assessments exercise each item?
6. Which items remain underrepresented in inventory?
7. Which items has a particular learner actually demonstrated?

Question count is secondary to this manifest.

---

## 2. V1 official scope baseline

V1 must ingest and version the official NCBE NextGen UBE Content Scope and Blueprint applicable to the target administration rather than permanently encoding one static outline.

The July 2026–February 2027 baseline contains:

### 2.1 Eight Foundational Concepts and Principles

- Business Associations and Relationships;
- Civil Procedure;
- Constitutional Law;
- Contracts;
- Criminal Law and Constitutional Protections of Accused Persons;
- Evidence;
- Real Property;
- Torts.

### 2.2 Seven Foundational Skills

- Issue Spotting and Analysis;
- Investigation and Evaluation;
- Client Counseling and Advising;
- Negotiation and Dispute Resolution;
- Client Relationship and Management;
- Legal Research;
- Legal Writing and Drafting.

### 2.3 Skills task manifest

Every numbered task in the official Foundational Skills and Tasks outline must be represented as a versioned scope item, including all current tasks 1–28 for the July 2026–February 2027 scope.

### 2.4 Selected Model Rules

Selected ABA Model Rules are represented under the versioned Ethics scope and mapped to the official Group B integration restrictions defined in `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md`.

### 2.5 Contextual resource domains

For July 2026 through February 2028, Family Law and Trusts & Estates must be represented as **resource-supplied contextual domains** for skills-focused IQS/PT generation. They are not treated as memorized foundational subjects during that period.

Starting with an exam blueprint where NCBE makes Family Law foundational, the applicable scope version must replace that treatment with the official foundational Family Law outline and knowledge expectations effective for that administration.

---

## 3. Official Scope Manifest

Add canonical models/data structures:

### `curriculum.OfficialScopeVersion`

Minimum fields:

- `id`
- `exam_program_id`
- `name`
- `effective_from`
- `effective_through`
- `source_id`
- `source_checksum`
- `status` (`DRAFT`, `VALIDATING`, `ACTIVE`, `SUPERSEDED`)
- `importer_version`
- `created_at`
- `activated_at`

Exactly one applicable active scope version may resolve for a given exam date/program combination.

### `curriculum.OfficialScopeItem`

Minimum fields:

- `scope_version_id`
- `stable_source_key`
- `parent_id` nullable
- `item_type`
- `ordinal_path`
- `display_name`
- `source_text_summary`
- `source_page`
- `source_locator`
- `starred`
- `knowledge_expectation`
- `resource_treatment`
- `is_leaf`
- `active`
- `source_hash`

Canonical `item_type` values:

- `SUBJECT`
- `SECTION`
- `TOPIC`
- `SUBTOPIC`
- `SKILL_GROUP`
- `SKILL`
- `SKILL_TASK`
- `ETHICS_RULE`
- `CONTEXTUAL_DOMAIN`
- `SCOPE_NOTE`

Canonical `knowledge_expectation` values:

- `RECALL_REQUIRED`
- `RECOGNITION_EXPECTED`
- `RESOURCE_SUPPORTED`
- `SKILL_APPLICATION`
- `NOT_APPLICABLE`

Canonical `resource_treatment` values:

- `NO_RESOURCES`
- `MAY_PROVIDE_RESOURCES`
- `RESOURCES_REQUIRED`
- `FORMAT_DEPENDENT`

Do not infer starred status from typography after import. Store the source-extracted star state explicitly and validate it.

---

## 4. Doctrine graph mapping

`OfficialScopeItem` and `DoctrineNode` are different concepts.

The official manifest mirrors NCBE’s published test scope. The doctrine graph may be richer and may contain derived rules, exceptions, contrasts, issue patterns, skills, ethics nodes, and fact archetypes.

Add mapping:

### `curriculum.ScopeNodeMapping`

- `scope_item_id`
- `doctrine_node_id`
- `mapping_role` (`PRIMARY`, `SUPPORTING`, `DERIVED_DETAIL`)
- `mapping_confidence`
- `provenance`
- `validated_at`

Hard requirements:

- every active official leaf scope item has at least one `PRIMARY` mapping;
- every active doctrine/rule/exception node used for NextGen readiness maps back to at least one active official scope item or an explicitly permitted supplemental/contextual scope;
- no orphan doctrine node may affect readiness.

---

## 5. Import and verification pipeline

Official scope ingestion is a controlled publication pipeline:

`REGISTER_SOURCE`
→ `PARSE`
→ `EXTRACT_HIERARCHY`
→ `EXTRACT_STAR_RESOURCE_METADATA`
→ `NORMALIZE`
→ `DIFF_PRIOR_SCOPE`
→ `MAP_TO_GRAPH`
→ `VALIDATE_COUNTS_AND_STRUCTURE`
→ `HUMAN/ADMIN_EXCEPTION_REVIEW`
→ `ACTIVATE`.

AI may assist extraction and mapping but may not activate a scope version or silently omit source items.

The importer must preserve the official hierarchy and source locator so an admin can trace every manifest item back to its source.

---

## 6. Scope completeness gates

An `OfficialScopeVersion` may become `ACTIVE` only when all of the following equal 100%:

### 6.1 Structural completeness

Every identified official subject, section, topic/subtopic leaf, skills task, selected ethics rule, and required contextual domain is represented.

### 6.2 Mapping completeness

Every active leaf has a primary doctrine/skill/ethics mapping.

### 6.3 Metadata completeness

Every applicable leaf has:

- star/knowledge expectation;
- resource treatment;
- effective version;
- source locator;
- source hash.

### 6.4 Conflict completeness

No unresolved duplicate path, contradictory star state, or ambiguous source mapping remains.

The admin UI must display a blocking coverage audit before activation.

---

## 7. Assessment inventory coverage

Inventory completeness is separate from scope completeness.

For each official leaf/testable unit, compute:

- validated assessment count;
- assessment-family diversity;
- response-type diversity;
- fact-archetype diversity;
- difficulty diversity;
- legal freshness;
- reliability distribution;
- public-content availability where applicable.

### 7.1 Minimum direct assessment coverage

Before BarClimb may claim launch-level complete coverage, every active official leaf/testable unit must be explicitly targeted by at least **two validated assessment exposures**, either as a primary target or an explicitly scored/validated secondary target.

An assessment merely tagged with a subject does not count.

### 7.2 Recall-required/starred topics

Each `RECALL_REQUIRED` leaf must have at least:

- two validated no-resource exposures;
- at least one exam-authentic exposure in a question family permitted by the active blueprint;
- one delayed-reassessment-capable inventory item or equivalent alternate variation.

Selected MRPC rules obey their official format restriction and therefore are not forced into standalone MCQ inventory when the blueprint prohibits that use.

### 7.3 Resource-variable/unstarred topics

Each such leaf must have at least:

- one validated recognition/application exposure without supplied law when blueprint-permitted; and
- one integrated/resource-supported exposure where the concept naturally supports such testing.

The Inventory Planner may satisfy multiple leaves in one authentic multi-doctrine assessment, but each leaf must appear in the immutable Generation Specification and validation record.

### 7.4 Contextual resource domains

Family Law and Trusts & Estates in the pre-July-2028 resource-supplied period require meaningful IQS/PT inventory and skills integration but do not contribute memorization/recall mastery.

---

## 8. Subject coverage proof

A subject is not “complete” because a learner answered many questions.

For each subject BarClimb calculates:

### `ScopeCoverage`

Percentage of active official leaf items for which the learner has sufficient evidence.

### `InventoryCoverage`

Percentage of active official leaf items for which the platform has sufficient validated assessment inventory.

### `RuleCoverage`

Coverage of doctrine/rule nodes mapped to official leaves, weighted so repeated evidence on one rule cannot substitute for untouched rules.

### `FormatCoverage`

Whether the learner has demonstrated the subject across applicable assessment/response types.

### `TransferCoverage`

Whether performance has transferred across sufficiently different fact archetypes/resources.

A user-facing `Subject Coverage 100%` is prohibited unless all required active official leaf groups meet the configured evidence threshold. High performance on a subset may show `Performance 92` while coverage remains materially lower.

---

## 9. Learner evidence mapping

Every scored AssessmentUnit must declare its scope targets before delivery.

`LearnerEvidence` records must retain:

- `official_scope_item_id` where applicable;
- `doctrine_node_id`;
- evidence dimension;
- response type;
- skill target;
- ethics target if applicable;
- resource/no-resource condition;
- item reliability;
- grading confidence;
- fact archetype;
- difficulty;
- timestamp.

No post-hoc AI classification may silently change the scope target of an already completed immutable AssessmentVersion.

---

## 10. Generation requirements

The Learner Assessment Planner and Inventory Planner must query the official manifest before generating.

Generation priority includes:

1. official leaves with zero validated inventory;
2. official leaves below minimum inventory depth;
3. starred/recall topics lacking no-resource variety;
4. missing skill-task combinations;
5. missing ethics integrations;
6. insufficient fact/format diversity;
7. reliability replacement needs;
8. high-demand areas after completeness obligations are satisfied.

A general prompt such as “make a Contracts question” is prohibited in production generation. Every generated assessment must cite specific scope targets in its Generation Specification.

---

## 11. Coverage dashboards for staff

Django Admin or a dedicated staff report must provide:

### Scope Audit

- official items total;
- imported;
- mapped;
- unmapped;
- metadata errors;
- version/source diff.

### Inventory Matrix

Subject → official leaf → assessment counts by:

- MCQ;
- IQS;
- PT;
- response type;
- difficulty;
- fact archetype;
- reliability state;
- freshness state.

### Coverage Gaps

Sortable priority list of:

- zero inventory;
- thin inventory;
- over-reused archetype;
- stale/under-review items;
- skill/ethics gaps.

Launch and scope-version activation gates consume these reports automatically.

---

## 12. Public coverage claims

Marketing may state **complete NextGen scope coverage** only when the active production scope version passes all scope/mapping gates and all official testable leaves satisfy minimum validated inventory coverage.

Until then use narrower language such as:

- `Built across the NextGen subjects and skills`;
- `Growing validated NextGen practice library`.

Do not claim complete coverage based on raw question count.

Public subject hubs may display a `Coverage verified against [scope version]` note only when the corresponding subject audit passes.

---

## 13. Scope version changes

When NCBE publishes a new Content Scope:

1. register the new source/version;
2. import into a candidate manifest;
3. produce machine and human-readable diff;
4. map additions/changes/removals;
5. identify affected assessments;
6. mark affected items for legal/scope revalidation;
7. calculate inventory deficits for new scope;
8. generate/validate required inventory;
9. activate only when completeness gates pass for the target exam period.

Historical attempts remain bound to the scope/assessment versions in effect when completed.

Learners with a future exam date resolve to the scope effective for that date.

---

## 14. Family Law 2028 transition

The system must support a scheduled scope transition without a product rewrite.

Pre-July-2028 behavior:

- Family Law = contextual/resource-supplied skills domain;
- no foundational recall coverage score;
- IQS/PT inventory required.

July 2028+ behavior once applicable official scope is activated:

- Family Law = Foundational Concepts and Principles subject;
- official Family Law outline imported as normal scope hierarchy;
- knowledge expectations/star metadata derived from applicable official scope;
- MCQ/IQS/PT generation permitted according to blueprint;
- learner coverage/readiness includes Family Law.

---

## 15. Trusts & Estates

For the current pre-July-2028 scope treatment, Trusts & Estates remains a resource-supplied contextual domain where required by NCBE. It must not be promoted to a memorized foundational subject unless a later official scope does so.

---

## 16. Ethics completeness

The Ethics contract remains authoritative for broader focused PR/Judicial Ethics practice.

For **NextGen completeness**, only the selected Model Rules and permitted integrations defined by the active official scope affect NextGen readiness. Every selected rule must:

- exist in `OfficialScopeItem` as `ETHICS_RULE`;
- map to canonical ethics nodes;
- preserve subsection limitations;
- preserve comments-excluded status where applicable;
- preserve no-resource/recall requirement;
- have validated integrated IQS inventory consistent with official skill restrictions.

Supplemental Model Rules and Judicial Ethics drills never create missing NextGen coverage obligations unless later added by official scope.

---

## 17. Skills completeness

The seven high-level skills are not enough for completeness. All official numbered skills tasks must be represented and mapped.

Inventory planning must prove meaningful coverage of the task set across applicable assessment families. One generic “legal writing” PT cannot satisfy every drafting/editing task.

Learner skill coverage is based on task-level evidence aggregated upward to the seven skill labels.

---

## 18. Testing requirements

Golden tests must include:

- exact manifest import from a fixed official-scope fixture;
- star/resource metadata preservation;
- missing-leaf detection;
- duplicate-path detection;
- unmapped-leaf activation rejection;
- scope-diff behavior;
- Family Law future-version transition;
- selected MRPC restriction enforcement;
- learner subject coverage remaining below 100% when one required leaf is untouched;
- inventory planner prioritizing uncovered leaves;
- assessment generation refusing missing/invalid scope targets;
- historical attempt remaining bound to superseded scope version.

---

## 19. Definition of complete rule coverage

For BarClimb v1, **complete rule coverage** means:

> Every testable leaf item and skill/ethics obligation in the official scope effective for the applicable exam blueprint has been imported with provenance, mapped to the internal competency graph, represented by sufficient validated assessment inventory consistent with its knowledge/resource/format rules, and is individually traceable in learner and staff coverage reporting.

It does not mean every conceivable rule taught in law school, every rule in an NCBE Sourcebook, or every possible issue variation has its own standalone page or question.

## 25. Community/native amendment

Community popularity cannot define curriculum coverage. Views, comments, reactions, shares, follows, or public-response volume never satisfy an OfficialScopeItem exposure requirement by themselves.

Community data may help the Inventory Planner identify educationally useful misconception patterns or demand, but complete coverage remains governed by official-scope mapping, validated assessment exposure, legal freshness, and applicable response/resource diversity.

All launch clients consume the same official-scope identifiers and coverage semantics. Native Progress views may simplify presentation, but may not calculate or label coverage differently from web.

---

# PART III - ETHICS AND FOCUSED PRACTICE

**Status:** Authoritative v1 companion specification  
**Applies to:** BarClimb NextGen UBE product  
**Purpose:** Define how professional-responsibility content required by the NextGen UBE is modeled and tested, and how BarClimb may additionally offer focused drills in broader ABA Model Rules and judicial ethics without becoming a separate MPRE product or corrupting NextGen readiness analytics.

## 1. Product rule

BarClimb v1 remains a NextGen UBE product. It does not create a separate MPRE exam program, MPRE simulation product, MPRE readiness score, or MPRE subscription.

Practice may nevertheless expose **Focused Practice Collections** that reuse BarClimb's assessment renderer, annotation tools, grading/review experience, history, spaced reassessment, and rule analytics for discrete bodies of rules that are useful to bar applicants.

Initial focused ethics collections are:

- `NEXTGEN_PROFESSIONAL_RESPONSIBILITY` - only the ABA Model Rules/subsections expressly within the active NextGen Content Scope;
- `MODEL_RULES_FOCUSED_DRILL` - broader ABA Model Rules of Professional Conduct practice useful for professional-responsibility/MPRE-style rule drilling;
- `JUDICIAL_ETHICS_FOCUSED_DRILL` - ABA Model Code of Judicial Conduct practice useful for judicial-ethics/MPRE-style rule drilling.

The latter two are supplemental practice collections, not additional NextGen subjects.

## 2. Current NextGen professional-responsibility scope

The active NextGen blueprint must store the selected professional-responsibility rules from the controlling NCBE Content Scope as versioned scope data rather than hard-coded prompt prose.

For the July 2026-February 2027 Content Scope, the enumerated rules are:

- MRPC 1.0 - Terminology
- MRPC 1.1 - Competence
- MRPC 1.2(a) and (d) - Scope of Representation and Allocation of Authority Between Client and Lawyer
- MRPC 1.3 - Diligence
- MRPC 1.4 - Communications
- MRPC 1.6(a) and (c) - Confidentiality of Information
- MRPC 1.7 - Conflict of Interest: Current Clients
- MRPC 3.1 - Meritorious Claims and Contentions
- MRPC 3.3(a)(1)-(2) - Candor Toward the Tribunal
- MRPC 4.1 - Truthfulness in Statements to Others
- MRPC 4.2 - Communication with Person Represented by Counsel
- MRPC 4.3 - Dealing with Unrepresented Persons

The active scope metadata must also encode that, under that blueprint:

- these rules may be assessed in the context of Group B Foundational Skills;
- they may be assessed within integrated question sets;
- they are not assessed in standalone NextGen multiple-choice sections;
- assessment is limited to the enumerated rule text/subsections and excludes comments unless a future official blueprint states otherwise;
- the examinee is expected to rely on recalled knowledge for these rules rather than supplied legal resources.

A later NCBE scope change creates a new `EthicsScopeVersion`; historical assessments remain attached to the scope version under which they were generated.

## 3. Curriculum graph extension

Add ethics as a first-class competency axis without turning Professional Responsibility into a ninth NextGen doctrinal subject.

Canonical node families now include:

- `SUBJECT`
- `DOCTRINE`
- `RULE`
- `EXCEPTION`
- `ISSUE_PATTERN`
- `SKILL`
- `FACT_ARCHETYPE`
- `ETHICS_RULE`
- `JUDICIAL_ETHICS_RULE`
- `TASK`

Ethics nodes may connect to doctrine, skills, tasks, and other ethics nodes through existing and new edge types:

- `TESTED_THROUGH`
- `RELEVANT_TO`
- `CONTRASTS_WITH`
- `PREREQUISITE_FOR`
- `COMMONLY_CONFUSED_WITH`
- `SUPPORTED_BY`
- `INTEGRATES_WITH`

A single canonical MRPC rule node is reused across NextGen-integrated assessments and supplemental focused drills. Scope is carried by the assessment/evidence record, not by duplicating the rule node.

## 4. Knowledge-expectation metadata

Every blueprint-to-node applicability record must support:

- `RECALL_EXPECTED`
- `RESOURCE_PROVIDED`
- `CONTEXT_DEPENDENT`
- `OUT_OF_SCOPE`

This metadata controls generation and readiness credit.

Selected NextGen MRPC rules that official scope requires from memory use `RECALL_EXPECTED` for the applicable blueprint. Other doctrinal areas that are supplied for skills-focused work use `RESOURCE_PROVIDED` or `CONTEXT_DEPENDENT` as appropriate.

## 5. Practice UX

Practice setup remains progressive and uncluttered.

Default entry remains:

- Recommended
- MCQ
- IQS
- PT

Add a secondary action labeled **Focused Practice**.

Focused Practice opens compact collection choices rather than a new product shell:

- Professional Responsibility
- Judicial Ethics
- other future approved focused collections

Within Professional Responsibility, the user may choose:

- `NextGen-selected rules`
- `All Model Rules drill`
- a specific rule/topic
- `Recommended` based on focused-practice evidence

Within Judicial Ethics, the user may choose:

- `Recommended`
- a specific judicial-ethics topic/rule family

The UI must clearly identify supplemental collections as focused practice. It must not imply that judicial ethics is part of the NextGen UBE when it is not within the active NextGen scope.

## 6. Focused drill formats

Focused ethics practice reuses registered BarClimb response components and exam-working tools.

Initial supported drill forms:

- `MCQ_SINGLE`
- `MCQ_MULTI` when pedagogically useful, but never presented as an official MPRE format unless it matches the relevant official format;
- `SHORT_CONSTRUCTED` for rule recall/explanation;
- `MEDIUM_CONSTRUCTED` for application;
- `RULE_RECALL` - a new focused-practice response type for typed or spoken-in-future recall against a canonical rule/rule elements rubric;
- `SCENARIO_CLASSIFICATION` - a registered component that asks whether conduct is permitted, prohibited, required, or otherwise classifiable under the governing rule when the source rule supports that framing.

`RULE_RECALL` and `SCENARIO_CLASSIFICATION` are practice components only and are not eligible for NextGen Simulation unless a future official capability profile permits them.

The existing assessment tools remain available where appropriate:

- answer-choice strike-through;
- four-color highlighting;
- mark/review state in multi-item drills;
- keyboard/touch operation;
- autosave/recovery;
- explanation and rule review after submission;
- Ask BarClimb after submission.

## 7. Assessment-generation rules

### 7.1 NextGen-integrated ethics

Generation must originate from a valid NextGen Generation Specification that includes:

- primary doctrine/context;
- one or more Group B skills/tasks when required by the active blueprint;
- one or more `ETHICS_RULE` targets expressly in the active `EthicsScopeVersion`;
- permitted assessment family, initially IQS under the July 2026-February 2027 scope;
- `knowledge_expectation = RECALL_EXPECTED` for the selected MRPC rule;
- `comments_testable = false` unless the governing official scope changes;
- no supplied copy of the tested MRPC provision when the official scope requires recall.

The generator may not create a standalone NextGen MCQ whose scoring target is one of these MRPC rules when the active official scope prohibits that format.

### 7.2 Supplemental Model Rules drill

Supplemental focused drills may test broader MRPC coverage using BarClimb-authored questions. Their Generation Specification must include:

- `practice_collection = MODEL_RULES_FOCUSED_DRILL`;
- canonical rule/subsection targets;
- source version;
- whether comments are included in the drill objective;
- drill format;
- difficulty;
- distinction traps/common confusions.

### 7.3 Judicial ethics drill

Judicial-ethics drills use the versioned ABA Model Code of Judicial Conduct source set and may cover topics such as judicial independence/impartiality, duties of office, ex parte communications, disqualification, and extrajudicial activities according to the active supplemental scope definition.

They must never be tagged as NextGen-core evidence unless a later official NextGen scope expressly adds them.

## 8. Evidence and analytics isolation

Every learner evidence record must include an `evidence_scope`:

- `NEXTGEN_CORE`
- `SUPPLEMENTAL_MODEL_RULES`
- `SUPPLEMENTAL_JUDICIAL_ETHICS`

and a `competency_dimension`, including where applicable:

- `RULE_RECALL`
- `ISSUE_RECOGNITION`
- `APPLICATION`
- `COUNSELING`
- `NEGOTIATION`
- `CLIENT_MANAGEMENT`
- `WRITING_DRAFTING`

Supplemental evidence can improve the user's focused-practice analytics for the canonical ethics node.

NextGen Readiness may consume supplemental evidence only under strict transfer rules:

1. the canonical ethics rule is within the active NextGen scope;
2. the evidence measures a competency dimension relevant to that scope;
3. supplemental rule-recall evidence may improve `RULE_RECALL` confidence but may not by itself establish NextGen integrated mastery;
4. NextGen proficiency/strong status for an ethics rule requires qualifying NextGen-context evidence, such as application within an eligible IQS/Group B task, once the blueprint requires integrated assessment;
5. judicial-ethics evidence contributes zero to NextGen Readiness unless a future active official blueprint expressly includes it.

The UI may therefore show a user as strong on Rule 1.6 recall but still developing on NextGen-integrated confidentiality application.

## 9. Progress UI

NextGen Progress remains centered on NextGen readiness.

Within Skills & Ethics, expose:

- Foundational Skills
- NextGen Professional Responsibility

For each applicable ethics rule show, when evidence exists:

- rule recall;
- integrated application;
- coverage;
- confidence;
- retention;
- qualifying NextGen evidence count/quality.

Focused Practice has a separate compact progress view for supplemental collections. It does not create a second dashboard or separate product identity.

Judicial Ethics appears only in Focused Practice progress unless it becomes part of an active NextGen blueprint.

## 10. History

History filters add:

- NextGen
- Professional Responsibility
- Judicial Ethics
- focused collection
- rule/rule family

An attempt retains its original `practice_collection` and `evidence_scope` forever even if future scope changes.

## 11. Public content and SEO

NextGen-integrated PR assessment pages may live within the normal `/nextgen/` taxonomy because they are genuine NextGen content.

Supplemental Model Rules and Judicial Ethics pages must not be placed under `/nextgen/` merely for SEO. Use a separate descriptive public taxonomy such as:

- `/professional-responsibility/`
- `/professional-responsibility/model-rules/`
- `/professional-responsibility/judicial-ethics/`

These are focused study resources within BarClimb, not a separately sold MPRE product.

Pages must accurately distinguish:

- what is within the active NextGen Content Scope;
- what is supplemental professional-responsibility practice;
- what is judicial-ethics practice.

## 12. Data model additions

Add or extend:

### `curriculum.EthicsScopeVersion`
- stable id
- exam blueprint/version when applicable
- effective dates
- source provenance
- comments_testable default
- lifecycle state

### `curriculum.EthicsScopeRule`
- scope version
- canonical ethics node
- exact included subsections
- allowed assessment families
- allowed skill/task contexts
- knowledge expectation
- resource provision policy

### `learning.PracticeCollection`
- stable code
- title
- collection type
- active/versioned source set
- counts_toward_nextgen_readiness boolean default false

### `learning.LearnerFocusedState`
- learner
- practice collection
- competency node
- dimension
- performance
- coverage
- confidence
- retention

Extend `LearnerEvidence`, `GenerationSpecification`, `AssessmentVersion`, and `Attempt` with the relevant collection/scope fields.

## 13. API additions

Add:

- `GET /api/v1/practice/focused-collections/`
- `GET /api/v1/practice/focused-collections/{code}/options/`
- `POST /api/v1/practice/focused-collections/{code}/start/`
- `GET /api/v1/progress/focused/`
- `GET /api/v1/progress/ethics/`

Existing attempt/response/annotation/grading endpoints are reused.

## 14. Validation

The validator must reject:

- a NextGen-integrated ethics assessment using an MRPC rule/subsection outside the active official ethics scope;
- comments as scored NextGen content where the active scope excludes them;
- a standalone NextGen MCQ targeting MRPC when the active scope disallows that use;
- supplied MRPC text when the active scope requires recall and the supplied text would answer the tested proposition;
- judicial-ethics content tagged as NextGen Core without explicit active-blueprint authority;
- supplemental focused-drill evidence being treated as full integrated NextGen mastery.

## 15. Golden fixtures

Add at minimum:

1. NextGen IQS combining a doctrinal matter, Group B counseling task, and MRPC 1.6 target;
2. NextGen IQS combining negotiation/client management and MRPC 4.1 or 4.2 as appropriate;
3. validator rejection of standalone NextGen MRPC MCQ under July 2026-February 2027 scope;
4. supplemental Model Rule 1.7 MCQ drill;
5. supplemental typed rule-recall drill;
6. judicial ethics MCQ on disqualification;
7. evidence-transfer test proving supplemental recall can raise recall confidence but cannot alone create NextGen integrated proficiency;
8. test proving judicial-ethics evidence has zero effect on NextGen Readiness;
9. scope-version migration test preserving historical attempts;
10. public-page routing test separating `/nextgen/` from supplemental professional-responsibility content.

## 16. Definition of Done extension

Ethics/focused practice is not complete until:

- official NextGen selected-rule scope is source-versioned;
- NextGen-integrated generation obeys format/context/resource restrictions;
- focused Model Rules and Judicial Ethics collections render through the common assessment system;
- learner evidence remains correctly isolated and transferred only under defined rules;
- Progress accurately distinguishes recall from integrated application;
- supplemental content cannot silently change NextGen Readiness;
- SEO accurately separates NextGen and supplemental content;
- all golden fixtures pass in light/dark, desktop/tablet/mobile, and keyboard flows.

## 26. Community/native amendment

Focused ethics practice is available on Web, iOS, and Android through the same canonical assessment/practice APIs.

A learner may publish an eligible focused-practice response only under the same explicit publication/privacy rules as other responses. Community discussion must clearly label whether a page is official NextGen-integrated ethics practice or supplemental broader Model Rules/Judicial Ethics practice so community/SEO activity never misrepresents supplemental material as NextGen scope.

---

# CONSOLIDATED BUILD RULE

Codex must implement these three parts as one coherent learning system. No client may invent unsupported assessment UI; no assessment may become available without capability and legal validation; no public claim of complete NextGen coverage may be made without the official-scope completeness gates; and supplemental ethics practice must remain analytically isolated from NextGen readiness except where the official blueprint expressly permits transfer.

## 27. Web GA and Native GA assessment-release rules

BarClimb releases commercially on Web before public native store releases. This changes **distribution timing only**, not assessment truth.

- Web GA must ship the full launch assessment/learning scope required by this specification.
- iOS and Android consume the same immutable AssessmentVersions, GenerationSpecifications, RuleObligations, grading contracts, learner evidence, and simulation assemblies.
- A client capability manifest determines whether a given version can be rendered on that client; a native gap never causes a duplicate “mobile version” of the assessment.
- Web GA may proceed while native concrete components remain incomplete, provided no Web-only contract makes later parity structurally impossible and the gap is tracked in client parity.
- Native GA requires full supported-family parity and device/runtime validation under the Native Platform Specification.
- Coverage certification and Web GA “complete current published NextGen scope” claims are curriculum/inventory facts, not claims that every client has already reached public distribution.
- Physical-device assessment interaction, recovery, and link-routing proof that is externally unavailable during Milestone 1 remains a platform-specific Native GA obligation. Automated contract/configuration evidence and a signed build path may satisfy only the M1.4 foundation gate; neither proves the deferred runtime behavior.
