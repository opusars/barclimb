# BarClimb Product Experience & Learning Network Specification

**Status:** Authoritative v1 companion specification.

This document consolidates and supersedes the former User Journey & Experience Contract, Visual Identity & Page Composition Contract, and Community, Network & Growth Contract. It governs the complete public/authenticated journey, visual identity, page composition, username-first public identity, publication/community behavior, social learning loops, healthy gamification, creator feedback, Circles, moderation, viral sharing, and network-growth constraints.

If a requirement here conflicts with a higher-level invariant in `BARCLIMB_BUILD_CONSTITUTION.md`, the Build Constitution controls. Otherwise this document is authoritative for experience/community behavior.

---

# PART I - USER JOURNEY AND EXPERIENCE

**Status:** Authoritative companion build contract  
**Applies to:** BarClimb v1 NextGen UBE product  
**Incorporated by:** `BARCLIMB_BUILD_CONSTITUTION.md`  
**Companion contracts:** `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md`, `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md`

---

## 1. Purpose

BarClimb must not merely be feature-complete. It must feel coherent, immediate, trustworthy, modern, and unusually useful from the first public page through repeated study sessions and paid conversion.

This contract governs the user journey above individual assessment interactions. It defines how anonymous visitors, SEO visitors, newly registered learners, free learners, paid learners, and returning learners move through the product without dead ends, duplicated work, unnecessary setup, or abrupt context loss.

The design goal is **fast proof of value before commitment, then progressively deeper personalization after commitment**.

---

## 2. Experience principles

The following are hard requirements:

1. **Value before registration.** A public visitor can experience genuine BarClimb teaching value before creating an account.
2. **One continuous journey.** Anonymous work can be claimed after signup when technically and legally safe; signup must not unnecessarily erase progress.
3. **Progressive disclosure.** Ask only for information needed for the next useful action.
4. **No dead ends.** Every major state offers a clear next action, recovery path, or explanation.
5. **One dominant action per state.** The interface makes the best next action unmistakable.
6. **Trust before persuasion.** Explain what is being measured, what AI did, what sources/blueprints apply, and what is not yet known.
7. **Earned personalization.** BarClimb infers ability from use instead of forcing a long diagnostic questionnaire.
8. **Context preservation.** Navigating resources, signing up, changing devices, refreshing, or returning later should preserve useful state wherever feasible.
9. **Respectful monetization.** Ads and upgrade prompts never interfere with timed examination fidelity, response entry, legal resources, grading trust, or accessibility.
10. **Fast perceived response.** Reuse validated inventory when appropriate, prefetch likely next actions, use skeletons rather than dead screens, and never make the user wonder whether the app registered an action.
11. **Delight through competence.** "Amazing" means the app feels aware of what the learner is doing, removes friction, remembers state, explains results clearly, and recommends the next useful action. Decorative animation is secondary.
12. **Mobile is a real product.** Phone users receive purpose-built flows rather than shrunken desktop layouts.

---

## 3. User states and canonical journeys

BarClimb recognizes these user journey states:

- `ANONYMOUS_DISCOVERY`
- `ANONYMOUS_ACTIVE`
- `SIGNUP_IN_PROGRESS`
- `NEW_FREE_LEARNER`
- `ACTIVE_FREE_LEARNER`
- `ACTIVE_PLUS_LEARNER`
- `RETURNING_LEARNER`
- `QUOTA_LIMITED`
- `PAYMENT_RECOVERY`
- `DORMANT_RETURN`

The frontend may not infer entitlement from local UI state. Django remains authoritative for account, quota, subscription, and saved-learning state.

---

## 4. Public homepage journey

### 4.1 Above-the-fold job

The public homepage must answer within one screen:

- What is BarClimb?
- Is it specifically for NextGen?
- What can I do right now?

Primary CTA:

**Try a NextGen Question**

Secondary CTA:

**See How BarClimb Works**

Existing account path:

**Sign in**

The homepage must not require signup before a visitor can see an authentic assessment experience.

### 4.2 Proof blocks

The homepage should demonstrate the product rather than only describe it. Required content concepts:

- Practice MCQ, IQS, and PT
- realistic NextGen tools/workspaces
- AI grading for constructed responses
- coverage across subject, doctrine, rule, issue, skills, ethics where applicable
- adaptive next-practice recommendations
- full simulation
- public growing study library

The page must avoid unsupported claims such as guaranteed passing or predictive pass probability.

### 4.3 Live sample

At least one public sample assessment or interactive excerpt should be reachable from the homepage in one action.

---

## 5. SEO-entry journey

A user arriving from search may never see the homepage first. Every indexable public doctrine or assessment page must therefore function as a complete first landing experience.

### 5.1 Public assessment page structure

Required order, adapted to the assessment type:

1. clear title and assessment identity;
2. subject/doctrine/type metadata;
3. substantive problem/content immediately visible;
4. interactive attempt CTA where allowed;
5. explanation/answer gated by an intentional reveal or submission action;
6. anonymous learner example when publication policy allows;
7. BarClimb grading/teaching analysis;
8. rule/issue explanation;
9. aggregate BarClimb insight when sufficiently supported;
10. reliability/freshness signal;
11. related assessments and doctrine links;
12. clear CTA to continue practicing;
13. share controls.

Ads may appear only in approved zones and may not interrupt the logical connection between a prompt and its response controls.

### 5.2 SEO visitor conversion

After meaningful value has been delivered, the page may invite:

**Practice another like this**

If the visitor starts an anonymous interactive attempt, BarClimb should avoid interrupting with signup until a natural value boundary, such as after submission or before persistence/advanced feedback.

### 5.3 Anonymous answer preservation

Where technically safe, an anonymous attempt receives an ephemeral signed identifier and local recovery token. If the visitor creates an account during the same browser journey, the app offers:

**Save this attempt to my account**

The backend performs ownership-safe conversion; the client does not simply relabel anonymous data.

Anonymous attempts expire under the retention contract and do not affect persistent learner analytics unless claimed by an account.

---

## 6. Signup and authentication journey

### 6.1 Signup fields

Initial signup should require only what is needed to create and secure an account:

- email;
- unique username used for public/community identity;
- password or approved passwordless/OAuth alternative if later selected by the implementation contract;
- acceptance of Terms, Privacy notices, Community Standards, and the v1 minimum-age requirement (18+).

Real name and date of birth are not requested for an ordinary learner account.

Do not require jurisdiction, law school, demographic data, study hours, phone number, or marketing consent.

### 6.2 Preserve context

Signup must preserve the referring destination and, where applicable, the current anonymous attempt.

After verification/authentication, return the learner to the intended experience rather than a generic dashboard unless onboarding must run first.

### 6.3 Email verification

If email verification is required, the app may allow safe limited use before verification but must clearly explain any actions that require verified identity. Verification links return users to the relevant product state.

---

## 7. New learner onboarding

Onboarding is intentionally lightweight and may appear as a focused modal/flow rather than a separate multi-page questionnaire.

Required questions:

1. **When do you expect to take the NextGen UBE?**
   - known exam date/session;
   - approximate date;
   - not scheduled yet.
2. **Where are you in preparation?**
   - just starting;
   - actively studying;
   - returning/re-taking or already experienced.

V1 does not ask jurisdiction because BarClimb v1 is NextGen-only.

Optional, skippable preference:

- default Practice difficulty: Adaptive recommended.

On completion, do not dump the user into analytics with no evidence. Route to a first useful action.

---

## 8. First-session experience

### 8.1 First-run recommendation

New learners see:

**Build my starting picture**

This launches a short baseline practice experience using normal BarClimb assessment mechanics. It is not presented as a mandatory diagnostic exam.

Alternate actions:

- Choose what to practice
- Explore public library

### 8.2 Baseline session

The baseline should be short enough to finish, broad enough to generate initial evidence, and composed from validated inventory. It may combine a small number of MCQs and at least one brief constructed-response task when appropriate to the current blueprint and learner experience.

The session should generally take about 10-20 minutes, configurable by blueprint/product policy.

### 8.3 First-win result

After the first completed session, the results experience must immediately answer:

- What did I do well?
- What should I improve?
- What did BarClimb actually observe?
- What should I do next?

The app should reveal the beginnings of the learner map rather than pretending comprehensive knowledge after minimal evidence.

Example presentation:

- **Evidence: promising, limited evidence**
- **Contracts: needs more coverage**
- **Issue spotting: strong first signal**
- **Written application: not enough evidence yet**

Primary CTA:

**Practice the next recommended skill**

Secondary:

**View my Progress**

---

## 9. Authenticated home journey

The authenticated home remains action-first.

Required priority:

1. **Recommended Next** - one high-value recommendation with reason;
2. **Practice**;
3. **Simulate**;
4. **Progress**;
5. **Continue** an unfinished eligible attempt if one exists;
6. recent activity/history access.

If an unfinished attempt exists, a prominent but non-blocking **Resume** affordance should appear before starting a conflicting duplicate attempt.

The home screen must not become a grid of metrics. Metrics belong in Progress.

---

