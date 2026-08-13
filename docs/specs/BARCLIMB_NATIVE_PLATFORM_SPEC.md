# BarClimb Native Platform Specification

**Status:** Authoritative v1 companion specification.

This document consolidates and supersedes the former Mobile Platform Contract. It governs iOS and Android as first-class launch clients, shared TypeScript contracts, React Native/Expo architecture, native assessment parity, offline/recovery, deep links, push, privacy, community parity, subscription verification, store release pipelines, and native launch gates.

## Native advertising correction

Web external-fill advertising uses Google AdSense when approved and enabled. Native iOS/Android external-fill advertising uses Google AdMob when approved and enabled. Direct sponsorship and house campaigns may serve across web and native through BarClimb's own ad-decision service. A pending AdSense or AdMob approval must not block the learner product from launching; house ads or no external-fill ad are valid fallbacks. Paid users remain ad-free.

The server-side ad decision must therefore distinguish at least `WEB_ADSENSE`, `NATIVE_ADMOB`, `DIRECT`, `HOUSE`, and `NONE`, subject to consent/platform policy and the advertising invariant in the Build Constitution.

---

**Status:** Authoritative v1 companion contract  
**Date:** August 12, 2026  
**Scope:** iOS and Android launch architecture, native UX, shared packages, authentication, deep links, offline behavior, notifications, billing, release, store policy, QA, and launch parity.

## 1. Launch requirement

BarClimb launches as three first-class clients:

1. Web
2. iOS
3. Android

Native applications are a v1 launch requirement, not a post-launch roadmap item.

A mobile app may not be a thin WebView wrapper. It must provide a high-quality native study/community experience with platform-native navigation, text input, sharing, notifications, deep linking, offline resilience, and purchases.

## 2. Technology decision

Use **React Native + TypeScript with Expo tooling** unless a documented blocking requirement discovered during Milestone 1 forces a change.

Repository structure should support a monorepo/shared-package model:

```text
apps/
  web/
  mobile/
    ios/android via React Native + Expo
packages/
  api-client/
  domain-types/
  assessment-schema/
  design-tokens/
  analytics-events/
  feature-flags/
  validation/
```

Do not force shared visual components between DOM React and React Native. Share contracts, types, schema, tokens, API clients, and pure business logic; implement platform-appropriate presentation separately.

## 3. Native information architecture

Primary mobile tabs:

- Home
- Practice
- Simulate
- Progress

Secondary surfaces through profile/menu/navigation:

- Search
- Community
- History
- Saved
- Notifications
- Account
- Billing
- Privacy
- Support

Assessment mode may temporarily hide normal app chrome to preserve focus.

## 4. Native assessment parity

All assessment families required on web must be usable on iOS and Android at launch:

- standalone MCQ
- IQS
- Standard PT
- LRPT
- focused ethics practice

Native clients consume the same versioned Assessment Presentation Schema and Capability Manifest as web.

Native equivalents are required for:

- answer selection
- strike-through/elimination
- highlighting
- review flags
- question navigation
- resource tabs/switching
- constructed-response editing
- notepad
- autosave
- results/GradeRenderer
- Ask BarClimb
- challenge/regrade

Phone PT/LRPT must remain fully functional even if desktop/tablet is the optimal form factor.

## 5. Offline and resilience

V1 offline support is bounded but real.

Required:

- local encrypted/OS-protected persistence for in-progress attempt state where practical
- pending write queue for safe idempotent autosave operations
- clear Offline/Syncing/Synced/Conflict states
- recovery after process kill/relaunch
- downloaded practice packs for selected standalone MCQ sets if implemented in launch scope
- no offline simulation start unless the entire simulation and timer/security contract can be satisfied; otherwise require connection to begin

Server remains authoritative for scoring eligibility, simulation timing, entitlement, and final submission.

## 6. Authentication

Native authentication uses the same user identity as web.

Required:

