# BarClimb Project Handoff

## Current state
M2.1 is accepted in `main` at `1b3ee5996cf82c50f3b645e1c29831115023dbb1`; exact-main Foundation CI run `32441068155` passed. M2.2a is implemented and fully validated locally on `m2-2a-rule-obligation-compiler-proof`, pending exact-commit CI, review, and merge. It proves deterministic Rule Obligation compilation/reconciliation/certification against immutable M2.1 scope identities using synthetic fixtures only. It does not import current real NCBE sources, establish a production national curriculum, add AI, or begin M2.2b. Accepted M1 platform evidence and deferred Native GA blockers remain unchanged.

The controlling release sequence remains **Web GA → iOS Native GA → Android Native GA**, with one first-class multi-client architecture and no Web-only shortcuts. Apple enrollment/signing, physical-device authentication/SecureStore, live OS association routing, store ownership/approval, and native production purchase/restore remain mandatory at the applicable Native GA and are not marked verified. M1.5 changes none of those provider/device statuses.

## Authoritative contracts
See `../specs/SPEC_MANIFEST.json`. Four Markdown specs control the build.

## Completed through repository kickoff
- Product/architecture/learning/network/native requirements consolidated.
- Ten acceptance milestones organized into six launch trains.
- Repository continuity/recovery system defined.
- Five coverage safeguards machine-specified: immutable official source artifacts, literal scope manifest, bidirectional mapping, maturity-based inventory coverage, and strict CI/release validation.
- Second-pass safeguards added: Rule Obligation Catalog, primary/exam authority mapping, automated multi-source reconciliation, optional enhanced NCBE Sourcebook reconciliation when lawfully available, subject coverage certification, assessment coverage-target confirmation, source-drift monitoring, provisional exam-target handling, and reproducible CoverageReleaseSnapshots.
- Three-scenario system audit completed: anonymous SEO discovery, signed-in Free, and Plus now share canonical models/assessment truth with server-composed projections, private public-page overlays, explicit StudySession/Review/Repair domain objects, capability-driven entitlement UI, cross-device orchestration, and release-blocking integration tests.
- Baseline repository committed on `main`; recovery commands and continuity state reconciled to repository reality.
- V1 jurisdiction posture made explicit: national NextGen UBE only, with no jurisdiction collection or dependency in onboarding, recommendations, analytics, assessment generation, or readiness.

## Completed in M1.1/M1.1a
- npm-workspace monorepo boundaries for `apps/backend`, `apps/web`, `apps/native`, and seven shared TypeScript packages.
- Django 5.2.17/DRF 3.16 environment-separated settings with PostgreSQL as the real-environment contract, a PostgreSQL CI/test setting, and SQLite isolated to foundation tests.
- Versioned `/api/v1/health/` and database-backed `/api/v1/ready/` endpoints with automated tests.
- One deduped React/ReactDOM 19.2.3 web runtime with a real root-shell mount test, and Expo SDK 57.0.15/React Native 0.86.2 native foundation. M1.4 replaces simulated destination state with React Navigation.
- TypeScript remains on the controlling 5.x line at 5.9.3 through Expo's supported dependency-validation exclusion.
- Hash-verified pip-tools production/development locks, npm 11 lock/install-script policy, per-surface lint environments, ES2022-only shared-package type environments, and an explicit portability gate.
- Node 24.19.0/npm 11.17.0 and Python 3.13.15 are aligned in version files, package metadata, CI, and setup documentation.
- Forced portrait orientation removed. M1.4 later establishes real native routing and gated deep-link foundations.