## 10. Practice setup journey

Practice uses progressive disclosure.

Step 1: assessment family

- MCQ
- Integrated Question Set
- Performance Task
- Focused Practice

Step 2: subject/scope

- Recommended
- Random
- specific subject/topic as allowed

Step 3: difficulty

- Adaptive
- Foundational
- Exam Level
- Stretch

Step 4: family-specific options only when they materially change the experience.

For IQS:

- Surprise Me
- Balanced
- Writing Emphasis
- Skills Emphasis

For PT:

- Surprise Me
- Standard PT
- Legal Research PT

For Focused Practice:

- NextGen-selected Professional Responsibility
- broader Model Rules drill
- Judicial Ethics drill
- specific rule/topic where supported

The default path from Practice to an assessment should take only a few decisions.

---

## 11. In-assessment journey

All requirements in `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md` apply.

Additional journey rules:

- submission always provides immediate visual confirmation;
- destructive submission/section-completion actions require appropriate confirmation when irreversible;
- the app warns about unanswered required units before final submission when navigation policy allows;
- the user always knows current question/unit, total progression, save state, and timed status where applicable;
- leaving an in-progress assessment triggers a safe-exit path rather than silent loss;
- Practice provides clear separation between working state and post-submission teaching state;
- Simulation remains fidelity-first and suppresses tutoring/feedback until allowed.

---

## 12. Result and feedback journey

Results must be layered rather than overwhelming.

### Layer 1: outcome

- score/result appropriate to assessment type;
- concise strongest signal;
- concise biggest improvement opportunity.

### Layer 2: why

- answer explanations or rubric breakdown;
- cited excerpts from learner response where supported;
- missed issues/rules/facts;
- grading confidence where material.

### Layer 3: learning

- improved approach;
- model/improved response where appropriate;
- relevant doctrine links;
- Ask BarClimb.

### Layer 4: next action

- recommended next assessment;
- alternate choice to practice another topic;
- Progress update.

The result page must never end with only a score.

---

## 13. Progress journey

Progress answers four learner questions:

1. **How ready am I?**
2. **What have I actually covered?**
3. **Where am I strong/weak?**
4. **What should I do next?**

Top-level view uses:

- Readiness Index when evidence is sufficient;
- Evidence completeness;
- subject coverage;
- one or two material skill/ethics signals;
- current recommended priority.

Drilldown hierarchy:

Subject -> doctrine -> rule/issue -> evidence dimensions.

Display Performance, Coverage, Confidence, and Retention progressively; do not force all four metrics into every summary card.

Focused Practice analytics remain visibly separate from NextGen readiness where required by the ethics contract.

---

## 14. History journey

History is not an archive dump. It supports study review.

Required filters:

- MCQ / IQS / PT / Focused Practice / Simulation;
- subject;
- date;
- score/performance;
- timed/untimed;
- completed/in-progress where applicable.

Opening an attempt restores the exact historical AssessmentVersion, response, grade, annotations/review data where retained, and related feedback. Historical records may not silently change because an assessment is later revised.

---

## 15. Return journey

### 15.1 Normal return

Returning learner lands on a home state tailored to current context:

- resume unfinished work;
- recommended next practice;
- upcoming exam urgency if known;
- reassessment due because of retention decay;
- recent progress signal.

Avoid generic greetings with no useful action.

### 15.2 Dormant return

After a meaningful inactivity interval, do not punish the learner with a streak reset or guilt message.

Show:

**Welcome back. Here's the fastest way to restart.**

Then one recommended short assessment based on prior evidence and retention uncertainty.

### 15.3 Cross-device return

Completed/saved server state, Progress, History, preferences, theme, subscription, and eligible annotations/workspace state synchronize across devices after authentication.

Local recovery remains device-specific and is only a fallback.

---

## 16. Quota and upgrade journey

### 16.1 Upgrade philosophy

Free limits are transparent before the learner invests substantial time. Do not spring an unexpected paywall at final submission.

### 16.2 Soft upgrade moments

Good upgrade moments include:

- after the learner receives useful feedback;
- when advanced analytics are visibly available but locked;
- when requesting a paid-only PT/full simulation;
- when a quota is nearly exhausted;
- after repeated usage demonstrates value.

Bad upgrade moments include:

- while typing a response;
- during a timed section;
- before showing promised grading on an already-started free assessment;
- as an interstitial blocking public educational content solely to force signup/payment.

### 16.3 Quota reached

When a free quota is exhausted, show:

- exactly what limit was reached;
- when it resets;
- what free actions remain;
- BarClimb+ benefits relevant to the current intent;
- clear upgrade CTA;
- no deceptive countdown.

### 16.4 Checkout continuity

Purchase return must restore the intended action. If the user tried to start a PT, successful upgrade returns them to that PT/start flow, not merely Account Billing. Web uses Stripe; iOS and Android use the platform-appropriate native purchase flow.

Payment failure leaves the account usable at its prior entitlement and provides recovery.

---

## 17. Advertising journey

Advertising is part of the free-user experience but must remain subordinate to learning.

- BarClimb+ has no ads.
- Public/free surfaces use the ad decision hierarchy defined in the Constitution.
- No ad appears inside answer choices, question stems, legal resources, response editors, notepads, grading evidence, or live timed sections.
- Ads do not imitate recommendations, feedback, system messages, or navigation.
- Direct sponsor creative is clearly labeled `Sponsored` or `Advertisement`.
- Sponsor targeting never receives private learner performance data.

The app reserves ad space to prevent layout shift.

---

## 18. Trust and provenance journey

BarClimb must make AI-powered assessment feel credible rather than magical.

At appropriate detail levels users can see:

- assessment type;
- blueprint/content-scope version when useful;
- reliability label;
- legal freshness/currentness status when public/relevant;
- whether an item is emerging, reliable, or established;
- grading rubric criteria for constructed responses;
- ability to report a problem;
- regrade path where applicable.

Do not expose internal chain-of-thought or verbose system prompts.

Public pages must distinguish BarClimb material from official NCBE material and maintain the independent-platform disclaimer.

---

## 19. Search and discovery journey

Search must support intent rather than only exact text.

User may search by:

- subject;
- doctrine;
- rule;
- issue;
- assessment type;
- skill;
- ethics rule where applicable.

Search results display useful metadata and a clear action:

- Learn
- Practice
- Review

No zero-result dead end. Offer nearby topics or broader search when possible.

---

## 20. Help and support journey

Every authenticated area has access to concise Help without obscuring the primary task.

Required paths:

- assessment-specific "Report a problem";
- general support/contact form;
- billing help;
- privacy/data rights;
- sponsor help for sponsor accounts.

Support submissions create structured internal records with category, user/account context, page/assessment identifier where relevant, and safe diagnostic metadata. Do not attach raw sensitive response text unless necessary and disclosed.

The user receives confirmation that the request was received.

---

## 21. Empty, loading, and error states

Every major screen requires explicit designed states.

### Empty Progress

Do not show blank charts. Explain that BarClimb needs evidence and offer **Start a short baseline**.

### Empty History

Offer **Start Practice**.

### No recommendation

Explain why and offer appropriate practice selection.

### Loading

Use skeletons/placeholders that preserve layout. For genuine AI work, show concise meaningful status without inventing exact completion times.

### Recoverable error

Keep completed input/state, explain what failed, and offer retry/fallback.

### Fatal/unavailable state

Provide safe return path and preserve recoverable work.

Raw provider exceptions are never user-facing.

---

## 22. Delight and microinteraction contract

The app should feel alive but disciplined.

Allowed delight patterns:

- subtle progress animation after submission;
- smooth resource/tab transitions;
- concise success acknowledgment;
- immediate saved-state feedback;
- intelligent preselection of Recommended practice;
- restrained celebration when meaningful coverage/mastery milestones are earned;
- useful comparison such as "You improved on this issue since your last attempt" when statistically justified.

Avoid:

- confetti after ordinary clicks;
- casino-like streak mechanics;
- guilt notifications;
- excessive badges;
- motion in timed Simulation;
- fake urgency.

All motion respects `prefers-reduced-motion`.

---

## 23. Notification journey

Notifications exist to continue a learning objective, not create noise.

Launch channels:

- in-app state;
- email via SendGrid.

Permitted learning notifications include:

- delayed grading complete;
- optional weekly progress digest;
- exam-date reminders;
- optional reassessment due.

Default study-marketing frequency is conservative and user-controlled.

No daily streak-pressure notifications by default.

---

## 24. Conversion instrumentation

The product must measure journey friction without sending private learner content to marketing analytics.

Required first-party funnel events include:

- `public_page_viewed`
- `public_assessment_started`
- `public_assessment_submitted`
- `signup_started`
- `signup_completed`
- `anonymous_attempt_claimed`
- `onboarding_started`
- `onboarding_completed`
- `baseline_started`
- `baseline_completed`
- `practice_setup_started`
- `assessment_started`
- `assessment_completed`
- `results_viewed`
- `recommendation_accepted`
- `progress_viewed`
- `quota_warning_shown`
- `quota_reached`
- `upgrade_started`
- `checkout_completed`
- `subscription_activated`
- `return_session_started`

