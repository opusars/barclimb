# BarClimb Build History

## 2026-08-12 — Pre-kickoff specification and continuity baseline
- Consolidated controlling specification set to four document families.
- Locked NextGen-only v1, learning network, the then-current coordinated Web+iOS+Android release requirement, complete official-scope coverage, and cross-platform commerce/moderation requirements. The public-release sequencing was later superseded by the 2026-08-20 Web-first amendment without weakening multi-client architecture.
- Added chat-independent repository recovery protocol.
- Application implementation: not started in this bootstrap.
## 2026-08-13 — Pre-build coverage hardening
- Hardened the four authoritative specs before repository kickoff.
- Added immutable official source artifacts and source hashes.
- Added Rule Obligation Catalog + authority mapping beneath official scope items.
- Added official NCBE Sourcebook reconciliation and SubjectCoverageCertification.
- Added independent AssessmentScopeTarget confirmation so metadata cannot fake coverage.
- Added inventory maturity states, strict release validators, source-drift workflow, provisional exam-target handling, and CoverageReleaseSnapshot.
- Updated milestones to ten acceptance milestones across the six launch trains and made coverage assurance a GA blocker.


## 2026-08-13 — Final pre-build three-scenario architecture audit
- Audited canonical models, API/view surfaces, UI composition, state ownership, permissions, milestones, feature flags, admin, caching, entitlement, and native parity across SEO Visitor, signed-in Free, and Plus.
- Corrected the then-stale nine-milestone/Web-first language under the coordinated-launch decision and old pricing/permission language in the master Constitution. The coordinated public-release rule was later explicitly superseded by the 2026-08-20 amendment.
- Added server-composed projections and explicit orchestration/domain models/endpoints.
- Added security/idempotency/performance tests for anonymous claim, private overlays, cross-device state, entitlement transitions, Search privacy, and Plus ad suppression.
- Synchronized all four controlling specs and continuity state.

## 2026-08-13 — Repository kickoff continuity reconciliation
- Reconciled project state and handoff with the existing `main` repository and committed baseline.
- Standardized recovery validation documentation on `python3` while retaining the validator's portable Python 3 shebang.
- Resolved stale onboarding language: v1 is national NextGen UBE only and does not collect or depend on jurisdiction in onboarding, recommendations, analytics, assessment generation, or readiness.
- Rehashed the changed controlling Build Constitution and validated the continuity package.
- Application implementation remains not started; Milestone 1 is next.

## 2026-08-13 — M1.1 multi-client repository and toolchain foundation
- Created npm-workspace monorepo boundaries for Django/DRF, React web, Expo native, and seven platform-neutral TypeScript packages.
- Added environment-separated Django settings, a PostgreSQL production contract, health/readiness endpoints, and isolated SQLite foundation tests without business models.
- Added minimal web and native proof shells; native remains React Native, not a WebView.
- Added pinned Python/npm dependencies, shared format/lint/typecheck/test/build commands, setup documentation, and foundation CI.
- Initially selected Expo SDK 55 based on an incorrect conclusion that SDK 57 could not retain the controlling TypeScript 5.x baseline; M1.1a explicitly supersedes that rationale.
- Verified backend tests, web build, shared-package resolution, and iOS/Android Expo bundle exports. Milestone 1 remains in progress.

## 2026-08-13 — M1.1a dependency and runtime foundation correction
- Corrected the web graph to one exact React/ReactDOM 19.2.3 runtime and added a real ReactDOM root-shell mount test.
- Upgraded native to Expo SDK 57.0.12/React Native 0.86.2 while retaining TypeScript 5.9.3 through Expo's supported exclusion; removed forced portrait orientation.
- Upgraded Django to 5.2.17 and replaced direct-only Python requirements with pip-tools-generated, hash-verified production/development locks.
- Aligned Node 24.19.0/npm 11.17.0 across local version files, package metadata, CI, and recovery documentation.
- Added PostgreSQL 17 CI coverage and proved migrations, health, and readiness locally against temporary PostgreSQL 14.
- Enforced per-surface lint globals and ES2022-only portable shared-package boundaries, including an automated negative guard.
- Removed the tracked `.DS_Store` and redundant continuity workflow; the single foundation workflow still validates continuity.
- Patched directly actionable Vite/Vitest advisories and documented remaining upstream Expo/Metro/Xcode toolchain reachability. No application business feature was introduced.