- email/password or supported account flow determined in auth spec
- secure token/session strategy documented for native; do not reuse insecure browser assumptions
- credentials/tokens stored only in platform secure storage
- logout revokes/clears local sensitive state appropriately
- optional biometric re-entry may protect an already authenticated local session; biometrics are not a separate BarClimb identity
- cross-device attempt/history sync

If third-party sign-in is introduced, comply with current platform parity requirements and document provider behavior.

## 7. Deep links and universal/app links

Every canonical public web object that has a meaningful native destination must deep-link:

- assessment
- public response
- discussion/comment
- doctrine/rule page where native equivalent exists
- notification target
- Circle invitation
- billing/account destination where allowed

Use HTTPS universal links/app links as canonical external URLs. If the app is not installed, the same URL must remain useful on the web.

## 8. Native sharing

Use native share sheets for public/shareable objects.

Share payload includes:

- canonical HTTPS URL
- concise title/text
- generated social preview handled by web metadata where applicable

Never share private learner response text, readiness, email, or account data without an explicit user action selecting that content.

## 9. Push notifications

Implement APNs through the chosen Expo/native notification path for iOS and FCM-compatible delivery for Android.

Backend models device registrations and notification preferences centrally.

Required notification families:

- grade/result ready
- retention/recommendation reminder
- reply/reaction
- followed thread/contributor activity where enabled
- Circle activity
- account/security
- billing/service
- product/marketing separately consented

Notification taps deep-link to the exact object.

Rate-limit/bundle community notifications to avoid spam.

## 10. Store subscriptions and entitlements

Django owns the canonical entitlement state across platforms.

Supported purchase sources:

- Stripe web
- Apple In-App Purchase / StoreKit
- Google Play Billing

A user who purchases through one supported platform receives the corresponding account entitlement on other clients subject to current store rules.

Required billing domain fields/models:

- purchase_source enum STRIPE/APPLE/GOOGLE
- external_product_id
- external_transaction/subscription identifiers
- original transaction/purchase token identifiers as applicable
- entitlement period
- renewal state
- grace/billing-retry state
- revocation/refund state
- verified_at

Required flows:

### iOS
- load products
- purchase
- restore purchases
- verify signed transaction/server state using current StoreKit/App Store server mechanisms
- server notification handling
- renewal/cancel/grace/refund/revoke
- sandbox + TestFlight verification

### Android
- Play Billing Library integration using the current supported version at implementation
- purchase acknowledgement
- restore/query existing entitlement
- backend purchase verification
- Real-time Developer Notification / lifecycle processing where applicable
- renewal/cancel/grace/account-hold/refund/revoke
- internal/closed testing verification

Client-side success is never the entitlement source of truth.

## 11. Pricing consistency

Plans remain centrally modeled and may have platform-specific price identifiers.

The product may experimentally offer different storefront-localized price points only if consistent with platform rules and clearly communicated. Do not promise identical nominal prices across all currencies/stores.

The UI must explain where subscription management occurs for the user’s purchase source.

## 12. Ads on mobile

Paid users are ad-free across all clients.

Mobile ad support, if enabled at launch, must use a provider implementation specifically approved for native applications and consent requirements. Web AdSense code is never embedded as a pseudo-native ad system.

Initial mobile priority is subscription/community retention; house/direct sponsor placements may be supported through BarClimb-controlled native creative. Any third-party mobile ad SDK requires separate privacy/security review and feature flag.

## 13. Community parity

Native clients launch with the core learning-network experiences:

- username/public profile
- public response reading
- discussion/comments/replies
- educational signals
- follow/save
- notifications
- block/report
- creator view/signal summary
- Circles if enabled in the launch flag set

Moderation/report/block cannot be web-only.

## 14. Native privacy and permissions

Request only permissions necessary for current functionality.

Launch should not request contacts, precise location, microphone, camera, photos, or tracking permission unless a concrete shipped feature requires it.

Device/push identifiers are treated as personal data and minimized.

Account deletion must be available in-app and through the required web path. Privacy settings and publication withdrawal must be accessible on native.

## 15. Accessibility

Native apps target WCAG-equivalent accessible outcomes and platform accessibility best practices:

- screen reader labels/order
- Dynamic Type/font scaling where practical
- sufficient touch targets
- no color-only state
- reduced motion
- high contrast assessment mode
- keyboard/hardware keyboard support on tablets where appropriate
- accessible editor and resource navigation

## 16. Performance

Targets:

- warm navigation feels immediate
- no blocking startup dependency on AI
- cached authenticated shell usable during transient API delay
- long lists virtualized
- assessment content/resource loading incremental where safe
- image/media sizes bounded
- crash-free sessions and app-start metrics instrumented

## 17. Native analytics

Use the same canonical first-party event names as web with platform/client metadata.

Add:

- app_installed/first_open where privacy-compliant
- deep_link_opened
- push_opened
- notification_permission_state
- purchase_started/completed/restored by source
- offline_recovery_used
- sync_conflict
- app_crash/nonfatal reporting via chosen observability stack

Do not create divergent business definitions by platform.

## 18. Store listing and acquisition

Launch deliverables include:

- App Store listing
- Google Play listing
- screenshots for required device classes
- preview/video only if it materially demonstrates product
- privacy disclosures/data safety forms
- content rating
- support URL
- privacy URL
- account deletion URL
- subscription disclosures
- review notes/test account where required

App-store screenshots should show real assessment/community/progress value, not decorative marketing screens only.

## 19. Mobile release pipeline

Establish during Milestone 1:

- bundle identifiers/application IDs
- signing/certificates/keys managed securely
- Expo/EAS or documented equivalent build pipeline
- dev/internal builds
- TestFlight
- Google Play internal/closed testing
- environment-specific API/config
- source maps/symbol upload to observability
- version/build numbering
- staged rollout/rollback strategy

Production web release may not silently imply native release; each client has explicit release status, but public v1 launch requires all three launch gates.

## 20. Mobile security

Threat model includes:

- token theft
- rooted/jailbroken device risk without overclaiming prevention
- reverse engineering/static secrets
- purchase spoofing
- deep-link spoofing
- local response leakage
- malicious rich/generated content
- replayed offline writes

No provider secret or authoritative answer key is shipped in the client bundle.

## 21. Mobile E2E golden flows

Required on both iOS and Android staging/test builds:

1. install → signup/login → onboarding → recommended MCQ → submit → result → Progress.
2. public response deep link → app opens exact response → attempt assessment → signup/claim if needed.
3. IQS with resources → background app → foreground → state intact → submit.
4. long constructed response → process restart/recovery → server reconcile.
5. push grade-ready → tap → exact graded attempt.
6. community reply → push → thread → signal/reply → block/report available.
7. purchase Plus → server entitlement → ads removed → web also recognizes entitlement.
8. restore purchase on fresh install.
9. cancellation/refund state reaches entitlement correctly.
10. Circle invitation link → join exact Circle.
11. offline transition during practice → local state persists → reconnect sync.
12. account deletion flow reachable and completes expected state.

## 22. Native launch gate

BarClimb cannot call v1 launched until:

- iOS App Store production release is approved/available or intentionally phased within a documented launch window;
- Android Play production release is approved/available or intentionally phased within the same documented launch window;
- both pass critical E2E flows;
- store billing and restoration are verified in production/sandbox-equivalent flows as applicable;
- UGC report/block/moderation is functional;
- push deep links work;
- privacy/account deletion requirements are complete;
- crash/observability is live;
- assessment presentation parity is proven.

## 23. Native technical-risk spikes required before feature build

Milestone 1 must prove the riskiest native assumptions with throwaway-or-promotable prototypes before the full feature build:

1. schema-driven MCQ renderer with strike-through/highlighting;
2. IQS resource switching with persistent answer state;
3. long PT/LRPT editor with autosave, copy/paste, formatting, keyboard behavior, background/foreground recovery, and hardware-keyboard sanity on tablet;
4. Universal/App Link to an assessment/public response;
5. staging auth + secure credential/token storage;
6. one sandbox StoreKit product query and one Google Play test-product query as soon as store projects permit.

