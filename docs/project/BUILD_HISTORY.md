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

## 2026-08-20 — M1.5 cross-client assessment presentation risk proof
- Began from clean accepted main `443bbbc849049d515d9c9b1797cd7909f50359f9` only after M1.4 exact-main Foundation CI passed; created bounded branch `m1-5-assessment-presentation-proof`.
- Replaced the reserved assessment-schema boundary with one runtime-validated portable contract covering the four canonical families, all canonical response-type identifiers, stable resources/units/choices, registered renderer components, and synthetic-fixture isolation.
- Added client-independent workspace state for selected answer, long-form draft, active resource/view, marked-for-review, inline/list/indent formatting, explicit autosave/recovery states, JSON serialization, and a replaceable persistence interface. No DOM/React/React Native dependency enters shared packages.
- Added platform-owned renderers: semantic Web radio/textarea/resource workspace and React Native accessible Pressable/TextInput resource workspace. Both consume the same fixtures/state; Web narrow/wide CSS and native runtime dimensions support phone/tablet and portrait/landscape architecture without orientation lock.
- Added deterministic MCQ, IQS, Standard PT, and LRPT fixtures marked `TEST_FIXTURE` / `DEVELOPMENT_ONLY`; production environments hide the proof. No Django assessment model/endpoint, curriculum, AI, grading, evidence, readiness, publication, SEO, or Milestone 2 feature was added.
- Exact Node 24.19.0/npm 11.17.0 acceptance passed clean install, live Expo compatibility, Doctor 20/20, all nine typechecks, 14 Web tests, 20 native tests, 8 shared schema/state tests, Web build, all seven portable packages, iOS/Android exports, Ruff/Django/migrations, and 60 local backend tests with four PostgreSQL-only skips. Audit remained the accepted 15-node `image-size`/`uuid` graph. Exact-commit GitHub CI remains the final branch gate.

## 2026-08-21 — M2.1 immutable official-source/scope foundation
- Began from accepted M1.5 main `0ebccf8da5e08fe18079e5d59477f33a956ae88b` after exact-main Foundation CI run `32434901406` passed; created bounded branch `m2-1-official-source-scope-foundation`.
- Added a Django official-source registry with immutable versioned artifact provenance and original-byte SHA-256, versioned multi-artifact national NextGen scope manifests, relational hierarchical scope items, source locators, and separate official treatment metadata.
- Added canonical scope hashing, idempotent controlled-manifest import, machine-readable validation, explicit transactional activation/supersession, historical-query preservation, production/test-fixture isolation, read-only admin, and an authenticated minimal active-scope API.
- Enforced `NEXTGEN_UBE` / `NEXTGEN_CORE` / national-only at model and database boundaries. Added PostgreSQL triggers against artifact replacement and active/superseded historical mutation. No official document binary, Rule Obligation, doctrine/compiler, curriculum certification, assessment inventory, learner evidence, or AI work was added.

## 2026-08-21 — M2.2a deterministic Rule Obligation compiler proof
- Began from accepted M2.1 main `1b3ee5996cf82c50f3b645e1c29831115023dbb1` after exact-main Foundation CI run `32441068155` passed; created bounded branch `m2-2a-rule-obligation-compiler-proof`.
- Added versioned Rule Obligations for all eleven controlling kinds, typed semantic relationships, immutable primary/secondary authority provenance, many-to-many official-leaf mappings, canonical hashing, and deterministic auto-approval/review/block decisions.
- Added lifecycle-driven compilation, reconciliation categories/coverage policy, staff review records, transactional certification, immutable CoverageReleaseSnapshots, scope-drift impact comparison, operator command, inspection-only Admin, and minimal authenticated certified-core API.
- Used synthetic `TEST_FIXTURE` corpus only. No real NCBE/legal corpus, commercial sourcebook, AI/embedding/LLM, assessment generation, learner evidence/readiness, public curriculum, or M2.2b work was added.
- Exact Python 3.13.15 clean install, Ruff/Django/migrations, 85-test SQLite and 93-test PostgreSQL suites, certified-history trigger proof, Celery smoke, exact Node/npm clean install, all Web/native/shared checks, Web build, Expo compatibility/Doctor, both exports, and audit-family comparison passed locally. No dependency or lockfile changed.