## 2026-08-13 — M1.2 runtime and environment foundation
- Integrated Celery 5.6.3 with Django through an environment-driven Redis/Valkey-compatible broker and explicit no-result-backend behavior.
- Added only the non-contractual `infrastructure.smoke` task to prove discovery and worker execution; no business tasks or models were created.
- Formalized local/test/review/staging/production configuration, fail-closed deployed validation, safe `.env.example` values, and structured process/environment logs.
- Extended readiness to check PostgreSQL and required KVS connectivity while keeping liveness dependency-free and optional future providers outside readiness.
- Added Heroku `web`, `worker`, and safe `release` process types; no scheduler, deployment, or managed provider was introduced.
- Extended CI for PostgreSQL 17, Redis 7.2, deterministic eager tests, and a real Celery worker smoke while preserving Web/Native/shared-package checks.

## 2026-08-13 — M1.3 identity and authentication foundation
- Established the minimal custom Django user before business migrations: normalized private email login, normalized unique future-public username, and Django password handling only.
- Added same-origin Web session/CSRF signup, login/logout, session lookup, verification, password reset, secure production transport/cookie settings, and authenticated-self contract.
- Added server-revocable/expiring opaque native sessions, digest-only PostgreSQL persistence, Expo SecureStore restoration/removal, and shared iOS/Android auth shell flows.
- Added purpose-bound, expiring, rotating, single-use email action tokens behind provider-neutral Django delivery; no email provider was verified.
- Added KVS auth throttles, owner/staff authorization primitives, security-negative tests, and foundation auth surfaces without learner/profile/entitlement/product work.

## 2026-08-13 — M1.3a authentication boundary hardening
- Removed action credentials from router-visible paths/query strings by emitting canonical-Web fragment links and immediately cleaning Web history before CSRF-protected body submission.
- Serialized native issuance/reset on the user row and bound native sessions to an authentication generation so every lock ordering rejects or invalidates old-password credentials; Web sessions continue to invalidate through Django's password hash.
- Enforced HTTPS across review/staging/production and documented/tested the Heroku rightmost-forwarded-address trust contract, IPv4/IPv6 normalization, casing-resistant identity throttles, and generic fail-closed KVS behavior.
- Added the PostgreSQL `AuthEmailDelivery` outbox with credential-free UUID task publication, deterministic digest-only retry credentials, leases, cancellation/terminal states, bounded retries/backoff, scheduled broker-recovery sweep, and manual replay command.
- Hardened native restore/save/logout state handling for authoritative rejection, transient connectivity/5xx, and every SecureStore rejection path; added case-insensitive Bearer parsing and safe non-JSON Web auth errors.
- Added focused SQLite/security and PostgreSQL row-lock race coverage without entering learner, entitlement, curriculum, assessment, billing, community, or provider-integration scope.

## 2026-08-15 — Accepted-main Expo patch continuity correction
- Updated the Expo SDK 57 direct dependency from 57.0.12 to the current Expo-recommended `~57.0.13` patch range after Expo compatibility metadata made the CI dependency check fail on unchanged accepted `main`.
- Regenerated the npm lock with Expo's compatible transitive patch set. React Native remains 0.86.2 and TypeScript remains 5.9.3 under the existing Expo validation exclusion.
- Re-ran dependency validation, Expo Doctor, all Web/native/shared checks, both production bundle exports, backend foundation/auth checks, audit review, and continuity checks. No application behavior or M1.4 functionality was introduced.