## Completed in M1.2
- Celery 5.6.3 Django integration with Redis/Valkey-compatible environment-driven broker/cache configuration, no result backend, deterministic eager tests, explicit conservative delivery defaults, and one non-contractual infrastructure smoke task.
- Explicit local/test/review/staging/production settings; fail-closed deployed secrets/URL/host/origin validation; safe public client API-base configuration; no provider credentials.
- Dependency-free liveness and PostgreSQL/KVS readiness with safe dependency labels, plus structured process/environment logs that exclude configuration and business payloads.
- Heroku `web`, `worker`, and release-check/migration process definitions. M1.2 added no speculative scheduler; M1.3a later adds beat for durable authentication-email recovery.
- Local PostgreSQL 14 + Redis 7.2 + live worker proof; CI models PostgreSQL 17 + Redis 7.2 and live worker execution. M1.4 later verifies the persistent Heroku topology and managed add-ons.

## Completed in M1.3
- Minimal custom Django `accounts.User` before business migrations: private normalized email login, normalized future-public username, Django password framework, no jurisdiction/profile/business state.
- Same-origin Web session authentication with explicit CSRF on every mutation, session rotation/logout, authenticated `/me`, verification, reset, secure-cookie/HSTS production settings, and no JWT/CORS expansion.
- Native opaque 30-day server sessions with digest-only PostgreSQL storage, server-side expiry/revocation, Expo SecureStore device-only persistence, startup restoration validation, and logout/reset cleanup.
- One-hour hashed/purpose-bound/rotating/single-use verification/reset actions and provider-neutral Django delivery. Console/in-memory delivery only was tested; SendGrid remains unverified.
- Hashed IP/identity KVS rate counters, reusable authenticated/admin/owner permissions, shared contracts, and scoped Web/iOS/Android auth screens.

## Completed in M1.3a
- Reset/verification links target the canonical Web origin and place credentials only in URL fragments. Web immediately removes fragment/query text with `replaceState` and submits credentials only in CSRF-protected POST bodies.
- Native issuance and password reset serialize on the user row; password/auth-security generation invalidates every pre-reset native credential, while Django's authentication hash invalidates Web sessions.
- Review/staging/production force HTTPS. Heroku client identity is the canonicalized rightmost router-appended forwarded address, with `REMOTE_ADDR` fallback; auth throttling fails closed with generic 503 when KVS is unavailable.
- `AuthEmailDelivery` is a durable PostgreSQL outbox with UUID idempotency, leases, bounded retries/backoff, terminal state, on-commit credential-free publication, one-minute beat recovery, and manual incident replay. Raw action credentials are derived only in worker memory and never stored plaintext or sent to Celery metadata/results/logs.
- Native restore distinguishes valid, authoritatively invalid, transient/offline/5xx, SecureStore read failure, and invalid-delete failure. Save and logout flows report server-revocation and local-deletion outcomes separately.
- M1.3a also makes Bearer scheme parsing case-insensitive and Web non-JSON errors safe. It adds no product domain or provider integration.

## Accepted-main dependency continuity corrections
- Expo's current SDK 57 compatibility metadata moved the recommended `expo` patch from 57.0.12 to 57.0.13 after M1.3a reached `main`, causing the CI-mode dependency gate to fail without an application-code change.
- The first correction used `~57.0.13`; accepted main now contains the Expo-required `~57.0.15` correction. M1.4 retains its React Navigation/Linking dependencies against that accepted lock baseline.
- React/ReactDOM remain 19.2.3, React Native remains 0.86.2, TypeScript remains 5.9.3 and intentionally excluded from Expo dependency validation, and Node/npm remain 24.19.0/11.17.0.