No event payload may contain the full text of a learner's legal response.

---

## 25. Journey performance requirements

To feel modern:

- public pages must render meaningful server-side content before client enhancement;
- normal authenticated navigation must not require full page reloads;
- validated inventory should open immediately under normal conditions;
- likely next assessment metadata may be prefetched when safe;
- resource switching is local and immediate once resources are loaded;
- save indicators update quickly and accurately;
- the app must never intentionally delay a result merely to simulate AI work.

---

## 26. Accessibility journey requirements

WCAG 2.2 AA target applies to the complete journey, including:

- cookie controls;
- signup/onboarding;
- menus;
- paywalls;
- ads;
- assessment tools;
- result visualizations;
- Progress;
- sponsor flows.

Keyboard focus must move predictably after dynamic transitions, dialogs must trap/restore focus correctly, status updates use appropriate live regions, and color is never the sole indicator of performance/state.

---

## 27. Canonical route map

### Public

- `/`
- `/nextgen/`
- `/nextgen/mcq/`
- `/nextgen/iqs/`
- `/nextgen/performance-tasks/`
- `/nextgen/{subject}/`
- `/nextgen/{subject}/{doctrine}/`
- `/nextgen/{subject}/{doctrine}/{assessment-slug}/`
- `/professional-responsibility/`
- `/professional-responsibility/model-rules/`
- `/professional-responsibility/judicial-ethics/`
- `/search/`
- `/pricing/`
- `/advertise/`
- `/privacy/`
- `/cookies/`
- `/terms/`
- `/login/`
- `/signup/`

### Learner app

- `/app/`
- `/app/practice/`
- `/app/attempts/{id}/`
- `/app/attempts/{id}/results/`
- `/app/simulate/`
- `/app/simulations/{id}/`
- `/app/progress/`
- `/app/progress/{node-id}/`
- `/app/history/`
- `/app/search/`
- `/app/account/`
- `/app/billing/`
- `/app/privacy/`

### Sponsor

- `/sponsor/`
- `/sponsor/campaigns/`
- `/sponsor/campaigns/{id}/`
- `/sponsor/billing/`

Routes may be refined only if semantic behavior is preserved and the API/SEO contracts are updated in the same change.

---

## 28. Page-state matrix requirement

Before a screen is accepted, implementation documentation must enumerate at least:

- anonymous/authenticated state;
- Free/Plus state;
- Light/Dark/System/assessment-high-contrast where applicable;
- mobile/tablet/desktop behavior;
- loading;
- empty;
- success;
- recoverable failure;
- permission/quota state;
- offline/reconnect where relevant.

A screen without its required state matrix is incomplete.

---

## 29. Journey E2E golden flows

The following must pass in staging before launch:

1. Search-engine-style entry -> public MCQ -> answer -> explanation -> signup -> claimed attempt -> Progress.
2. Public IQS page -> browse resources -> start limited interaction -> signup -> resume context.
3. Homepage -> Try a NextGen Question -> complete -> signup -> lightweight onboarding -> first recommendation.
4. New account -> baseline -> results -> Progress -> recommended practice -> second assessment.
5. Returning Free learner -> Resume unfinished IQS -> autosave -> submit -> quota warning -> continue available free action.
6. Free learner -> paid-only PT -> transparent upgrade -> Stripe test Checkout -> entitlement webhook -> return to PT start -> complete without ads.
7. Returning Plus learner -> reassessment recommendation -> complete -> Progress update.
8. Dormant learner -> return email/deep link -> short restart recommendation -> completed practice.
9. Constructed response -> grading delayed -> leave page -> email/in-app availability -> result opens correct attempt.
10. Assessment problem -> report challenge -> confirmation -> later assessment status update does not corrupt historical result.
11. Mobile public page -> signup -> mobile practice -> switch resource/response repeatedly -> refresh -> recover -> submit.
12. Theme System -> Dark OS -> authenticated cross-device preference synchronization.
13. Cookie rejection -> contextual/house ad fallback as allowed -> core product remains functional.
14. Sponsor purchase journey -> approved creative -> Stripe payment -> campaign scheduled -> sponsor metrics visible.
15. Account deletion/privacy request -> appropriate confirmation and data-rights state.

---

## 30. Experience quality gate

A milestone containing user-facing functionality may not satisfy Definition of Done unless reviewers can answer **yes** to all applicable questions:

- Can a first-time user understand the page without prior explanation?
- Is the primary next action obvious?
- Can a phone user complete the same core objective without fighting the layout?
- Is state preserved through ordinary navigation and recoverable failures?
- Does the app explain what just happened after an important action?
- Does every result lead naturally to learning or progress?
- Are upgrade prompts placed after demonstrated value or at transparent entitlement boundaries?
- Can the user recover from an error without losing work?
- Are trust, reliability, and AI boundaries understandable where material?
- Does the experience remain good with ads disabled, blocked, unavailable, or replaced by direct/house inventory?
- Is the experience usable by keyboard and screen reader?
- Is there any place where Codex substituted a generic admin-looking form for an intentionally designed learner experience?

Any "no" blocks milestone completion.

---

## 31. Product acceptance standard: AMAZING

For BarClimb, "amazing" is operationally defined as:

- **Immediate:** the learner reaches real value quickly;
- **Clear:** every screen has obvious purpose and next action;
- **Adaptive:** recommendations reflect actual evidence rather than generic sequencing;
- **Remembering:** the system preserves work, preferences, progress, and context;
- **Credible:** assessments, grading, reliability, and scope feel transparent and controlled;
- **Fluid:** resource-heavy work remains fast and comfortable across devices;
- **Rewarding:** progress becomes visible after meaningful effort;
- **Respectful:** monetization, ads, notifications, and AI never overpower the learning objective;
- **Resilient:** provider failures, refreshes, connectivity issues, and retries do not casually destroy work;
- **Focused:** sophisticated capabilities do not create a cluttered interface.

A feature-rich but confusing, slow, generic, brittle, or visually unfinished implementation fails this contract even if its endpoints and unit tests pass.


# PART IV — COMMUNITY AND NATIVE JOURNEYS

## 32. Username and public-identity journey

Public identity is username-first. The learner chooses a unique username during signup/account creation. Real names are neither required nor exposed by default.

The username step must explain its purpose in one sentence: it is the identity used if the learner publishes, comments, joins a Circle, or appears in community surfaces.

The learner may complete private study before customizing a public profile. BarClimb must never make public contribution mandatory for learning access.

## 33. Publish-response journey

After a graded eligible response, publication is an earned optional action, never a prechecked checkbox.

Flow:

1. learner receives the full private result first;
2. `Publish response` offers a preview;
3. learner chooses username attribution or explicit anonymous publication where supported;
4. learner sees exactly which response/grade/explanation fields will be public;
5. privacy/PII scrub and content eligibility run;
6. learner confirms;
7. publication receives stable canonical URL;
8. share/community controls appear;
9. learner can later withdraw publication from the response or Privacy & Data settings.

The result may say what becomes possible after publication (discussion, views, educational signals) but may not pressure the learner to expose private work.

## 34. Creator-return journey

A user who published content should have a reason to return that is based on usefulness, not vanity alone.

Creator surfaces can show:

- qualified views
- Helpful / Sharp Analysis / Clear Explanation / New Angle counts
- replies
- saves
- practice starts attributable to the page where measurement supports it

Notification examples route directly to the contribution/thread. Self-views and bot-like refresh activity do not inflate the creator experience.

## 35. Discussion journey

Public assessment/response pages include a contextual discussion layer after the educational content.

A learner can:

- read a bounded set of high-quality/top/recent comments;
- reply;
- use educational signals;
- follow the thread;
- report content;
- block a username;
- mute the thread.

After discussion, the primary CTA remains educational: **Try this assessment**, **Compare your answer**, or **Practice this rule**.

No public/global random chat, DMs, or infinite generic feed is part of v1.

## 36. Community Pulse journey

Authenticated Home may contain a finite `Community Pulse` below the dominant Recommended Next/Readiness actions.

Examples:

- a strong response in a doctrine the learner has recently practiced;
- a discussion about a misconception relevant to recent study;
- a high-quality new angle on a question the learner completed;
- Circle activity.

The module is intentionally small. Completion of its finite set returns the learner to study rather than auto-loading endless content.

## 37. Study Circle journey

A learner may create or join an invite-only Circle using a link/code.

Initial Circle journey:

create/join → see usernames → share existing assessment/response → discuss → optionally start group challenge → return to own learner plan.

Circle participation never exposes private readiness or private responses unless the learner explicitly shares/publishes them.

## 38. Healthy gamification journey

BarClimb uses `Momentum`, meaningful learning achievements, and contribution achievements.

Momentum emphasizes consistent meaningful study across a week or multiple weeks. Missing one calendar day does not create a catastrophic reset.

Achievement celebrations are concise and skippable. They never block the result or next-practice action.

Public display of an achievement is opt-in.

## 39. Cross-platform acquisition journey

