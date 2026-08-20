# BarClimb Native Platform Specification

**Status:** Authoritative v1 companion specification.

This document consolidates and supersedes the former Mobile Platform Contract. It governs iOS and Android as first-class product clients from the foundation onward, shared TypeScript contracts, React Native/Expo architecture, native assessment parity, offline/recovery, deep links, push, privacy, community parity, subscription verification, store release pipelines, and separate Native GA gates.

## Native advertising correction

Web external-fill advertising uses Google AdSense when approved and enabled. Native iOS/Android external-fill advertising uses Google AdMob when approved and enabled. Direct sponsorship and house campaigns may serve across web and native through BarClimb's own ad-decision service. A pending AdSense or AdMob approval must not block the learner product from launching; house ads or no external-fill ad are valid fallbacks. Paid users remain ad-free.

The server-side ad decision must therefore distinguish at least `WEB_ADSENSE`, `NATIVE_ADMOB`, `DIRECT`, `HOUSE`, and `NONE`, subject to consent/platform policy and the advertising invariant in the Build Constitution.

---

**Status:** Authoritative v1 companion contract  
**Date:** August 12, 2026  
**Scope:** iOS and Android architecture from Milestone 1 through Native GA, native UX, shared packages, authentication, deep links, offline behavior, notifications, billing, release, store policy, QA, and parity.

## 1. First-class native requirement and release sequencing

BarClimb is architected from the beginning for three first-class clients:

1. Web
2. iOS
3. Android

**Web GA is the first commercial public release.** iOS and Android follow through separate Native GA gates. Native applications therefore are not a disposable post-Web rewrite or an optional architecture seam; their high-risk foundations, shared contracts, build/signing prerequisites, and parity ledger begin during Milestone 1 even though public store distribution may occur later.

A mobile app may not be a thin WebView wrapper. It must ultimately provide a high-quality native study/community experience with platform-native navigation, text input, sharing, notifications, deep linking, offline resilience, and purchases.

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

Establish during Milestone 1 at foundation depth:

- stable bundle-identifier/application-ID strategy and environment-specific identities;
- Expo/EAS ownership or a documented equivalent build pipeline;
- securely managed signing/certificate/key architecture and at least one genuinely signed internal-build path where current account access permits;
- portable, fail-closed environment-specific API/config;
- dev/internal build profiles, version/build numbering, and a documented staged rollout/rollback strategy;
- source-map/symbol handling architecture for observability; and
- an explicit per-platform ledger for account access, signing, build, device/runtime, deep-link, and store evidence.

TestFlight, Google Play internal/closed testing, final platform signing/provisioning, production observability upload, and production rollout remain required at the applicable Native GA. An unavailable Apple team, store account, or test device is recorded as `BLOCKED_EXTERNAL` or `NOT_VERIFIED`; it does not by itself fail the Milestone 1 foundation gate when the portable architecture is in place and at least one permitted platform has produced a signed internal build. A JavaScript export is never a substitute for that signed-build proof.

Production Web GA must not silently imply native release. Each client has explicit release status. Web GA may precede public iOS/Android availability, but the native release pipeline, identifiers, build/signing foundations, deep-link contracts, and parity ledgers begin early and remain active so later Native GA is a release of the same product rather than a retrofit.

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

## 22. Native GA launch gate

Web GA may already be live when this gate is evaluated. BarClimb cannot call the applicable native platform publicly launched until:

- that platform's App Store or Google Play production release is approved/available or intentionally phased within a documented launch window;
- that platform passes its critical E2E flows on the required real-device/runtime matrix;
- store billing and restoration are verified in production/sandbox-equivalent flows as applicable;
- UGC report/block/moderation is functional;
- push deep links work;
- privacy/account deletion requirements are complete;
- crash/observability is live;
- assessment presentation parity is proven.

iOS and Android are independent Native GA gates: iOS GA does not wait for Android approval, and Android GA does not retroactively alter iOS status. Evidence and unresolved gaps remain platform-specific in provider and client-parity ledgers.

## 23. Native technical-risk spikes and evidence schedule

The project must prove the riskiest native assumptions early enough to prevent Web-only contracts. Throwaway-or-promotable prototypes cover:

1. schema-driven MCQ renderer with strike-through/highlighting;
2. IQS resource switching with persistent answer state;
3. long PT/LRPT editor with autosave, copy/paste, formatting, keyboard behavior, background/foreground recovery, and hardware-keyboard sanity on tablet;
4. Universal/App Link architecture and route mapping to an assessment/public response;
5. staging auth protocol + secure credential/token storage state machine;
6. one sandbox StoreKit product query and one Google Play test-product query as soon as store projects permit.

A failed spike can change the concrete native library/tool choice without changing the product contract. Renderer/editor contract risks in items 1–3 must be resolved before the related Milestone 4 feature is accepted rather than discovered at launch.