## Completed in M1.4 repository/deployed proof
- Web auth uses stable React Router paths for signup, login, verification, reset request/completion, and the authenticated proof shell; Django serves direct/refresh entry and hashed assets on the same staging origin as `/api/v1`.
- Native uses React Navigation auth and authenticated boundaries with navigation-only future placeholders. Local/staging/production API/Web origins and app identities are fail-closed; staging/production require HTTPS.
- Canonical-link parsing removes query/fragment data from fallbacks. Universal/App Link configuration is gated; verification/reset remain Web-only and association endpoints stay unpublished until signing identities are verified.
- Persistent `barclimb-staging` runs deployed commit `6bec558` with Essential-0 PostgreSQL `postgresql-aerodynamic-56880`, Mini KVS `redis-flat-93728`, and one Basic Web/worker/beat process each. The code deploy was release v8; credential rotation advanced the current configuration release to v12, after which all three processes and database/KVS readiness recovered.
- Deployed release/migrations, liveness/readiness, HTTPS redirect/forwarded protocol, direct routes, Web session auth, native bearer API issuance/revocation, rightmost-forwarded-IP throttling, beat recovery, worker delivery, and sanitized log evidence passed.
- The production-rejected staging email sink proves outbox processing without delivery or SendGrid verification. Heroku/Postgres/KVS and Expo/EAS are `VERIFIED_NONPRODUCTION`; other providers remain `NOT_VERIFIED`.
- Expo/EAS login verifies owner access to the existing `@opusarss-team/barclimb` project; the repository is durably linked to project ID `8ed30301-53d9-4630-b2c4-70d6d51f465b` without creating a duplicate.
- EAS internal build `2e340187-f441-4175-ba8b-852d044996f7` produced a signed Android staging APK from exact executable-state commit `2e32876bce0ecf315b174071fa6505d408f29258`; the stable evidence page is `https://expo.dev/accounts/opusarss-team/projects/barclimb/builds/2e340187-f441-4175-ba8b-852d044996f7`.
- Deferred Native GA evidence remains open: no BarClimb Apple Developer Program team currently exists, so iOS bundle/signing/profile/device setup and a real iOS build are blocked. This host lacks full Xcode/simctl and Android SDK/adb/emulator, and no actual native/SecureStore runtime proof exists. Android EAS signing is verified nonproduction, but Google Play ownership/recovery is not. Under the clarified gate these are not M1.4 foundation blockers and none is marked verified.

## Web-first release-strategy amendment
- Web GA is the first commercial/revenue release; iOS Native GA and Android Native GA follow as independent platform gates.
- Native public-store approval, production store purchase/restore, and public native release are not Web GA blockers merely because they are incomplete.
- Native remains active architecture insurance from Milestone 1: M1.4 risk proof, portable schemas/state, canonical URLs/deep-link contracts, provider-neutral entitlement, shared identity/curriculum/assessment/evidence/publication truth, and explicit capability/parity ledgers remain mandatory.
- The Web GA gate retains the anonymous SEO → substantive learning → Instant Practice → signup/claim, authenticated My BarClimb, and Plus ad-free/deeper-learning journeys.
- M1.5 began only after accepted M1.4 was fast-forwarded to main and exact-main CI passed.

## M1.4 gate reconciliation
- M1.4 foundation acceptance requires real staging with PostgreSQL/KVS and Web/worker/beat, deployed Web auth, portable native auth architecture, real native navigation, fail-closed portable configuration, EAS/build-project ownership, automated SecureStore state coverage, deep-link architecture/config, green Web/native CI and both exports, an explicit evidence ledger, and at least one real signed native internal-build path where current accounts permit.
- The signed Android staging APK is qualifying signed-build evidence; JavaScript exports alone would not be.
- Missing Apple enrollment/team, final Apple signing/provisioning/iOS build, physical-device auth/SecureStore lifecycle, AASA/assetlinks publication and OS routing, Google Play ownership/recovery, store approvals, and native purchase/restore do not indefinitely block M1.4 or Web development when the foundation gate passes.
- Every such deferred item remains a hard blocker for its applicable iOS or Android Native GA. Evidence may not be inferred across platforms or proof types.