## 2026-08-21 — M2.2b real-source pilot second-review correction
- Started from accepted main `a468fb6d3d850757fe1af82c18f244e95ad77de8` on bounded branch `m2-2b-real-scope-authority-pilot`. Current official NCBE Content Scope/Blueprint and official U.S. Courts FRCP bytes were acquired only transiently, hash verified, and excluded from Git/API.
- First human review required corrections rather than approval. V1 compile/policy identity and its exact correction-required disposition are preserved; no reviewer identity or final attestation was fabricated and V1 was never certified.
- Created immutable V2 identities. Removed Candidate 1's two misleading procedural-step edges; changed Candidate 2 from `PROCEDURAL_STEP` to `LIMITATION`; corrected Candidate 3's Rule 4(h) addressee distinction, Candidate 4's omitted United States plaintiff predicate and expense wording, and Candidate 5's forum-state/service-state formulation. Candidates 6–8 and the two valid Rule 4(m) relationships remain unchanged.
- At the second-review checkpoint, transient exact-source execution reproduced scope checksum `2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f` and V2 compile checksum `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`. Reconciliation reported zero issues, one of one pilot leaves sufficient, 20 active testable leaves, and `national_complete: false`; certification was then blocked by absent V2 human attestations. The later approval/certification entry below supersedes only that pending state.
- Regenerated `M2_2B_HUMAN_REVIEW_PACKET.md` as the V2 packet and retained `M2_2B_HUMAN_REVIEW_PACKET_V1.md` as review history. No certification, merge, AI use, national-corpus expansion, assessment work, or next-slice work occurred.

## 2026-08-21 — M2.2b bounded pilot human approval and certification
- Recorded Leo Rayos's supplied identity, qualification, authority-review statement, common rationale, timestamp, and eight explicit `APPROVE` decisions in a body-free review manifest. The privileged operator workflow calls `record_obligation_review` for every candidate and does not fabricate an account or alter approved statements.
- Extended immutable review/snapshot evidence with reviewer identity, qualification, rationale, attestation/manifest hashes, authority provenance, and deterministic snapshot identity. PostgreSQL now rejects human-review update/delete directly; exact reruns return the same reviews and snapshot, while changed input fails.
- Reacquired-byte execution reproduced scope checksum `2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f` and compile checksum `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`; reconciliation remained zero-issue and primary-authority-complete.
- Certified only the one-leaf `PILOT_ONLY` compile. Snapshot `8ffc025a-ddac-5765-b7b2-130c84282c83` / `60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0` contains eight obligations, one covered target leaf, 20 active testable leaves outside the pilot, and `national_complete: false`.
- Ruff/Django/migration checks, 98 SQLite tests with nine PostgreSQL-only skips, all 107 PostgreSQL 14/Redis tests, all workspace format/lint/typecheck/tests/Web build, and shared-package portability passed. No raw source, AI, assessment, learner, client, dependency, provider, merge, or next-slice work was added.