Canonical public URLs are always useful on the web.

If iOS/Android is installed, eligible links open the exact native object through Universal/App Links. If not installed, the web page remains complete and can offer a platform-appropriate app-install CTA without obscuring the content.

Canonical viral loop example:

SEO/share → public response → discussion/comparison → attempt → signup/claim → app install or continue web → recommended practice → optional publish/share.

## 40. Native first-run journey

Native app first run must not be a second onboarding universe.

Existing account:

install → sign in → server preferences/history/state appear → resume/recommendation.

New account:

install → signup with username identity → minimal exam-date/experience onboarding → recommended practice.

Push-permission request should occur contextually after the learner has seen a benefit such as delayed grading or retention reminders, not as an unexplained first-screen system dialog.

## 41. Mobile purchase journey

Upgrade returns the learner to the study action that triggered it.

Web uses the web purchase flow. iOS and Android use the platform-appropriate native purchase flow. After verified entitlement, all clients display the same Plus access.

Native must provide Restore Purchases and clear subscription-management guidance based on purchase source.

## 42. Native offline/recovery journey

During ordinary practice, temporary connectivity loss must produce a visible Offline state while preserving work locally. Reconnection syncs safely; unresolved conflicts surface a recovery choice.

The learner must not discover data loss after reopening the app.

## 43. Community/mobile journey golden flows

In addition to §29, launch E2E includes:

- SEO/share → public response → installed-app deep link → same response → attempt;
- private result → publish → creator view → reply/signal notification → exact thread;
- report abusive comment → block username → moderator action;
- Circle invite → native/web join → share assessment → discussion;
- native purchase → verified Plus → web recognizes entitlement;
- fresh-device restore purchase;
- mobile IQS/PT background/relaunch recovery;
- dormant learner push → exact retention practice rather than generic Home.

---

# PART II - VISUAL IDENTITY AND PAGE COMPOSITION

**Status:** Authoritative v1 companion contract  
**Date:** August 12, 2026  
**Controls:** Brand expression, visual system, page composition, responsive composition, density, motion, and visual acceptance.  
**Read with:** `BARCLIMB_BUILD_CONSTITUTION.md`, `BARCLIMB_LEARNING_ASSESSMENT_SPEC.md`, and `BARCLIMB_PRODUCT_EXPERIENCE_NETWORK_SPEC.md`.

---

## 1. Brand thesis

BarClimb must look like a serious modern legal-intelligence product, not a conventional LMS, law-school portal, generic AI chatbot, videogame, or courthouse-template website.

The visual idea is **precision + ascent + momentum**. The “climb” concept appears through progress, elevation, directional composition, contour/elevation motifs, and increasingly complete competence—not literal mountains, cartoon climbers, towers, or decorative gavels.

The product should feel:

- fast;
- premium;
- exact;
- calm under pressure;
- technologically current;
- visibly designed for legal work;
- approachable enough to use daily.

Do not copy Domino’s colors, typography, or branding. Take only the interaction lesson: obvious primary actions, large usable targets, progressive disclosure, and a system that feels transactional and immediate rather than menu-heavy.

---

## 2. Logo and brand marks

### 2.1 Wordmark

Primary mark: `BarClimb` wordmark. Keep the mark compact enough for a 44–56px application header.

### 2.2 Symbol

A secondary symbol may use a minimal ascending bar/step or abstract `B/C` climb mark. It must remain legible at favicon size and may not resemble an official government, court, or NCBE seal.

### 2.3 Prohibited motifs

Do not build the identity around:

- gavels;
- courthouse columns;
- scales of justice;
- graduation caps;
- generic mountain photography;
- fake legal seals;
- neon AI brains;
- chat bubbles as the main brand identity.

---

## 3. Color system

Colors are semantic tokens, never hard-coded ad hoc in components.

### 3.1 Core brand palette

- `--bc-brand-700`: `#1E3FA8`
- `--bc-brand-600`: `#2754D7`
- `--bc-brand-500`: `#3568F5`
- `--bc-brand-100`: `#EAF0FF`
- `--bc-signal`: `#12A594`

Brand blue is the primary action/accent. Signal teal is reserved for selected positive/active data accents and may not compete with the primary CTA.

### 3.2 Light theme

- canvas: `#F6F8FB`
- surface: `#FFFFFF`
- elevated surface: `#FFFFFF`
- text: `#111827`
- muted text: `#5E6878`
- subtle text: `#7A8493`
- border: `#DDE3EC`
- strong border: `#C8D0DC`
- success: `#16805A`
- warning: `#A9650A`
- danger: `#B42318`
- focus: brand-500

### 3.3 Dark theme

- canvas: `#0C1119`
- surface: `#121925`
- elevated surface: `#182231`
- text: `#F4F7FB`
- muted text: `#AAB4C2`
- subtle text: `#8390A1`
- border: `#293548`
- strong border: `#3A4960`
- primary interactive: `#6F95FF`
- success: `#41B98B`
- warning: `#E0A348`
- danger: `#F07167`

### 3.4 High-contrast assessment mode

High-contrast is a separate assessment display profile, not simply dark mode. It must meet the official-capability profile requirements and must never hide semantic state solely through color.

### 3.5 Usage rules

- No gradients on ordinary cards or assessment surfaces.
- Marketing may use one restrained brand wash or contour field, but not psychedelic gradients.
- Red is reserved for destructive/error states.
- Green is not used as the only indication of a correct answer.
- Subject identity must not rely on eight unrelated bright colors; subjects use text/iconography and restrained secondary accents.

---

## 4. Typography

Primary UI family: **Inter** with robust system sans-serif fallback.

Legal-source and long-form assessment text may use the same family for consistency; do not introduce decorative serif fonts unless future usability testing demonstrates a reading benefit.

Desktop scale:

- Display: 48/56, 700, marketing only
- H1: 36/44, 700
- H2: 28/36, 650–700
- H3: 22/30, 650
- Body: 16/25, 400
- Legal reading: 17/28, 400
- Small/supporting: 14/20, 400–500
- Data value: 28–36, 650–700 depending context

Mobile scale reduces display/H1 while preserving 16px minimum body controls and comfortable legal reading.

Maximum ordinary reading width: approximately 72–80 characters. Assessment resources may be wider only when layout requires split-pane work.

---

## 5. Shape, elevation, and density

- Control radius: 8px.
- Standard panel radius: 12px.
- Marketing feature surface: maximum 16px.
- Shadows are subtle and rare; border + surface contrast is preferred.
- Never create a dashboard made of dozens of floating cards.
- Primary surfaces use whitespace and hierarchy rather than decorative containers.
- Legal workspaces prioritize density and screen real estate over marketing decoration.

---

## 6. Iconography

Use one consistent outline icon family. Icons support labels; they do not replace ambiguous text.

Canonical concepts requiring icons include:

- Practice;
- Simulate;
- Progress;
- Search;
- History;
- highlight;
- strike/eliminate;
- flag/review;
- resources;
- notepad;
- timer;
- theme;
- account;
- save state;
- reliability/freshness.

Icons must be visually simple and readable at 16–24px.

---

## 7. Motion

Motion communicates continuity, not spectacle.

- micro-state: 120–180ms;
- normal panel transition: 180–260ms;
- avoid parallax in the authenticated study product;
- no animation while the user is actively typing unless directly related to save state;
- simulation mode suppresses nonessential motion;
- respect `prefers-reduced-motion`.

A subtle upward/forward transition may reinforce “climb” after completing meaningful work, but never delay the next action.

---

# PART II — PAGE COMPOSITION

## 8. Global public shell

Desktop header composition:

`Logo | Practice | NextGen Library | How It Works | Pricing | Advertise | Sign In | Start Free`

- `Start Free` is the dominant header CTA.
- Public navigation is sticky only when it does not consume excessive vertical space.
- Mobile header uses logo, Start Free, and compact menu.

Public footer groups:

- Product;
- NextGen Library;
- Company/Support;
- Advertise;
- Legal/Privacy;
- independent-platform disclaimer.

Do not place ads in the primary global header or navigation.

---

## 9. Public homepage composition

### 9.1 Hero

Desktop: two-column composition.

Left:

- eyebrow: `Built for the NextGen UBE`;
- H1 focused on practicing the exam and knowing what remains untested;
- 1–2 sentence value proposition;
- primary CTA: `Try a NextGen Question`;
- secondary CTA: `See How BarClimb Works`;
- compact trust line: MCQ / IQS / PT / AI grading / coverage intelligence.

Right:

A live-product visual, not stock photography: an interactive/sample MCQ or IQS fragment with authentic assessment controls and a compact progress/coverage preview.

Mobile stacks the value proposition first and live sample second.

### 9.2 Immediate proof strip

Short proof points only:

- realistic NextGen formats;
- subject/rule/issue coverage;
- constructed-response grading;
- full simulation;
- adaptive next practice.

### 9.3 Try-it section

A real usable sample. Completing it must demonstrate strikeout/highlight/review or written-response interaction where applicable.

### 9.4 Assessment families