For Milestone 1/M1.4, items 4–5 are accepted at foundation depth only when native route configuration/canonical parsing exists, native authentication uses the shared server protocol, the SecureStore save/restore/delete/failure state machine has automated coverage, both platform exports and CI pass, and the evidence ledger is explicit. Live AASA/`assetlinks.json` publication and OS routing, physical-device SecureStore/authentication lifecycle, and the sandbox product queries in item 6 require the relevant external accounts/devices and may remain `BLOCKED_EXTERNAL` or `NOT_VERIFIED` until the applicable Native GA. They remain mandatory gates there and may not be inferred from config tests, exports, backend API calls, or another platform's signed build.

## 24. Account model decision for v1

V1 authentication is **email + username + password**, with email verification/password reset as configured. Do not add Google/Facebook/Apple social sign-in merely for convenience during v1; doing so creates additional identity/store-policy branches without improving the core launch loop enough to justify them.

A future social-sign-in change requires an auth-contract update and platform-policy review.

## 25. Developer-account prerequisites

At Milestone 1 kickoff, begin verification and document ownership/access or the exact external blocker for:

- Apple Developer Program / App Store Connect;
- Google Play Console;
- required bundle IDs/package names;
- signing and store roles using least privilege;
- organization-owned recovery/admin access rather than a single developer’s personal credentials where feasible.

Store-account setup is a schedule dependency, not a launch-week task. Missing Apple Developer Program enrollment/team access or Google Play ownership/recovery does not by itself block M1.4 foundation acceptance or Web development when the shared architecture, EAS/build-project control, one available signed internal-build path, and honest evidence ledger satisfy the foundation gate. It remains a hard prerequisite for the applicable Native GA and must be pursued early rather than silently deferred.

---

# CONSOLIDATED NATIVE BUILD RULE

The native apps are not wrappers around the website. They consume the same authoritative backend/domain contracts while owning platform-native interaction, storage, lifecycle, accessibility, billing, and distribution behavior. Web may reach GA first; iOS and Android become supported public clients when their separate Native GA gates pass.

# PART III — WEB-FIRST / NATIVE-GA RELEASE CONTRACT

## 26. Strategic release sequencing

BarClimb uses Web-first commercial release sequencing. Native remains first-class from Milestone 1, but public App Store/Google Play release no longer blocks Web GA.

This is **not** permission to defer native architecture. Before Web GA, the project must preserve and continuously test the seams that are expensive to retrofit later:

- one backend/domain identity across clients;
- opaque/revocable native authentication architecture;
- stable canonical HTTPS URLs and deep-link route registry;
- Assessment Presentation Schema and client capability manifests;
- server-authoritative attempts/autosave/evidence/recommendations;
- portable annotation/resource anchors;
- provider-neutral Subscription/Entitlement models;
- public/community IDs and moderation semantics;
- privacy/deletion semantics;
- environment-specific API configuration;
- internal build/signing/store-account prerequisites and technical-risk spikes.

External Apple/Google enrollment, platform-final signing, physical-device access, association publication, review, or store delays are tracked as platform-specific native-release dependencies. They do not hold M1.4 acceptance or the Web milestone train hostage when the Milestone 1 foundation obligations are met, but no missing proof is treated as completed or removed.

## 27. Native GA obligations after Web GA

Each platform must independently pass:

- production-capable signed build and release pipeline;
- critical assessment-family parity;
- PT/LRPT editor and recovery on target devices;
- SecureStore/session restoration/revocation on real runtime;
- Universal/App Links;
- push notification routing;
- account deletion/privacy surfaces;
- UGC report/block/moderation;
- provider-neutral Plus entitlement consumption;
- StoreKit/Google Play purchase, restore, grace, refund/revocation behavior when native purchases are offered;
- accessibility/device matrix;
- crash/observability;
- store metadata/review readiness.

The iOS gate specifically requires an authorized Apple Developer Program team, final bundle/signing/provisioning, a signed iOS internal and production/store-capable build, physical-device Keychain/SecureStore and authentication lifecycle proof, published AASA association with real Universal Link routing, App Store approval, and native purchase/restore lifecycle evidence when purchases are offered. The Android gate specifically requires production/store-capable signing, physical-device Keystore/SecureStore and authentication lifecycle proof, published `assetlinks.json` association with real App Link routing, Google Play ownership/recovery and approval, and native purchase/restore lifecycle evidence when purchases are offered. Evidence is platform-specific: a signed Android internal APK proves the early signed-build path but proves none of the iOS, device-runtime, OS-routing, Play ownership, or production-purchase obligations.

A native client may launch later without altering scoring, learner evidence, public identity, community ranking, or subscription semantics established by Web GA.

## 28. Web-first compatibility gate

Before accepting a material Web feature intended for later native use, review must answer:

1. Is its server/domain contract renderer-independent?
2. Can iOS/Android consume the same API object without scraping Web HTML?
3. Is durable learner state server authoritative or safely syncable?
4. Does the canonical public URL have a future native route mapping?
5. Does monetization resolve through capabilities/entitlements rather than Web checkout state?
6. Is the remaining native implementation gap recorded in `CLIENT_PARITY.md`?

If any answer is no, the Web implementation is architecturally incomplete even if Web UI works.