## 2026-08-21 — M2.2c Civil Procedure subject foundation
- Began from accepted M2.2b main `2b042d158bb68307a0af223acec1542b62702d20` after exact-main Foundation CI run `32522925767` passed; created bounded branch `m2-2c-civpro-subject-foundation`.
- Added V1's immutable/versioned Civil Procedure subject manifest tied to the exact current official scope and the six coarse records then treated as official subject leaves, with production coverage policy `BARCLIMB_CIVPRO_COVERAGE_POLICY@2026_V1`. Later human review rejected that terminal-leaf interpretation; the V2 entry below preserves the correction without rewriting V1 history.
- Added 18 curriculum-layer coverage requirements and 75 typed slots, plus future certified-satisfaction links. These are structural planning truth, not Rule Obligation statements; counts cannot certify a leaf or subject.
- Added 16 authority-family acquisition plans and 45 mappings for actually applicable constitutional, statutory, federal-rule, Supreme Court, and optional-secondary evidence. Five case plans require exact case/proposition identity, locator, status, and later-treatment review; authority drift has deterministic impact rules.
- Linked the accepted Rule 4 snapshot unchanged as `PARTIAL_LEAF_COVERAGE`, `PILOT_ONLY`, and insufficient for leaf/subject completeness. No recertification or substantive-statement mutation occurred.
- Added read-only operator gap reporting, exact subject-plan import, privileged immutable external-human review workflow, inspection-only Admin, relational constraints, and PostgreSQL immutability triggers.
- Produced `M2_2C_HUMAN_REVIEW_PACKET.md`. The plan remains `REVIEW_PENDING`, with zero certified slots, `subject_complete: false`, and `national_complete: false`. No subject-wide candidates, assessment inventory, AI/provider integration, or next slice began.

## 2026-08-26 — M2.2c V2 terminal-topic structural correction
- Preserved the rejected V1 manifest and exact review packet; added an identity-honest `REJECT — REVISION REQUIRED` disposition without fabricating reviewer qualification, attestation, or approval.
- Verified the accepted 6,109,365-byte NCBE scope artifact against SHA-256 `22aa277048c04fdd887db66284c28bade9989b9f8a654fab05781bafa5b19b1a` in transient storage. Normalized 27 short factual terminal Civil Procedure topic identities with exact hierarchy, locators, and 14 starred/13 unstarred markers; no source PDF bytes or explanatory bodies were committed.
- Added immutable `SubjectOfficialTopic` hierarchy and classified the six accepted coarse scope records as BarClimb planning aggregates. Completeness now operates over terminal topics, 43 corrected requirements, and 157 typed slots; six-group and percentage shortcuts are explicitly rejected.
- Reworked jurisdiction, service/notice, venue, Erie/Hanna, TRO/PI, Rule 11, pleadings, joinder/intervention, discovery, jury preservation, dispositive motions, default/preclusion, and appellate planning. Removed required posttrial-relief and broad appellate-procedure overreach.
- Expanded to 22 authority plans and 76 requirement mappings with explicit conditional predicates, nine requirement-sensitive case plans, conditional FRAP, and national-only incorporated-state-law boundaries.
- Preserved the accepted Rule 4 V2 compile, reviews, snapshot, and checksums unchanged. Its timing and other out-of-perimeter obligations remain valid supplemental evidence and cannot inflate subject completeness.
- Generated the comprehensive active V2 review packet and stopped at `SECOND_REVIEW_PENDING`; no substantive candidate, approval, certification, merge, next slice, dependency, client, provider, or controlling-spec change was introduced.
- Final continuity, JSON/canonical hash, milestone, `git diff --check`, secret/generated-junk/raw-source, and scope-isolation scans passed. The final focused M2.2c run passed 18 tests with two intended PostgreSQL-only skips. Exact-commit CI exposed only separately scoped Expo patch drift.