Three large product modules:

- MCQ;
- Integrated Question Sets;
- Performance Tasks.

Each explains what the learner does, not generic marketing copy.

### 9.5 Intelligence section

Show a credible example of Progress:

- coverage vs performance;
- rule-level gaps;
- skill evidence;
- recommendation.

### 9.6 Content/library section

Surface real public doctrine and assessment pages. This proves depth and routes users into SEO content.

### 9.7 Pricing

Simple Free vs BarClimb+ comparison. Lead with learning value and ad-free status; do not use fake urgency.

### 9.8 Final CTA

One clear action: `Start Free` or `Try a Question` based on whether the visitor has already attempted a sample in the current session.

### 9.9 Advertising

No AdSense/direct ad above the primary hero CTA. Homepage ad density must be lower than ordinary public content pages because conversion and brand trust dominate that surface.

---

## 10. SEO subject hub composition

Example: `/nextgen/contracts/`.

Required order:

1. breadcrumb;
2. H1 + concise scope description;
3. `Practice Contracts` CTA;
4. current blueprint/knowledge-expectation note;
5. subject coverage map grouped into official scope sections;
6. important doctrine/rule clusters;
7. current BarClimb inventory counts by assessment family;
8. representative practice items;
9. aggregate learner insights only when thresholds are satisfied;
10. related skills/ethics integrations;
11. related subject links;
12. approved ad zones;
13. final practice CTA.

A subject hub is a learning resource, not a tag archive.

---

## 11. SEO doctrine/rule page composition

Required order:

1. breadcrumb;
2. H1;
3. official-scope relationship and knowledge expectation (`Recall expected`, `May use supplied resources`, etc.);
4. concise BarClimb explanation derived from validated sources/content;
5. elements/factors/decision structure where applicable;
6. exceptions/contrasts;
7. common traps and confusion relationships;
8. practice inventory;
9. anonymous learner example/aggregate insight when eligible;
10. related official-scope items;
11. CTA to practice the exact concept.

Do not create one SEO page for every machine-internal node. Only create a page when it has standalone educational value and sufficient validated content.

---

## 12. Public assessment page composition

The the User Journey part of this specification ordering remains controlling. Visually:

- assessment content begins near the top;
- prompt and response controls remain visually connected;
- ad placements never split a prompt from answer choices or response editor;
- answer/explanation is intentionally revealed after submission or explicit reveal;
- teaching analysis is visually separated from the original assessment;
- share controls are easy to find after the user understands the page.

---

## 13. Authenticated Home composition

Desktop uses a 12-column grid but should visually read as three zones, not a dashboard wall.

### Zone A — Recommended Next (dominant)

Approximately two-thirds width on desktop:

- specific reason;
- assessment family;
- estimated time;
- subject/skill target;
- one primary `Start` CTA.

### Zone B — Readiness snapshot

Approximately one-third width:

- Readiness Index if evidence permits;
- Evidence Completeness;
- one link to Progress.

### Zone C — Primary actions

Three large actions:

- Practice;
- Simulate;
- Progress.

Resume state, if present, appears above secondary activity and never competes with Recommended Next.

Mobile order:

1. Resume if active;
2. Recommended Next;
3. Practice/Simulate/Progress;
4. readiness snapshot;
5. recent activity.

Free-user ads may appear only after the primary study actions, never between Recommended Next and its Start CTA.

---

## 14. Practice setup composition

Practice setup is a step composer, not a dense filter form.

1. choose family;
2. choose Recommended / Random / Subject;
3. choose difficulty;
4. reveal only family-specific options;
5. summary + Start.

Specific-topic search is a secondary path.

Focused Practice is visible but subordinate to the three primary NextGen families.

---

## 15. Progress composition

### 15.1 Top layer

Maximum four headline concepts:

- Readiness;
- Evidence completeness/coverage;
- strongest current area;
- highest-value next gap.

### 15.2 Subject layer

Subjects appear as a sortable/list-style competence map rather than decorative cards. Each row shows:

- coverage;
- performance;
- confidence indicator;
- retention indicator where meaningful;
- trend;
- drill-down action.

### 15.3 Subject detail

Group by official NCBE scope structure. Show:

- section/topic hierarchy;
- `Not assessed`, `Limited evidence`, `Developing`, `Proficient`, `Strong`, `At risk`;
- starred/recall indicator where applicable;
- format diversity and fact diversity only in detailed view;
- exact practice CTA for weak/uncovered nodes.

Never imply a rule has been covered merely because the parent subject has many attempts.

---

## 16. Simulation composition

Pre-start:

- exam/session identity;
- duration;
- rules/allowed tools;
- technical readiness;
- Begin.

In-session:

- quiet assessment chrome;
- timer;
- navigator;
- flag/review;
- supported exam tools;
- no marketing navigation;
- no paid upsell;
- no ad during timed section.

Post-session:

- completion confirmation;
- scored/unscored processing state;
- results when available;
- next recommended practice after results.

---

## 17. Pricing composition

Two primary plan columns only at launch:

- Free;
- BarClimb+.

BarClimb+ is visually emphasized but not manipulated with fake countdowns or false “best deal” claims.

Show:

- practice limits;
- IQS/PT/simulation access;
- analytics depth;
- AI feedback;
- ad-free status;
- billing cadence.

Direct sponsor products live under `/advertise/`, not on learner pricing.

---

## 18. Sponsor/Advertise composition

Public `/advertise/` must feel like a professional media product rather than an admin form.

Required sections:

- audience/use case;
- inventory products;
- where ads can appear;
- privacy boundary/no learner-level targeting;
- sample creative placements;
- campaign workflow;
- CTA: `Create a Campaign` / `Contact BarClimb`.

Sponsor dashboard follows the same visual system but is separated from learner navigation.

---

# PART III — VISUAL ACCEPTANCE

## 19. Required visual QA states

Every major page must be reviewed in:

- Light;
- Dark;
- 320px;
- 390px;
- 768px;
- 1024px;
- 1440px;
- realistic long content;
- empty state;
- loading state;
- error state;
- free/ad state where applicable;
- paid/no-ad state where applicable.

## 20. Visual rejection criteria

A page fails if it:

- looks like default Django/Bootstrap/admin styling;
- uses generic dashboard card grids without hierarchy;
- makes the main CTA visually ambiguous;
- squeezes desktop split panes into unusable mobile columns;
- exposes raw schema/technical labels;
- uses ads as primary visual landmarks;
- displays long legal text at poor line lengths;
- makes progress look gamified rather than credible;
- visually suggests BarClimb is official NCBE material;
- feels materially different between features because components were independently styled.

## 21. Build gate

Before broad feature build proceeds beyond the design-system milestone, staging must contain approved responsive reference implementations of:

1. public homepage;
2. public subject hub;
3. authenticated Home;
4. standalone MCQ;
5. integrated IQS;
6. PT workspace;
7. Progress subject map;
8. result/grade page.

Codex must reuse the approved system and compositions. It may not redesign them feature by feature.

# PART IV — COMMUNITY AND NATIVE COMPOSITION

## 22. Public response page as a network object

The response itself remains visually dominant. Community chrome must not make the page resemble a noisy social feed.

Required order:

1. assessment/context identity;
2. response author username + contribution context;
3. learner response and BarClimb evaluation;
4. educational comparison/insight;
5. qualified views and educational-signal row;
6. `Try this assessment` / comparison CTA;
7. response collections such as Helpful / Sharp Analysis / New Angle where enough quality inventory exists;
8. threaded discussion;
9. related doctrine/practice.

Follower counts are secondary metadata, never hero metrics.

## 23. Username/profile composition

Public profile header includes:

- username
- avatar/mark
- optional short bio/exam window
- contribution level
- Follow control

Below:

- contribution summary (qualified views, Helpful, Sharp Analysis, Clear Explanation, New Angle)
- selected achievements
- strongest public contribution topics
- published responses
- public discussion contributions

Private readiness, private Progress, study hours, private scores, and email are never shown.

## 24. Educational signal visual language

Signals are labeled textual controls with restrained icons, not heart/like clones.

Canonical visible labels:

- Helpful
- Sharp Analysis
- Clear Explanation
- New Angle
- Same Trap where supported

The design must remain understandable without color. Counts are secondary to labels.

## 25. Discussion composition

Comments use readable editorial typography and clear username/time/edited metadata.

- bounded indentation depth;
- replies collapse sensibly on phone;
- Report/Block/Mute are discoverable but visually secondary;
- legal disagreement is not styled as conflict/hostility;
- moderator/removed states are explicit;
- composer never competes with the main assessment CTA.

## 26. Community Pulse composition

Community Pulse is a compact finite module, never a full-screen infinite feed.

Each card must identify:

- why it is relevant (subject/rule/assessment/Circle context);
- the contribution type;
- username;
- one useful engagement signal;
- one learning action.

Avoid vanity-first cards whose only content is popularity.

## 27. Achievement and Momentum composition

Achievements use the BarClimb ascent/momentum language without cartoon trophy overload.