## 2026-08-15 — M1.4 staging auth and client proof (in progress)
- Replaced manual Web auth switching with stable React Router destinations and same-origin Django serving for direct/refresh requests; fragment credentials remain memory-only and are removed immediately.
- Added React Navigation unauthenticated/authenticated boundaries, navigation-only future destination placeholders, fail-closed native/Web environment selection, distinct environment app IDs, and canonical-link parsing.
- Added Universal/App Link association endpoints and Expo platform configuration, but deliberately kept published association disabled and excluded credential-bearing auth completion paths until real signing identities are verified.
- Added a staging-only validating auth-email sink that production rejects, Heroku-compatible Web build/static collection, and explicit Heroku KVS self-signed TLS handling following provider guidance.
- Provisioned persistent non-production `barclimb-staging`, Essential-0 PostgreSQL `postgresql-aerodynamic-56880`, and Mini KVS `redis-flat-93728`; deployed code release v8 at commit `6bec558` with Web/worker/beat active. A later staging credential rotation advanced the current configuration release to v12; all three processes and database/KVS readiness recovered without a code change.
- Verified deployed migrations, HTTPS redirect/forwarded protocol, PostgreSQL/KVS readiness, direct Web routes, Web session authentication, native bearer issuance/revocation, spoof-resistant auth throttling, scheduled beat recovery, worker outbox delivery, and sanitized logs.
- At this point M1.4 was incomplete: EAS was not authenticated, full Xcode and Android tooling were absent, internal builds were not produced, and actual iOS/Android auth/SecureStore behavior was not exercised. Later entries supersede this status.

## 2026-08-20 — Web-first commercial release-strategy amendment
- Reconciled the supplied four-spec amendment into the controlling bundle: Web GA is first, followed by independent iOS and Android Native GA gates, while one multi-client architecture remains mandatory from Milestone 1.
- Preserved national NextGen-only v1 onboarding, provider-neutral entitlement, canonical cross-client truth, portable assessment/workspace contracts, and the three Visitor/Free/Plus Web GA journeys; corrected stale jurisdiction, Stripe-specific truth, and coupled-native-gate text found in the supplied Build/Native documents.
- Reframed the same ten milestones into Web GA delivery gates plus continuing Native GA obligations. M1.4 native risk proof remains required architecture insurance; native store release itself is not a Web GA blocker.
- This amendment occurred while `m1-4-staging-auth-client-proof` was already in progress. That branch remains intentionally unmerged and must merge amended main before continuing; M1.5 remains blocked pending M1.4 completion or explicit re-scope.
- No application, dependency, environment, provider, deployment, or M1.4 file changed.

## 2026-08-20 — Accepted-main Expo SDK 57 patch follow-up
- Updated only the native direct Expo range from `~57.0.13` to `~57.0.15` after Expo's hosted SDK 57 compatibility metadata made the specification-amendment CI dependency gate fail on unchanged accepted main.
- Regenerated the npm lock through Expo tooling. Expo-owned CLI/config/asset/constants/file-system/modules patches refreshed and the CLI graph deduplicated; React/ReactDOM, React Native, SecureStore, TypeScript, Node, npm, and application behavior remained unchanged.
- Re-ran clean install, Expo compatibility/Doctor, all workspace checks, Web build, both native exports, backend foundation/auth regression, audit, continuity, and diff checks. No specification, M1.4, provider, route, auth, staging, EAS, deep-link, SecureStore, or product work entered the correction.
- The Web-first specification amendment and M1.4 remain separate unmerged branches; M1.5 remains blocked.

## 2026-08-20 — Web-first amendment accepted-main integration
- Fast-forwarded accepted main to the already-reviewed Expo SDK 57.0.15 maintenance commit after its exact branch CI passed, then required and received green main CI on the same commit.
- Merged accepted `origin/main` into `spec-web-first-release-strategy` without rebasing or rewriting published history. Reconciled continuity while preserving all four amended controlling specs, their manifest hashes, the accepted dependency lock, and application implementation.
- At this point the amendment remained pending until review/merge and M1.4 was incomplete/unmerged at `fa5b2e7`; later entries supersede this status. M1.5 remained blocked.