## 2026-08-30 — Expo SDK 57 accepted-main patch maintenance
- Began bounded branch `maintenance/expo-sdk57-patch` from exact accepted main `2b042d158bb68307a0af223acec1542b62702d20`; paused M2.2c remained locally/remotely untouched at `0436b0d63cbab2fd1a0ef15125683da5967e4150`.
- Live Expo tooling independently required `expo@~57.0.18`, `expo-linking@~57.0.8`, `expo-secure-store@~57.0.2`, and React Native `0.86.3`. Applied only those direct stable SDK 57 patch corrections and npm-generated transitive lock reconciliation. React/ReactDOM 19.2.3, TypeScript 5.9.3/exclusion, Node 24.19.0/npm 11.17.0, application IDs, EAS identity, architecture, behavior, specs, providers, backend, assessment, and curriculum remain unchanged.
- Exact Node/npm clean `npm ci` installed 716 packages. All nine workspace typechecks, 14 Web tests, 20 native tests, 8 assessment-schema tests, Web production build, seven-package portability, live Expo compatibility, Doctor 20/20, and iOS/Android production exports at 863/858 modules passed.
- Ruff lint/format, Django system/migration checks, 98 SQLite tests with nine PostgreSQL-only skips, all 107 PostgreSQL 14/Redis 7.2 tests, and live Celery `infrastructure.smoke` passed. Exact Python 3.13.15 clean hash installation remains a hosted-CI gate because only Python 3.11.2 is available locally.
- `npm audit --omit=dev` improved from 15 aggregate nodes (10 moderate/5 high) across `image-size` and `uuid` to 10 moderate nodes rooted only in `uuid`; the patched Expo/Metro graph removes `image-size`. No force fix ran. Continuity, tracked JSON, canonical spec hashes, ten-milestone order, dependency/source isolation, `git diff --check`, and secret/generated-junk review passed. Maintenance branch CI run `33335000102` and exact-main CI run `33337075531` passed before integration into M2.2c.

## 2026-08-30 — Accepted maintenance integrated into M2.2c V2
- Normally merged accepted main `1a264422dcf692e867b1f3642111f41494023c7f` into the published M2.2c branch without rebase, squash, cherry-pick, reset, force-push, or history rewrite. Six continuity conflicts were reconciled by preserving both chronological records; dependency and curriculum files did not conflict.
- Inherited the exact accepted Expo/Linking/SecureStore/React Native lock state and 10-moderate/uuid-only audit evidence. Preserved all M2.2c V1/V2 packets, terminal topics, treatments, requirements, slots, authority mapping, Rule 4 evidence, and false subject/national completeness without substantive change.
- Integrated local validation passed: exact Node/npm clean install; all nine typechecks; 14 Web, 20 native, and 8 schema tests; Web build; seven-package portability; live Expo compatibility; Doctor 20/20; and iOS/Android exports at 863/858 modules. Ruff/Django/migration checks, 116 SQLite tests with 11 skips, all 127 PostgreSQL 14/Redis tests, the focused 18-pass/2-skip M2.2c suite, and live Celery smoke passed. Audit remains 10 moderate and uuid-only. Exact-merge CI remains before returning the branch to the second human-review gate. No review, approval, certification, candidate compilation, merge to main, or subsequent slice began.

## 2026-08-31 — M2.2c V3 narrow second-review correction
- Recovered an interrupted uncommitted run at exact branch SHA `8f640c19eace479c87391e7acb75630ccf01f714`. It had created only an exact V2 packet archive and a partial V3 manifest with version metadata plus the TRO/PI `RULE`/`DISTINCTION` narrowing; no commit, push, staging, test change, continuity change, approval, or certification existed.
- Preserved V1 and exact V2 packet history. `M2_2C_V2_REVIEW_DISPOSITION.json` records **REVISE — NARROW V3 CORRECTION REQUIRED** without inventing reviewer identity, qualification, attestation, or approval. Active V3 stops at `THIRD_REVIEW_PENDING`.
- Added immutable manifest/policy V3 identities while retaining all 27 topics, 14-starred/13-unstarred treatment, six planning-only aggregates, and 43 requirements. Removed eight artificial mandatory slots without replacement padding: TRO/PI net -3, severance -1, claim preclusion -1, issue preclusion -1, final judgment -1, and standards of review -1, producing 149 slots.
- Corrected only reviewed authority boundaries: FNC case authority is required and Title 28 conditional for statutory-transfer contrasts; concurrent jurisdiction and well-pleaded-complaint propositions require controlling Supreme Court support; Title 28 remains proposition-sensitive; TRO/PI case authority is conditional while rule-grounded FRCP support remains required. Erie/FRAP/state-incorporation boundaries and all 22 authority-plan identities remain unchanged.
- Preserved Rule 4 compile `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`, snapshot `8ffc025a-ddac-5765-b7b2-130c84282c83`, and certification `60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0`. Zero V3 slots are certified; subject, subject-certification, and national completeness remain false. No substantive candidate, authority corpus, migration, dependency, client, provider, specification, application behavior, merge, or next-slice work was added.