- compact celebratory state;
- meaningful title + earned reason;
- private/public display control;
- no confetti that blocks work;
- reduced-motion alternative;
- no giant daily streak flame as a permanent global visual.

## 28. Native mobile visual system

Web and native use the same semantic design tokens and brand character, but native follows platform ergonomics.

Native requirements:

- bottom tab navigation for primary destinations;
- native-safe areas;
- platform-appropriate sheets/navigation transitions;
- minimum touch targets;
- dynamic text sizing without clipping;
- assessment focus mode can hide global chrome;
- resources/editors prioritize usable vertical space;
- share, notification, purchase, and system dialogs use native platform behavior;
- no visual imitation of a desktop browser inside the app.

## 29. Native App Store/Play screenshots

Store screenshots must feature real product value:

- NextGen MCQ interaction tools;
- IQS/PT workspace;
- Progress/coverage intelligence;
- public/community response comparison;
- creator/community usefulness;
- simulation.

Decorative brand-only screens may supplement but may not replace real-product screenshots.

---

# PART III - COMMUNITY, NETWORK, AND GROWTH

**Status:** Authoritative v1 companion contract  
**Date:** August 12, 2026  
**Scope:** Community identity, public responses, discussion, reputation, discovery, gamification, sharing, network effects, moderation, circles, notifications, and growth instrumentation.

## 1. Product thesis

BarClimb is not a generic social network and may never optimize for passive scrolling. It is a **learning network** in which high-value study activity can become durable, searchable, discussable educational content.

Canonical network loop:

```text
Practice
→ useful response/result
→ optional publication
→ views + discussion + comparison + reputation
→ another learner attempts the assessment
→ new response/result
→ stronger assessment, doctrine, and community data
→ better discovery + recommendations + search value
→ more learners
↺
```

The network must make learning more useful. Any social mechanic that increases time-on-site while reducing useful learning is a product defect.

## 2. Identity: usernames, not real names

Public identity is username-first.

- Every account receives a unique, case-insensitive `username` chosen during or immediately after signup.
- Real legal names are not required for ordinary learner accounts and are never displayed publicly by default.
- Public routes use `/u/{username}/`.
- Username changes are rate-limited and maintain redirects/tombstones where needed to prevent impersonation or broken public links.
- Reserved, deceptive, impersonating, hateful, sexually explicit, or trademark-abusive usernames are prohibited.
- Email, billing identity, device identifiers, readiness, private grades, and private learner-state data are never exposed on a public profile.
- Users may use an optional avatar or generated initials/icon; no profile photo is required.

Public profile may show only user-controlled or derived public contribution data:

- username
- optional short bio
- optional exam year/window, never precise personal location
- contribution level/reputation label
- published responses
- public comments/replies
- selected achievements
- topic contribution strengths derived from public contributions, not private mastery
- response views
- helpful-community signals received
- followers/following only if enabled; counts are visually secondary

## 3. The public response is a first-class network node

A learner response may become a `PublishedResponse` only with explicit publication consent.

A public response page can include:

- assessment prompt/resources subject to publication eligibility
- username or explicit anonymous publication choice
- learner response
- BarClimb score/rubric where consented
- BarClimb evidence highlights
- improved approach/model response where appropriate
- doctrine/rule/skill mapping
- reliability context
- response views
- educational reactions
- threaded discussion
- comparison with other public responses
- CTA to attempt the same assessment or a materially similar one

Publication consent must be revocable. Withdrawal removes the response from public display and public profile while preserving legally/operationally necessary private records according to the privacy contract.

## 4. Discussion layer

Discussion attaches to educational objects rather than existing as a context-free global chat.

Thread-capable nodes:

- public assessment
- published response
- public doctrine/rule page
- aggregate insight
- Circle-shared assessment or response

Launch discussion features:

- top-level comments
- threaded replies with bounded nesting depth in the UI
- edit window with visible edited state
- delete own comment
- report
- block user
- mute thread
- follow thread
- permalink to comment/reply
- moderator removal/lock

No direct messages, random chat, anonymous live chat, or public chat rooms at launch. These increase moderation and safety risk without being necessary to the learning network.

## 5. Educational signals — no generic likes

BarClimb does not use a generic Like button as the primary response signal.

Canonical response/comment signals:

- **Helpful** — this improved my understanding.
- **Sharp Analysis** — strong issue/fact/rule reasoning.
- **Clear Explanation** — unusually understandable explanation.
- **New Angle** — useful materially different approach.

Canonical assessment-level learning signal:

- **Same Trap** — the learner reports falling for the same misconception/distractor. This is an aggregate learning signal, not reputation currency.

Rules:

- One user may apply each allowed signal once per target.
- Self-signals are prohibited.
- Signals from blocked, banned, bot-detected, or suspicious accounts may be excluded from public totals and reputation calculations.
- Signal counts may be hidden/suppressed until minimum activity thresholds to reduce herd effects.
- Downvotes are not used for public popularity. Incorrect/ambiguous/outdated content uses the existing structured challenge/report system.

## 6. Views and creator feedback

Creators should see legitimate evidence that their work is useful.

Track:

- total qualified views
- unique qualified viewers where privacy-safe
- views over time
- signal counts
- comment/reply counts
- saves/bookmarks
- assessment starts attributable to the public response where attribution is technically supportable

Do not count:

- creator self-views
- obvious bots/crawlers
- repeated refresh spam inside a bounded deduplication window

Public UI may show rounded counts after minimum thresholds. Creator analytics may show more detail. Never claim causal language such as “you taught 312 learners” unless measurement supports it; prefer “312 learners engaged with this response” or “47 practice starts followed this page.”

## 7. Reputation is contribution reputation, not learner readiness

Public reputation must never reveal or proxy private readiness.

`ContributionReputation` is calculated from public contribution quality and trust signals, including:

- unique qualified educational signals
- response reliability/quality moderation status
- sustained useful contributions across time
- diversity of useful contributions
- successful challenge/correction behavior where appropriate
- anti-gaming trust factor

Do not reward raw posting volume linearly.

Reputation presentation uses understandable levels rather than addictive casino-like point explosions. Example labels:

- New Contributor
- Contributor
- Trusted Contributor
- Distinguished Contributor

Exact thresholds are configurable and versioned. Reputation can decrease or be withheld for moderation violations or detected manipulation.

## 8. Comparison experiences

Assessment pages may show community response collections:

- Most Helpful
- Sharp Analysis
- Clear Explanation
- New Angle
- High-scoring response, only if public scoring consent allows
- Recent quality responses

Do not create a single global “best student” ranking.

Comparison should answer: **How did other learners reason through this?** not **Who is smartest?**

## 9. Discovery: finite community pulse, not doomscroll

Community discovery is contextual and bounded.

Allowed surfaces:

- Home `Community Pulse` with a small finite set of high-value items
- subject/doctrine community highlights
- assessment discussion and response tabs
- public response discovery
- followed threads/contributors
- Circle activity
- notifications inbox

Every discovery card must have a learning path: read, compare, attempt, review, discuss, or save.

No infinite-scroll generic social feed at launch. Pagination/load-more is acceptable on explicit community browse pages.

Ranking signals prioritize:

1. educational relevance to current context
2. content quality/reliability
3. user novelty
4. community usefulness
5. recency
6. diversity of contributors
7. anti-spam trust

Popularity alone may not dominate ranking.

## 10. Follows, saves, and subscriptions

Users may:

- follow another username
- follow a discussion thread
- follow a doctrine/rule/subject
- save/bookmark public assessments/responses

Following another learner affects community discovery and notifications only. It does not affect readiness or pedagogical recommendations except where the user explicitly starts a shared assessment.

## 11. Study Circles

Launch architecture includes invite-only `StudyCircle` groups because small-group network effects create retention without requiring public exposure.

V1 Circle features:

- create Circle
- invite via link/code
- username-based membership
- share assessment/public response into Circle
- Circle discussion thread
- lightweight weekly activity summary
- optional group challenge using existing assessments
- leave/remove member
- owner/moderator roles
- report/block safety behavior

No private DMs and no unmoderated live chat at launch.

Circle leaderboards, if used, are bounded and learning-oriented (e.g. “most helpful contribution this week”), never raw time-spent competitions.

## 12. Healthy gamification

Gamification must reinforce learning or contribution.

### Momentum

Use forgiving weekly momentum rather than punitive daily streak loss.

Examples:

- meaningful practice on 3 days this week
- 4 consecutive active weeks
- completed 3 of 4 planned sessions

No streak protection purchases, shame messages, or catastrophic reset animations.

### Achievements

Achievements must encode meaningful evidence. Initial families:

- Issue Spotter — proficiency across diverse issue patterns
- Rule Keeper — delayed retention across multiple rules
- Transfer — success across materially different fact archetypes
- Counsel — demonstrated counseling skill across contexts
- Researcher — successful legal research task performance
- Closer — completed a full simulation
- Contributor — useful published contributions
- Explainer — repeated Clear Explanation signals
- Sharp Analyst — repeated Sharp Analysis signals
- Community Builder — useful Circle/community participation without moderation issues