## M1.4 foundation acceptance evidence
- Persistent nonproduction staging, PostgreSQL, and KVS: `barclimb-staging` is owner-accessible; Essential-0 PostgreSQL 18.3 and Mini KVS 8.1.9 are available; readiness reports both `ok`.
- Operational processes and deployed Web auth: Web, worker, and beat are up; HTTPS root and login/signup/app routes return 200, HTTP redirects 301, and anonymous `/api/v1/auth/me/` correctly returns 401. Earlier controlled staging signup/login/session, native bearer, outbox/beat/worker, proxy/rate-limit, and sanitized-log proofs remain valid.
- Portable native auth, real navigation, and fail-closed configuration: shared opaque-session contracts, React Navigation stacks/tabs, environment-specific app identities/origins, and rejection paths are implementation- and test-covered.
- Native build ownership and signed path: authenticated EAS Owner access to `@opusarss-team/barclimb` project `8ed30301-53d9-4630-b2c4-70d6d51f465b` is current; finished Android internal build `2e340187-f441-4175-ba8b-852d044996f7` is tied to executable commit `2e32876`.
- Shared validation: exact Node/npm clean install, Expo live compatibility and Doctor, all nine typechecks, Web/native tests, Web build, seven-package portability, both native JS exports, backend checks/tests, audit comparison, continuity, manifest/JSON/milestone checks, and diff/scope review pass.
- SecureStore and deep links: automated state-machine coverage exercises restoration, authoritative rejection, transient failures, save/delete failures, revocation, and logout; route/config parsing and association gating are tested. Staging AASA/assetlinks remain 404, correctly preserving real OS routing as a Native GA gap.
- No Web-only shortcut: shared-package portability passes, native uses React Native navigation rather than WebView, and the controlling portable auth/domain/link contracts remain intact.

## Current branch coordination
- Authoritative accepted main is `1b3ee5996cf82c50f3b645e1c29831115023dbb1`; local and remote main passed exact-SHA CI before M2.2a began.
- Active branch is `m2-2a-rule-obligation-compiler-proof`. It must pass full local/PostgreSQL validation, be committed and pushed, and pass exact-commit CI, then be reviewed. Do not merge automatically and do not begin M2.2b.

## M1.5 cross-client assessment presentation risk proof
- `@barclimb/assessment-schema` defines one runtime-validated, JSON-serializable presentation contract for the four controlling families and all controlling response-type identifiers. The bounded component registry contains only `SINGLE_SELECT_QUESTION` and `LONG_RESPONSE_EDITOR`; schema validation rejects unknown components and renderers return a typed fail-safe rather than omitting content or using HTML/WebView.
- One portable workspace state stores selected choice, draft document, active resource/view, review flag, formatting ranges/list/indent semantics, and save/recovery metadata without DOM/native coordinates or widget state.
- Web consumes the shared MCQ/IQS/PT/LRPT fixtures through semantic radio buttons, resource tabs, a textarea workspace, keyboard-native controls, local snapshot persistence, and narrow/wide responsive CSS.
- Native consumes the same fixture objects through accessible React Native `Pressable`/`TextInput` components, phone/tablet-responsive layout, unrestricted orientation, module-lifetime proof persistence, autosave, and background-transition save handling.
- Shared state tests prove MCQ reselection/review, IQS resource switching without answer loss, long-form drafting/formatting, save pending/failure/retry, serialization/restoration, and recovery of the last complete snapshot after an interrupted write.
- Every fixture is `TEST_FIXTURE` / `DEVELOPMENT_ONLY`, uses synthetic fictional text, and is hidden in production client environments. It never enters Django assessment inventory, curriculum, evidence, readiness, publication, grading, or analytics.
- No backend assessment model/endpoint, AI, grading, curriculum, learner evidence, recommendation, or production attempt system was added. The eventual Django API must serve this renderer-independent shape and own authoritative attempt versions in Milestones 3–4.
- Architectural conclusion: **yes**, one portable assessment presentation/state contract supports Web and React Native for MCQ, IQS, and long-form PT/LRPT without a second client-specific assessment model. Remaining risks concern production editor/storage libraries, richer editor behaviors, server autosave/concurrency/conflict semantics, and real-device accessibility/background/process recovery—not schema divergence.