## 2026-08-31 — M2.2c V3 review-packet presentation cleanup
- Separated the active V3 identity/immutable inputs from the archived V1/V2 review record and labeled every historical V1/V2 field explicitly. The packet retains one V3 title, one third-review-pending status, one V3 introduction, and only V3 operative manifest/policy/gate metadata.
- No topic, treatment, planning aggregate, requirement, typed slot, authority mapping, compiler/certification behavior, Rule 4 evidence, approval state, dependency, provider, application, specification, or subsequent-slice truth changed.

## 2026-08-31 — M2.2c V3 human coverage-plan approval
- Recorded Leo Rayos's supplied approval through the existing `record_subject_plan_review` operator workflow against reviewed commit `d4908c78cf185ce4bb5342802dfa79d7866af2d1`, V3 manifest SHA-256 `b706b7182ab165377a9e60520b083cdaf87562b256dfb0c371f9aa38d948c0c3`, policy/gate/scope identity, and exact reviewed packet SHA-256 `5a0b02efe178e2c8996a95cd19a5e1b0122ac242ad8505dad2b079e94dd9646b`. The immutable review manifest has SHA-256 `6ceea17f91c7523c993a25a702b6e7ab923117d8a918baa7ed916d57bac87c97`.
- Preserved the reviewed packet bytes separately and updated the active packet to **APPROVE — COVERAGE PLAN ACCEPTED**. Exact replay is idempotent; altered packet or review input is rejected.
- Approval satisfies only the V3 plan-review gate for a later separately authorized controlled compilation slice. No substantive candidate was compiled or approved, no authority was acquired, no slot was certified, no subject snapshot was created, and `subject_complete`, `subject_certified`, and `national_complete` remain false.

## 2026-09-02 — M2.2c accepted and Expo SDK 57 patch metadata refreshed
- M2.2c fast-forward merged into accepted main at `0947308d4ba5792119d5f03dc2f00ae2427da8ff` with its human-approved V3 plan and all false completeness/certification flags intact.
- Bounded maintenance commit `d06f37e4f0312c0e00391107f55a163c39ecac4b` updates only Expo 57.0.18 → 57.0.19, Linking 57.0.8 → 57.0.9, SecureStore 57.0.2 → 57.0.3, the Expo-required transitive lock graph, and current audit evidence. React Native 0.86.3 and React 19.2.3 are unchanged.
- Exact maintenance Foundation CI run `33687348735` passed continuity, Python 3.13.15/PostgreSQL/Redis/Celery backend gates, all client checks, live Expo compatibility, Doctor 20/20, and iOS/Android exports. The maintenance commit then fast-forwarded to main without a merge commit.
- Current npm metadata reports 17 moderate and zero high/critical aggregate nodes across the documented `uuid` and newly reported `decode-uri-component` families. React Navigation versions did not change; no audit fix ran.
- No application, backend, curriculum, candidate, authority, provider, native configuration, or controlling-specification change occurred. The next bounded Milestone 2 slice requires separate authorization after exact-final-main CI.