Achievements can be private by default with per-achievement public-display control.

## 13. Notifications and re-engagement

Notification channels:

- in-app inbox
- push (iOS/Android)
- email where appropriate

Preference categories:

- grading/results
- learning/retention reminders
- community replies/signals
- follows/Circle activity
- product announcements
- marketing/promotional

High-value examples:

- “Someone replied to your Contracts analysis.”
- “Your response reached 100 qualified views.”
- “A rule you previously struggled with is ready for retention practice.”
- “Your PT grade is ready.”
- “You are one assessment away from complete Evidence coverage.”

Marketing/promotional push must be separately controllable and comply with current platform policy. Notification delivery is rate-limited and bundled to prevent harassment or compulsion.

## 14. Viral sharing

Every shareable node has a stable canonical URL and privacy-safe social card.

Shareable objects:

- public assessment
- public response
- discussion
- aggregate insight
- achievement
- progress milestone explicitly chosen by learner
- Circle invitation

Cards should create curiosity around the learning object, not merely advertise BarClimb.

Examples of copy patterns:

- “Only 34% of BarClimb attempts got this Evidence issue right. Can you?”
- “My response scored 88 on this NextGen IQS. Compare your approach.”
- “Three strong ways to analyze this Contracts problem.”

Publicly displayed percentages require minimum sample sizes and appropriate caveats.

## 15. Referral system

Referrals are secondary to organic sharing.

If incentives are enabled, they must be bounded study benefits such as a limited additional grading credit, never cash-like spam incentives, fake scarcity, review manipulation, or chart manipulation.

Referral attribution model tracks invite/share source without exposing social graph data to advertisers.

## 16. Community safety and moderation

Community cannot launch without UGC safety controls required by app-store policies and BarClimb standards.

Required:

- Terms/Community Standards acceptance
- profanity/toxicity/spam screening
- link safety validation
- user report flow
- content report flow
- block user
- mute thread
- moderator queue
- moderator action audit trail
- warning/restriction/suspension/ban states
- appeal/review mechanism
- rate limits for comments/replies/follows/signals/invites
- anti-brigading and duplicate-account heuristics
- support/contact surface

Moderation must distinguish disagreement about law from abuse. A legally incorrect answer is corrected/challenged; it is not automatically “abusive.”

## 17. Community privacy

- Public profile and public contribution are opt-in surfaces governed by explicit settings.
- Private grades/readiness/history never become public by default.
- Published learner response consent is separate from ordinary account Terms.
- Deleted/withdrawn content disappears from public discovery promptly while moderation/legal retention records may persist privately where justified.
- Block relationships are private.
- Advertisers receive no user-level community graph, readiness, discussion, or targeting data.

## 18. Network graph model

Core node types:

- User/PublicProfile
- Assessment
- AssessmentVersion
- DoctrineNode
- SkillNode
- EthicsNode
- PublishedResponse
- DiscussionThread
- Comment
- Reaction
- Bookmark
- Follow
- StudyCircle
- Achievement
- AggregateInsight

Core edges:

- ATTEMPTED
- AUTHORED
- PUBLISHED
- DISCUSSED
- REPLIED_TO
- REACTED_TO
- SAVED
- FOLLOWS
- MEMBER_OF
- MAPS_TO_DOCTRINE
- MAPS_TO_SKILL
- SHARED
- VIEWED_QUALIFIED

Graph semantics may be stored relationally in PostgreSQL at launch. A graph database is not required.

## 19. Canonical community models

Add Django `community/` app.

Minimum models:

### community.PublicProfile
- user OneToOne
- username canonical/unique case-insensitive
- bio nullable
- avatar object nullable
- public_exam_window nullable
- visibility/state
- contribution_level
- created_at/updated_at

### community.PublishedContribution
Generic/stable identity for public responses and future contribution types; links to concrete publication object and author profile.

### community.DiscussionThread
- target content type/id or typed FK strategy documented
- state OPEN/LOCKED/ARCHIVED
- created_at

### community.Comment
- thread FK
- author FK
- parent nullable
- body
- moderation_state
- edited_at nullable
- created_at

### community.Reaction
- actor FK
- target type/id
- signal enum HELPFUL/SHARP_ANALYSIS/CLEAR_EXPLANATION/NEW_ANGLE/SAME_TRAP where allowed
- created_at
- unique actor/signal/target

### community.ContentView
- target
- viewer user nullable
- anonymous/session hash nullable
- qualified bool
- source/referrer category
- occurred_at

### community.Follow
- follower FK
- target user/thread/doctrine typed target
- created_at
- uniqueness enforced

### community.Bookmark
- user FK
- target
- created_at

### community.UserBlock
- blocker FK
- blocked FK
- created_at
- unique pair

### community.ContentReport
- reporter FK
- target
- reason
- details
- state
- created_at

### community.ModerationCase / ModerationAction
Auditable moderation workflow.

### community.ReputationSnapshot
- profile FK
- model_version
- score internal
- public_level
- component_data JSON
- calculated_at

### community.AchievementDefinition / UserAchievement
Versioned achievement rules and earned state.

### community.StudyCircle / StudyCircleMembership / CircleShare
Invite-only small-group network.

## 20. Community API surface

Under `/api/v1/community/`:

- GET/PATCH `/profile/`
- GET `/profiles/{username}/`
- POST `/profiles/{username}/follow/`
- DELETE `/profiles/{username}/follow/`
- POST `/profiles/{username}/block/`
- GET `/threads/{id}/`
- POST `/threads/{id}/comments/`
- PATCH/DELETE `/comments/{id}/`
- POST `/targets/{type}/{id}/reactions/`
- DELETE matching reaction endpoint
- POST/DELETE bookmarks
- POST reports
- GET `/pulse/`
- GET `/notifications/`
- circles CRUD/invite/share endpoints
- creator analytics endpoint scoped to own profile/contributions

All write endpoints are authenticated, authorized, rate-limited, CSRF-safe for web, and use platform-appropriate authenticated API behavior on native.

## 21. Ranking, anti-gaming, and abuse resistance

Community ranking and reputation must have:

- minimum account-age/trust weighting where appropriate
- unique-user weighting
- velocity anomaly detection
- self-interaction exclusion
- reciprocal-ring detection heuristics
- duplicate-account/device/IP risk signals used conservatively
- moderation overrides
- model versioning

Never display secret anti-abuse thresholds.

## 22. Community analytics and network health

Track at minimum:

- public response publication rate
- qualified response views
- view → assessment-start rate
- assessment-start → signup conversion from public responses
- comments per active public response
- educational signals per public response
- percent of contributors receiving at least one meaningful interaction
- creator return rate after first community interaction
- follows and thread follows
- Circle creation/activation/retention
- share → visit → attempt → signup funnel
- moderation reports per 1,000 contributions
- blocked-user rate
- reputation concentration / contributor diversity
- community-assisted paid conversion

Do not optimize solely for session duration or comment volume.

## 23. Monetization rules for community surfaces

- Paid users remain ad-free.
- Public community pages may contain restrained ads only where they do not interrupt the response or discussion reading flow.
- Ads may not be targeted using private learner performance, readiness, discussion sentiment, follows, blocks, or public username identity.
- Sponsor campaigns cannot buy community reputation, pinned praise, reaction counts, or disguised comments.
- Sponsored educational content must be clearly labeled and isolated from organic reputation systems.

## 24. Community E2E golden flows

Required before launch:

1. username creation → publish response → public profile → qualified external view → creator analytics increment.
2. SEO visitor → public response → discussion → attempt same assessment → signup claim → follow thread.
3. authenticated user → Helpful/Sharp Analysis signal → deduplication → creator notification.
4. abusive comment → report → block → moderator action → hidden content → audit trail.
5. response withdrawal → public URL updates appropriately → profile removal → no learner-state corruption.
6. username change → old public links redirect safely.
7. Circle create → invite → join → share assessment → discuss → leave.
8. share card → deep link to installed mobile app, fallback to web when not installed.
9. bot/repeated refresh → qualified-view metric does not inflate materially.
10. banned account cannot continue posting/signaling through normal authenticated endpoints.

## 25. Definition of done

Community is not complete until:

- web, iOS, and Android render the governed community experience;
- moderation/report/block flows are live in staging;
- public-profile privacy is correct;
- community writes are rate-limited;
- deep links work;
- creator analytics are bot/self-view resistant;
- accessibility passes;
- no community metric changes learner readiness;
- app-store UGC requirements are satisfied;
- the community loop demonstrably routes back into learning rather than passive scrolling.

## 26. Legal freshness propagation through the network

Community content never outranks canonical law/assessment state.

- Published responses inherit the legal-freshness context of the source AssessmentVersion.
- If an assessment becomes `REVALIDATION_REQUIRED`, `STALE`, `SUPERSEDED`, or `RETIRED`, public responses and discussions display an appropriate status notice and may be removed from recommendation/ranking/indexing until revalidated.
- Community comments cannot amend the canonical answer. A credible legal-correctness concern routes into Challenge/revalidation.
- Aggregate insights must pin the assessment/legal-source versions used to produce them.
- Old discussions may remain historically viewable where useful, but BarClimb must not present superseded law as current guidance.