A failed spike can change the concrete native library/tool choice without changing the product contract. It must be resolved before Milestone 4 rather than discovered at launch.

## 24. Account model decision for v1

V1 authentication is **email + username + password**, with email verification/password reset as configured. Do not add Google/Facebook/Apple social sign-in merely for convenience during v1; doing so creates additional identity/store-policy branches without improving the core launch loop enough to justify them.

A future social-sign-in change requires an auth-contract update and platform-policy review.

## 25. Developer-account prerequisites

At Milestone 1 kickoff, create/verify and document ownership/access for:

- Apple Developer Program / App Store Connect;
- Google Play Console;
- required bundle IDs/package names;
- signing and store roles using least privilege;
- organization-owned recovery/admin access rather than a single developer’s personal credentials where feasible.

Store-account setup is a schedule dependency, not a launch-week task.

---

# CONSOLIDATED NATIVE BUILD RULE

The native apps are not wrappers around the website. They consume the same authoritative backend/domain contracts while owning platform-native interaction, storage, lifecycle, accessibility, billing, and distribution behavior. Web, iOS, and Android all launch as supported clients.

## 26. Cross-scenario native projection and orchestration parity

Native iOS/Android consume the same server projections and domain contracts as web for Home/My BarClimb, Progress, Search, StudySession, Review Queue, RepairPlan, notifications, and entitlement capabilities. Native clients may render platform-native composition but may not independently decide learner priorities, coverage/mastery, publication visibility, or effective Plus status.

Required native routes/screens include:
- Home/Recommended Next/Resume
- Practice setup + AssessmentRenderer
- Simulate
- Progress drilldown
- Search
- History + eligible pattern insight
- Review Queue/Suggested Review
- RepairPlan
- Notifications
- public response/community/profile/Circle deep-link destinations
- Account/Privacy/Billing
- creator analytics

## 27. Cross-device continuation beyond attempts

Cross-device sync covers not only attempt text but learning intent:
- active StudySession/step
- RepairPlan position
- Review Queue state
- portable annotations/highlights
- selected resource/unit
- substantial unfinished IQS/PT
- notification-read state
- relevant preferences.

Server versions and conflict rules apply. Local caches must not silently overwrite newer server state.

## 28. Native Search and public-link behavior

Search results use the shared SearchProjection. Opening a canonical public BarClimb URL should:
1. open exact native destination when installed and supported;
2. retain canonical HTTPS fallback on web;
3. hydrate private learner overlay only after authenticated authorization;
4. never put private learner metadata into shared link previews.

## 29. Plus transition safety on native

Effective entitlement/capabilities are resolved server-side and cached only for UX continuity. During transient startup entitlement uncertainty, prefer suppressing inappropriate paid-user ads until authoritative status resolves where feasible.

Grace/cancel/downgrade/refund cannot destroy or strand accepted in-progress work. A privilege change applies at documented safe boundaries and preserves history, learner state, published contributions, Review Queue, RepairPlan history, and local recovery data according to retention rules.

## 30. Native offline boundaries for newer orchestration

Ordinary downloaded/cached Practice and in-progress writing may use offline recovery. New planner decisions, Search, community writes, entitlement-changing starts, new RepairPlan generation, and authoritative Progress recalculation generally require server connectivity unless an explicitly versioned offline contract exists.

When offline, show the last synchronized projection as stale/read-only where appropriate rather than inventing a new recommendation locally.

## 31. Additional native E2E flows

Add to the launch suite:
13. desktop/web StudySession starts → iPhone resumes same session intent and next eligible step.
14. Android adds Review item → web reflects it exactly once; Suggested Review remains separate.
15. Plus public-page deep link → native page opens with ad suppression and private overlay after auth, while copied share URL remains public-safe.
16. active RepairPlan → process kill → recovery → adaptation continues without duplicate evidence.
17. entitlement changes during an accepted PT → PT remains recoverable/submittable under safe-boundary policy; next privileged start observes new entitlement.
18. offline launch → stale Home projection clearly labeled/degraded → reconnect → authoritative Home refresh with no client-side learner recalculation.