## M2.1 immutable official-source and scope foundation
- `official_scope` owns immutable/versioned artifact provenance, original-byte SHA-256, artifact status/supersession, any-number source-to-scope roles, versioned canonical scope hashes, hierarchical official items/leaves, exact source locators, and bounded source-provenanced treatment metadata.
- Production scope coordinates are enforced as exactly national `NEXTGEN_UBE` / `NEXTGEN_CORE`. The file-fed importer performs no network acquisition, is idempotent, reports deterministic validation, defaults to no activation, and rejects state/jurisdiction scope through ordinary paths.
- Explicit activation transactionally requires valid current normalization and fixture/source/hierarchy invariants, then preserves prior active truth as immutable `SUPERSEDED` history. Django guards, relational constraints/`PROTECT`, and PostgreSQL triggers cover both normal and bulk mutation paths.
- Admin is inspection-only and the authenticated API exposes only the active version/checksum, suitable provenance, and portable hierarchy. All included source content is conspicuous synthetic `TEST_FIXTURE`; no official NCBE document bytes are committed and fixture truth is excluded from production activation/API.
- M2.2 must key Rule Obligation/compiler provenance to immutable scope-version/item identities. It must not mutate the official perimeter, treat secondary material as perimeter authority, or infer completeness from question counts. No Rule Obligation, doctrine graph, reconciliation, certification, production assessment inventory, learner evidence, or AI exists yet.

## M2.2a deterministic Rule Obligation compiler proof
- `curriculum` versions one exact M2.1 scope, compiler schema, input hash, canonical output, immutable fixture policy, lifecycle, and supersession chain. Eleven controlling obligation kinds, many-to-many leaf mapping, typed acyclic semantic relations, structured primary/secondary evidence, and deterministic decision outcomes are relational truth.
- Reconciliation produces machine-readable omission/excess/conflict/ambiguity/duplicate/provenance/jurisdiction/structure issues with blocking/warning/info severity and policy-based fixture coverage metrics. Secondary evidence never defines perimeter or substitutes for required primary authority.
- Staff-only review records issue, resolution, reviewer, time, rationale, and truth impact. Certification requires a fresh zero-blocking reconciliation and exact hashes, then transactionally preserves an immutable coverage snapshot; PostgreSQL triggers protect certified/superseded history and children.
- Synthetic `TEST_FIXTURE` scope, authority, obligations, issues, reviews, compiles, and snapshots are production-ineligible by default and hidden from the production API. No real NCBE document or production doctrine is present. This proves the integrity gate, not current real-source acquisition or national completeness.
- M2.2b should acquire/register real current official NCBE artifacts and a bounded substantive-authority pilot, define reviewed real-source coverage policy, and feed controlled candidates through this deterministic gate. It must not introduce AI or claim full production curriculum completeness prematurely.