## 2026-09-03 — M2.2d bounded federal-question authority and candidate compilation
- Created `m2-2d-civpro-federal-question` from clean accepted main `e7b1517dc0a048ecf4b102306dd0e9e86f2401f8` after continuity and exact-main CI run `33687821581` passed.
- Acquired only official House 28 U.S.C. § 1331 and official U.S. Reports Mottley source bytes transiently. Their exact SHA-256 values are `f1a418156a2be3117aa698c83788ff6b544d68c602bb4559d06cc2daa2129ac7` and `73c4f2d4ada6a12b94106e045533c9b835a492cba9475f09de4da267341978ec`; no raw source body entered Git. Article III and all unrelated authority families remained unacquired.
- Added immutable requirement-specific authority acquisition, proposition-type evidence, exact candidate-to-approved-topic/requirement/slot mapping, effective partial authority-plan reporting, and PostgreSQL database-level immutability. Existing plan, authority, compiler, Rule 4, and certification truth is preserved.
- Compiled exactly three `REVIEW_REQUIRED` candidates for `civpro-topic-federal-question-jurisdiction`: one `RULE`, one `ELEMENT`, and one `LIMITATION`. Exact-byte compile `a46fbd51a441ec54fa74f2826a50241ff94e4fd3eefa49e24e568174d15b606d` has zero reconciliation findings, three required human reviews pending, and `certification_eligible: false`.
- Generated `M2_2D_CIVPRO_FEDERAL_QUESTION_HUMAN_REVIEW_PACKET.md` and stopped at candidate review. No approval, slot satisfaction, topic/subject certification, snapshot, other topic, provider/client/dependency/specification change, merge, or later slice was introduced.

## 2026-09-03 — M2.2d exact candidate approvals recorded
- Recorded Leo Rayos's supplied `APPROVE` decisions for the exact federal-question `RULE`, `ELEMENT`, and `LIMITATION` through the existing `apply_obligation_reviews` → `record_obligation_review` workflow.
- Extended that workflow's manifest envelope to bind the exact compile/input/reviewed-packet checksums plus candidate statement/canonical hash, topic/requirement/slot/treatment mapping, authority source hash and proposition evidence, and relationship edges. Exact replay created zero records; altered statement, authority hash, compile checksum, or packet is rejected.
- Preserved the pre-review packet byte-for-byte at SHA-256 `4fdf1c70c1a4228537880c500856198809ef368d53abbc465027bb5389696eda`. Candidate-review status is `APPROVED` and the prerequisite is eligible, but topic/subject certification remain false, no snapshot exists, and subject/national completeness remain false.

## 2026-09-04 — Expo SDK 57 patch-metadata maintenance 3
- Began from exact accepted main `e7b1517dc0a048ecf4b102306dd0e9e86f2401f8` on `maintenance/expo-sdk57-patch-3`; published M2.2d remained untouched at `c3e71259c6839ec3ae46d57e92e1da402b04a370` during maintenance.
- Live Expo SDK 57 tooling required only `expo@~57.0.20`. The npm lock consequently refreshes Expo 57.0.19 → 57.0.20, its nested CLI 57.0.21 → 57.0.22, modules-core 57.0.15 → 57.0.16, and modules-jsi 57.0.7 → 57.0.8. Linking 57.0.9, SecureStore 57.0.3, React Native 0.86.3, React/ReactDOM 19.2.3, and TypeScript 5.9.3/exclusion remain unchanged.
- Clean npm install, client checks, live Expo validation, Doctor 20/20, both exports, Ruff/Django/migrations, SQLite and PostgreSQL/Redis backend suites passed locally. Audit remains 17 moderate and zero high/critical across the existing `uuid` and `decode-uri-component` families. No audit fix ran.
- No application, backend behavior, curriculum, candidate, review, authority, certification, provider, app identity, EAS/signing, or controlling-specification change occurred. Exact maintenance, exact main, and integrated M2.2d CI remain required in that order.

## 2026-09-04 — Accepted maintenance integrated into M2.2d
- After maintenance CI run `33891560476` and exact-main CI run `33891769482` passed on `8463d68ce2e82d1b105646181da06ef8cf788583`, normally merged accepted main into published M2.2d without rebase or history rewrite. Only continuity conflicts were reconciled.
- Preserved all M2.2d compile/input/packet/review hashes, three approvals, authority hashes, relationships, and false certification/completeness state. No curriculum, candidate, authority, certification, application, provider, dependency, or specification change was introduced by the integration.