## 2026-08-20 — M1.4 continuation under accepted Web-first strategy
- Merged accepted main `4850b78` into the published M1.4 branch without rebasing or rewriting history, preserving the amended controlling specifications and the existing M1.4 implementation/evidence.
- Reconciled M1.4's React Navigation/link dependencies with the accepted Expo SDK 57.0.15 baseline and regenerated the npm lock deterministically.
- Web GA remains first, while M1.4 continues as mandatory early native architecture insurance. M1.5 remains blocked until M1.4 is completed or explicitly re-scoped from evidence.
- Authenticated Expo/EAS as an Owner and linked the repository to the existing `@opusarss-team/barclimb` project without creating a duplicate. Apple/Android signing, internal-build, native-runtime, and OS association evidence remain separate gates.
- Produced signed Android internal build `f2b86aba-4cec-4660-b8dd-f14ea112f134` from merge commit `9174007` using EAS-managed credentials. The noninteractive iOS build stopped before upload because no suitable internal-distribution credentials exist.
- Corrected the Heroku account diagnosis: the earlier forbidden result came from unrelated account `leor@cashcopawn.com`. Fresh CLI authentication verified `apollonomios@gmail.com` as the staging owner; all three processes and both managed data services are available, and no suspension/deletion is scheduled.
- Declared `ITSAppUsesNonExemptEncryption=false` in dynamic Expo configuration because the current app uses only standard/exempt OS-provided HTTPS and SecureStore encryption and contains no proprietary cryptography.
- Produced exact-executable-state Android internal build `2e340187-f441-4175-ba8b-852d044996f7` from commit `2e32876` with the existing EAS-managed keystore; the signed APK is build-only non-production evidence.
- At the time of this evidence audit M1.4 remained incomplete under the earlier ambiguous gate: no BarClimb Apple Developer Program team existed, no actual iOS/Android runtime or SecureStore lifecycle was exercised, and OS association remained disabled/unverified. The later gate-reconciliation decision below relocated those external proofs to Native GA without marking them verified.

## 2026-08-20 — M1.4/Web-first foundation-gate reconciliation
- Began from clean accepted main `4850b7829e9a5f6205082a761643d6f109de7fd6`, after exact-sha Foundation CI runs `32416558206` and `32417562112` passed and the Web-first amendment was authoritative. Created `spec-m14-web-first-gate-reconciliation`; the published M1.4 branch remained untouched at `4c1d2e64a0ab2e29684fcf95599ab2c4e27cf769`.
- Amended all four controlling specification families to define the M1.4 foundation evidence package: persistent staging/PostgreSQL/KVS and Web/worker/beat; deployed Web auth; portable native auth, navigation, environment/config, and deep-link architecture; verified native build-project control; automated SecureStore state coverage; green Web/native CI and both exports; an explicit evidence ledger; and at least one actual signed native internal-build path where accounts permit.
- Recorded that the existing signed Android internal build qualifies for the available-platform signing proof while a JavaScript export does not. The current green M1.4 evidence appears sufficient for acceptance only after this amendment reaches main and that branch is brought forward, reconciled, rerun, reviewed, and merged.
- Relocated rather than removed externally blocked proof. Apple enrollment/team, final iOS signing/provisioning and signed builds, physical-device iOS/Android auth/SecureStore lifecycle, published AASA/assetlinks and actual OS routing, Google Play ownership/recovery, store approvals, and native production purchase/restore remain mandatory before their applicable independent Native GA.
- Updated the manifest hashes and recovery/state/handoff/history/decision/test/parity/provider/release continuity. No application, dependency, environment, deployment, or M1.4 branch file changed; M1.5 remains blocked.

## 2026-08-20 — M1.4 foundation acceptance
- Merged authoritative main `95b2d269566aae8a16045341d983b396c2a7a717` normally into `m1-4-staging-auth-client-proof` without rebasing or rewriting history. Nine continuity-only conflicts were reconciled; all controlling specifications/manifest came from main and all legitimate M1.4 implementation/evidence remained intact.
- Revalidated the clarified foundation gate on exact Node 24.19.0/npm 11.17.0: clean install, Expo compatibility/Doctor, all nine typechecks, 9 Web tests, 18 native tests, Web build, seven portable packages, both exports, Ruff/Django/migrations, 60 local backend tests, continuity/manifest/JSON/milestone checks, and evidence/architecture review passed.
- Fresh read-only staging checks confirmed correct Heroku ownership, Web/worker/beat, PostgreSQL/KVS, health/readiness, HTTPS/redirect, Web auth routes, anonymous auth enforcement, and intentionally unpublished association files. Fresh EAS checks confirmed Owner project control and the finished signed Android internal build.
- The production audit remained the accepted 15-node `image-size`/`uuid` toolchain baseline. No application, dependency, resource, credential, or provider state changed during acceptance.
- Marked M1.4 foundation accepted pending exact-commit CI, review, and merge. Apple/iOS signing, physical-device authentication/SecureStore, live OS links, Google Play ownership/approval, store approvals, and native production purchase/restore remain open Native GA blockers. M1.5 remains blocked until merge.