## Tests actually run
- M2.2a exact-runtime local acceptance: a clean hash-verified Python 3.13.15 install passed Ruff, Django system/migration checks, 85 SQLite tests with eight PostgreSQL-only skips, all 93 tests against PostgreSQL 14, and the live Redis/Celery foundation smoke. The 12 focused deterministic compiler tests and two PostgreSQL-only curriculum integrity tests are included in those totals.
- Exact Node 24.19.0/npm 11.17.0 clean `npm ci` installed 717 packages. `npm run check` passed all nine typechecks, 14 Web tests, 20 native tests, 8 assessment-schema tests, and the production Web build; seven-package portability, live Expo compatibility, Doctor 20/20, and iOS/Android exports at 863/858 modules passed. The lockfile did not change.
- Current `npm audit --omit=dev` retains 15 aggregate paths in the same documented `image-size` and `uuid` toolchain families. Current advisory metadata reports 10 moderate/5 high rather than the earlier 7 moderate/8 high; dependencies, paths, reachability, and mitigation are unchanged, and no forced fix was run.
- M1.5 exact-runtime local acceptance on Node 24.19.0/npm 11.17.0: clean `npm ci` installed 717 packages; live Expo compatibility and Doctor 20/20 passed; all nine typechecks, 14 Web tests, 20 native tests, 8 shared schema/state tests, Web build, all seven portable packages, and iOS/Android exports at 863/858 modules passed. Ruff/Django/migration checks and 60 local backend tests passed with four PostgreSQL-only skips. Audit remained the accepted 15-node `image-size`/`uuid` graph. Exact-commit CI is pending push.
- Current M1.4 acceptance rerun on exact Node 24.19.0/npm 11.17.0: clean `npm ci` installed 717 packages; live Expo compatibility passed; Doctor passed 20/20; `npm run check` passed all nine typechecks, 9 Web tests, 18 native tests, and production Web build; seven-package portability and iOS/Android exports at 854/849 modules passed. Ruff lint/format, Django system/migration checks, and 60 local backend tests passed with four PostgreSQL-only skips. Exact-commit GitHub CI supplies the PostgreSQL/Redis/Celery acceptance path.
- Current read-only staging/EAS sanity: correct Heroku owner, Web/worker/beat, PostgreSQL/KVS, health/readiness, HTTPS/redirect, Web auth routes, anonymous auth enforcement, gated 404 association endpoints, EAS Owner project, and finished signed Android build all passed. No resource or credential changed.
- Earlier M1.4 audit evidence recorded the same 15 aggregate `image-size`/`uuid` toolchain paths as 7 moderate/8 high; the current M2.2a audit metadata redistribution is recorded above and in `SECURITY_ADVISORIES.md`.
- Accepted-main exact-sha Foundation CI runs `32416558206` and `32417562112` on `4850b78`: PASSED. Local/remote main matched exactly before this branch was created.
- Separate M1.4 exact-sha Foundation CI run `32423925699` on untouched commit `4c1d2e6`: PASSED.
- M1.4 pre-reconciliation final rerun on exact Node 24.19.0/npm 11.17.0: clean `npm ci`, all nine typechecks, 9 Web tests, 18 native tests, Web build, all seven portability packages, live Expo dependency validation, Doctor 20/20, and iOS/Android JS exports PASSED. Ruff lint/format, Django system/migration checks, and 60 local backend tests PASSED with four PostgreSQL-only skips. Android EAS internal build passed; iOS credential/build and both actual runtimes remain deferred Native GA gaps.
- Reconciled specification branch locally on Node 24.19.0/npm 11.17.0: clean `npm ci` installed 687 packages; live `CI=1 npx expo install --check` PASSED; Expo Doctor PASSED 20/20; `npm run check` PASSED all nine workspace typechecks, 4 Web tests, 13 native tests, and the Web production build; `npm run portability` PASSED all seven shared packages. Specification/continuity/search and diff checks are recorded in `TEST_LEDGER.md`.
- Accepted-main GitHub Actions run `32415566577` on `77d5567`: PASSED continuity, backend/PostgreSQL/Redis/Celery, TypeScript checks, live Expo dependency validation/Doctor, and iOS/Android exports.
- Web-first amendment GitHub Actions run `32413722581`: continuity PASSED; backend/PostgreSQL/Redis/Celery PASSED; TypeScript clean install, full check, and portability PASSED. The TypeScript job then FAILED `npx expo install --check` because Expo's live SDK 57 metadata advanced the recommended Expo patch from accepted-main 57.0.13 to 57.0.15. Doctor/exports were skipped after that failure. This is external baseline dependency drift, not a specification-diff failure, and remains outside this specification-only branch.
- M1.3a hardening: 48 SQLite security/lifecycle tests pass with four PostgreSQL-only skips; the complete 52-test PostgreSQL 14 + Redis 7.2 suite passes, including reset-vs-issuance in both lock orders, token consume-vs-reissue, and duplicate signup. Ruff/system/migration checks, npm full check/build and portability with 17 Vitest tests, Expo Doctor 20/20, iOS/Android production JS exports, continuity validation, and diff checks pass. Hosted Foundation CI also passes the exact-runtime continuity, backend/PostgreSQL/Redis/Celery, and TypeScript/Expo jobs.
- M1.3 local security/lifecycle suite: Ruff and Django checks PASSED; 25 Pytest tests PASSED on the available Python 3.11 SQLite path. `npm run check` and portability PASSED with four Web/native Vitest tests and production Web build; Expo dependency check, Doctor 20/20, and iOS/Android JS exports PASSED. Hosted exact-runtime PostgreSQL 17/Redis 7.2/Celery and Node 24 acceptance also PASSED on the pushed branch.
- `python3 scripts/validate_continuity.py` passes against the committed repository baseline and controlling-spec manifest.
- Clean hash-verified Python lock installation passes on exact Python 3.13.15; Django 5.2.17 system check and 2 health/readiness tests pass on isolated SQLite and on a temporary local PostgreSQL 14 cluster after applying all built-in migrations. CI uses Python 3.13.15 and PostgreSQL 17.
- Clean `npm ci`, ESLint, Prettier, all TypeScript workspace typechecks, three Vitest tests (including the ReactDOM mount), the portability gate, and the Vite production build pass on exact Node 24.19.0/npm 11.17.0.
- `npm ls react react-dom --all` resolves only React 19.2.3; the built web asset contains only that React patch marker.
- Expo dependency compatibility reports current, Expo Doctor passes 20/20, and iOS/Android production JS exports pass on exact Node 24.19.0. A signed Android internal APK now passes through EAS. Simulator/device execution remains unverified because full Xcode/simctl and Android SDK/adb/emulator are absent; iOS internal build/signing is also pending.
- Remaining npm audit findings are upstream Expo/React Native build/config-tool paths documented in `SECURITY_ADVISORIES.md`; no forced downgrade was applied.

