# BarClimb Decision Log

These are durable pre-build decisions. Supersede explicitly; do not silently delete.

- **NextGen-first:** v1 is the national NextGen UBE product. Jurisdiction add-ons are dormant future components, not v1 UI. V1 onboarding does not ask for jurisdiction, and recommendations, analytics, assessment generation, and readiness must neither require nor depend on it.
- **Assessment intelligence:** deterministic planning/specification precedes AI generation; raw first-pass AI is never learner-visible.
- **Complete coverage:** official NCBE scope manifest, not question count, defines curriculum completeness.
- **Schema-driven assessment UI:** AI composes only registered presentation/resource/response components.
- **Learning network:** public responses may become network nodes with threaded discussion, educational signals, qualified views, username identity, Circles, reputation, and sharing. Generic Like/Dislike and infinite social feeds are excluded.
- **Private mastery boundary:** community popularity/reputation never changes readiness/mastery.
- **Native at launch:** Web, iOS, Android are first-class v1 clients; React Native/Expo is default native architecture unless an early spike proves a blocker.
- **Commerce:** server-authoritative cross-platform entitlement; Stripe web, Apple iOS, Google Play Android.
- **Healthy engagement:** Momentum/meaningful achievements, not punitive streak loss or doomscrolling.
- **Repository memory:** the repository ZIP must be sufficient to resume with zero chat history.
- **Coverage assurance v2 (2026-08-13):** “Complete coverage” means complete coverage of the current published NCBE scope, not a raw question count or an unverifiable claim to every conceivable rule. The release proof requires checksum-verified official sources, literal scope manifest, bidirectional mappings, reviewed Rule Obligations, authority mappings, applicable official NCBE Sourcebook reconciliation, per-subject catalog certification, independently confirmed assessment coverage targets, launch seeding, and strict CI/release snapshots.
- **Coverage tagging cannot self-prove (2026-08-13):** an assessment counts toward inventory/learner coverage only when independent validation confirms the named scope/RuleObligation target is materially exercised; context-only/incidental tags never count.

- **Three-scenario canonical architecture (2026-08-13):** Visitor, Free, and Plus experiences use one assessment/curriculum/learner truth. Complex pages consume server-authoritative versioned projections (`HomeProjectionV1`, public private overlays, Search/Progress/Attempt/Grade/capability projections) instead of client-side recomputation.
- **Orchestration is domain state (2026-08-13):** Study Sessions, Review Queue, Suggested Review, Repair Plans, learner planning snapshots, Session Impact, anonymous discovery/claim, notifications, and community launch models are explicit backend contracts, not frontend-only dashboard state.
- **Capability-driven Plus (2026-08-13):** clients render effective capabilities from server entitlement rather than scattering Free/Plus conditionals. Plus never changes scoring/mastery/community rank and is ad/upsell-free globally while authenticated.
- **Personalized public pages stay private (2026-08-13):** canonical SSR/SEO content is identity-independent; signed-in learner status is hydrated through private no-store overlays and never enters shared caches, metadata, sitemaps, or link previews.
- **Sourcebook dependency correction (2026-08-13):** NCBE Sourcebooks are optional enhanced reconciliation only. Mandatory coverage uses official NCBE perimeter + authoritative law + lawful independent reconciliation; automation remains the core compiler path.

- **Capability-driven surface parity (2026-08-13):** a versioned client surface capability manifest gates activation of Home, Search, Review, Repair, overlays, community, creator analytics, and account surfaces across required launch clients; plan names do not become scattered UI business logic.
- **Provider-agnostic subscription domain (2026-08-13):** `billing.Subscription`/provider events are canonical across Stripe, Apple, and Google. Stripe-specific IDs/tables are implementation details, not the product subscription truth.
- **Orchestration lifecycle hardening (2026-08-13):** StudySession, RepairPlan, entitlement, anonymous claim, review acceptance, and notifications have explicit lifecycle/idempotency/security obligations; safe-boundary entitlement changes cannot destroy accepted in-progress work.
- **Repository kickoff complete (2026-08-13):** the committed `main` repository baseline is authoritative; Milestone 1 is the next implementation milestone, and future recovery must not repeat bootstrap copy/initialization steps.
- **M1.1 monorepo/toolchain (2026-08-13):** use npm workspaces with `apps/backend`, `apps/web`, `apps/native`, and platform-neutral `packages/*`. Web and native own separate presentation implementations; shared packages expose only portable contracts, types, tokens, validation, analytics-event envelopes, and feature-flag shapes.
- **Runtime baselines (2026-08-13):** target Python 3.13, Django 5.2 LTS, DRF 3.16, Node 22.13, React 19.2, and TypeScript 5.x. Use Expo SDK 55/React Native 0.83 because Expo SDK 57 requires TypeScript 6 and would contradict the controlling kickoff baseline.
- **M1.1 database testing (2026-08-13):** PostgreSQL remains mandatory for real environments. In-memory SQLite is permitted only for isolated framework health tests; database-sensitive integration work must use PostgreSQL.