This freshness propagation is essential to keeping the network useful for years rather than accumulating an ungoverned archive of stale bar-prep advice.

## 27. Community SEO and spam-indexing rules

Community growth must not create low-quality search inventory.

- Individual comment permalinks are not independently indexable; canonical points to the substantive parent page.
- Public username profiles begin `noindex` until they meet configurable substantive-contribution/quality thresholds.
- Empty or near-empty profiles are `noindex`.
- Published response pages become indexable only through the existing publication/content-quality/privacy gates.
- User-generated links are sanitized and use appropriate rel attributes/policies.
- Removed/spam/banned content is excluded from sitemaps immediately.
- Search ranking pages never rely on comments alone for substantive publisher content.

## 28. Audience and age posture

BarClimb v1 is an adult professional-education product intended for users **18 years or older**. Signup/Terms must communicate the minimum age without collecting date of birth unless later legally required.

The service is not directed to children. If future product expansion changes that posture, privacy, moderation, store-rating, and parental-consent requirements require a new product/legal review before launch.

## 29. Automated moderation service boundary

Automated moderation may assist but never silently become the sole adjudicator for serious account penalties.

Add a central `CommunitySafetyService` with versioned policy/rule/model configuration for:

- spam/link abuse
- harassment/threats
- hate/sexual/graphic content
- credential/personal-information exposure
- prompt-injection/malicious generated content where applicable

Low-risk auto-actions may rate-limit or hold content for review. Serious suspension/ban decisions remain auditable and appealable, with human review available.

## 30. Share-card generation contract

Share cards are deterministic branded assets generated from approved templates and public data. AI image generation is not required for ordinary share cards.

Templates must support assessment, response, insight, achievement, and Circle-invite objects; automatically omit private fields; and generate Open Graph/social metadata consistently with canonical URLs.

---

# CONSOLIDATED EXPERIENCE RULE

BarClimb must feel like one product, not a study tool plus a bolted-on social network. Every community surface must lead back toward learning, every public identity is username-first, private learner intelligence stays private, public popularity never modifies readiness, and engagement mechanics must reward meaningful learning/contribution rather than endless consumption.

# PART IV — FINAL THREE-SCENARIO SURFACE AND VIEW CONTRACT

This part converts the Visitor, signed-in Free, and Plus journeys into explicit page/view composition requirements.

## 60. Global navigation and identity continuity

Public header: BarClimb brand, Learn/Practice discovery entry, Search, Pricing where appropriate, Sign in/Create account. It remains compact and content-first.

Authenticated shell: BarClimb | Practice | Simulate | Progress | Search | Account, with Home reached by brand/home affordance and mobile primary navigation optimized for Practice/Simulate/Progress. Notifications and contextual community entry must not crowd primary study navigation.

Authentication should not visually replace the public knowledge graph with a disconnected application. Canonical public pages remain first-class destinations after signup.

## 61. Public SEO page composition by search intent

Each canonical learning page declares one primary intent: LEARN, PRACTICE, COMPARE, EXAM_SCOPE, SKILL, or ETHICS. The first viewport varies composition while the canonical underlying subject matter remains consistent.

Common order:
1. answer the search intent immediately;
2. restrained scope/freshness/reliability/provenance trust signals;
3. high-value learning object or Instant Practice;
4. explanation/distinction;
5. aggregate/community insight when sufficiently supported;
6. graph-aware Continue Learning;
7. earned signup/persistence action;
8. deeper related inventory/community.

Never force signup before providing the answer/search value promised by the page.

## 62. Authenticated private overlay composition

When signed in, canonical public pages may add a clearly private **Your BarClimb** region after authentication:
- current mapped mastery/coverage/evidence state;
- last relevant attempt;
- retention/review status;
- recommended practice;
- Add to Review / Practice this / Repair this actions;
- Plus-only deeper patterns/Ask where eligible.

This region must render from a private overlay endpoint and must not alter public canonical metadata/indexing.

## 63. Home composition

The Home experience is shared by Free and Plus:
1. Recommended Next — visually dominant;
2. qualifying Resume — strong but subordinate according to documented precedence;
3. Readiness + Evidence Completeness snapshot;
4. Practice / Simulate / Progress entry actions;
5. active StudySession/RepairPlan/Review summary;
6. Path-to-Exam/This-Week summary where useful;
7. restrained recent activity and Community Pulse.

Plus removes ads/upsells and unlocks deeper eligible actions. It does not receive a separate premium dashboard.

## 64. Study Session UX

Quick, Standard, and Deep are one-tap presets around planner-generated coherent work. Custom/advanced goals remain progressive disclosure.

Session header shows purpose and approximate duration, not a rigid list learners are punished for deviating from. Users may skip/dismiss eligible steps. The server planner can adapt subsequent steps but must explain material changes on request.

Session Complete should favor closure:
- meaningful work completed;
- actual learning impact;
- unresolved areas;
- next useful move;
- clear stop/Done action.

No endless “keep going” loop by default.

## 65. Review Queue and Suggested Review UX

Two visually distinct groups:
- **My Review Queue** — intentional durable saves;
- **Suggested Review** — system recommendations awaiting acceptance.

Suggested items state why: retention due, repeated error, transfer uncertainty, unresolved writing issue, etc. Actions: Practice now / Add / Dismiss.

The durable queue supports cleanup, completion/archive, and filters. It must not become a silent backlog of every wrong answer.

## 66. Weakness Repair UX

A Repair sequence begins with the current hypothesis and uses bounded diagnostic/adaptive steps. After enough evidence, summarize the likely bottleneck and what changed. Use cautious language when evidence is limited.

Repair may be launched from Progress, Simulation results, History patterns, Search/public-page private overlays, or Recommended Next. It uses standard assessment components rather than inventing a second exercise engine.

## 67. Progress and longitudinal storytelling

Progress top level answers:
- How am I doing?
- How much of the applicable scope have I actually tested?
- How stable is this picture?
- What is strongest/weakest/unassessed?
- What should I do next?

Use the official NextGen hierarchy and visibly distinguish UNASSESSED/LIMITED EVIDENCE from poor performance.

Longitudinal views may show prior-period snapshots and largest gains/unresolved areas, but avoid decorative charting or pseudo-precision unsupported by evidence.

## 68. Search as universal study surface

Authenticated Search groups results by intent and learner relevance: Learn, Your Status, Practice, History, Review, Community, and contextual Ask. Public Search omits private groups.

Search supports official names, aliases, common abbreviations, Model Rule references, skills, doctrines, rules/issues, and assessment types. Search never invents new curriculum identity.

## 69. History and Plus pattern intelligence

History always preserves immutable attempt detail. Plus may add pattern summaries only when evidence thresholds are met, each with drillable supporting attempts and a Practice/Repair action. Pattern analysis is an explanatory layer over history, never a replacement for the record.

## 70. Plus whole-site experience

While authenticated with effective Plus capability:
- no AdSense, AdMob, direct sponsor, house ad, or routine upgrade CTA anywhere;
- public/SEO/community pages also suppress monetization chrome;
- deep analytics and Ask appear contextually rather than in a separate Premium area;
- community rank/reputation remains identical to Free rules;
- billing UI is quiet and source-aware;
- fair-use limits remain invisible during ordinary legitimate use.

## 71. Community-to-learning bridge

Community objects should normally expose a sensible learning action when one exists: Practice this rule, Try this assessment, Compare your response, Review this distinction, etc. Community engagement itself does not count as mastery.

Community Pulse is finite and context-aware; no infinite generic feed is required for launch.

## 72. View-state requirements

Every major surface specifies:
- loading/skeleton
- useful empty state
- error/retry
- offline/degraded where relevant
- Free restriction/transparent entitlement boundary
- Plus state
- accessibility/high-contrast
- responsive desktop/tablet/mobile/native form.

No major state may degrade to a raw API error, blank panel, or generic “Something went wrong” when a recoverable next action is known.

## 73. Visual hierarchy across all scenarios

The brand remains precision + ascent + momentum. Visual reward comes from clarity, progress, successful learning transitions, and meaningful contribution—not casino-style saturation.

Priority hierarchy:
1. current learning objective/action;
2. assessment/resource content;
3. feedback/progress;
4. useful community context;
5. monetization for eligible Free/anonymous surfaces.

Ads or community chrome may never visually outrank an active learner action.

## 74. Scenario acceptance heuristics

A reviewer must be able to answer Yes:
- Visitor: “Did I get the answer I searched for before being asked to commit?”
- Visitor: “Did BarClimb reveal an interactive/network advantage over a static article?”
- Free: “Is the best next study action obvious, while alternate choices remain available?”
- Free: “Can I understand weak vs unassessed and see why a recommendation exists?”
- Plus: “Has selling disappeared while capability deepened?”
- Plus: “Can I move among app study, Search, public pages, community, and native without losing context?”
- All: “Does every social/content interaction have a safe privacy/identity boundary?”