## Providers actually verified
Heroku app runtime, Essential-0 PostgreSQL, and Mini KVS remain `VERIFIED_NONPRODUCTION`. Correct owner account `apollonomios@gmail.com` can inspect `barclimb-staging`; Web/worker/beat are up, PostgreSQL and KVS are available, public readiness is healthy, and Heroku reports no scheduled suspension or deletion. Expo/EAS project control and Android internal build/signing are verified nonproduction. Apple, Google Play, SendGrid, S3, OpenAI, Stripe, Sentry, and ad providers remain `NOT_VERIFIED`; no production-provider claim follows.

## Known risks
Execution breadth remains the principal engineering risk. Curriculum completeness depends on automated official-scope/rule compilation, authority provenance, lawful multi-source reconciliation, subject certification, and strict inventory gates. NCBE Sourcebooks are optional enhanced reconciliation when lawfully available; do not make purchase/access a build or launch dependency.

## Exact next task
Commit and push `m2-2a-rule-obligation-compiler-proof`, require green GitHub Actions on the exact branch SHA, and then stop for review. Do not merge automatically and do not begin M2.2b.

## Resume commands
```bash
python3 scripts/validate_continuity.py
cd apps/backend && ../../.venv/bin/ruff check . && ../../.venv/bin/python manage.py check --settings=config.settings.test && ../../.venv/bin/pytest
npm run check
npm run portability
npm run doctor --workspace @barclimb/native
```
Use Python 3.13.15, Node 24.19.0, and npm 11.17.0 for baseline parity. Install Python requirements with `--require-hashes`. See `../implementation/ENVIRONMENT.md` for setup and the PostgreSQL smoke path. Expo Doctor requires network access for all checks.

For backend acceptance, also run PostgreSQL and Redis/Valkey where available, select `config.settings.postgres_test`, and execute the PostgreSQL concurrency and worker paths documented in `../implementation/ENVIRONMENT.md`. Staging is real and persistent; do not expose config values or test production there. Native GA still requires the deferred platform-specific signed-build, actual-runtime, association, store, and purchase evidence.

## Final integration note
Before feature UI implementation, establish the canonical provider-agnostic billing domain, server projection schemas, orchestration models/state machines, and client-surface capability manifest. These prevent Visitor/Free/Plus and Web/iOS/Android from diverging.
