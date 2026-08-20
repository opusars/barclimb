# BarClimb Project Handoff

## Current state
Milestone 1 and M1.4 are in progress on `m1-4-staging-auth-client-proof` under accepted amended main. M1.4 has persistent verified-nonproduction Heroku/PostgreSQL/KVS staging, deployed Web auth/routes/outbox processes, React Navigation scaffolding, gated deep-link configuration, and verified owner access to the existing `@opusarss-team/barclimb` EAS project. It is not complete unless internal-build/signing and actual iOS/Android authentication/SecureStore evidence close the remaining gaps. No learner profile, onboarding, entitlement, curriculum, assessment, billing, or later product domain has been implemented.

The controlling release sequence is **Web GA → iOS Native GA → Android Native GA**, while architecture remains one first-class multi-client product from Milestone 1. Public native approval/release does not gate Web GA merely because incomplete, but M1.4 remains mandatory early native architecture insurance and M1.5 remains blocked.

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
- Forced portrait orientation removed. Proper native routing/deep links remain later Milestone 1 foundation work.

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
- The production-rejected staging email sink proves outbox processing without delivery or SendGrid verification. Heroku/Postgres/KVS is `VERIFIED_NONPRODUCTION`; every other provider remains `NOT_VERIFIED`.
- Expo/EAS login now verifies owner access to the existing `@opusarss-team/barclimb` project; the repository is durably linked to project ID `8ed30301-53d9-4630-b2c4-70d6d51f465b` without creating a duplicate.
- M1.4 remains incomplete: Apple team/bundle/signing and Android signing/recovery evidence and internal builds are pending, this host lacks full Xcode/simctl and Android SDK/adb/emulator, and no actual native/SecureStore runtime proof exists.

## Web-first release-strategy amendment
- Web GA is the first commercial/revenue release; iOS Native GA and Android Native GA follow as independent platform gates.
- Native public-store approval, production store purchase/restore, and public native release are not Web GA blockers merely because they are incomplete.
- Native remains active architecture insurance from Milestone 1: M1.4 risk proof, portable schemas/state, canonical URLs/deep-link contracts, provider-neutral entitlement, shared identity/curriculum/assessment/evidence/publication truth, and explicit capability/parity ledgers remain mandatory.
- The Web GA gate retains the anonymous SEO → substantive learning → Instant Practice → signup/claim, authenticated My BarClimb, and Plus ad-free/deeper-learning journeys.
- M1.5 may not begin until M1.4 is completed or explicitly re-scoped under the amended controlling specifications.

## Current branch coordination
- Accepted amended main `4850b78` is merged into this published branch without rebasing or rewriting history. Existing M1.4 implementation and evidence remain intact; current verification determines whether its external gaps can now close.
- M1.4 remains separate and unmerged from main. Do not begin M1.5 from this branch.

## Tests actually run
- Reconciled specification branch locally on Node 24.19.0/npm 11.17.0: clean `npm ci` installed 687 packages; live `CI=1 npx expo install --check` PASSED; Expo Doctor PASSED 20/20; `npm run check` PASSED all nine workspace typechecks, 4 Web tests, 13 native tests, and the Web production build; `npm run portability` PASSED all seven shared packages. Specification/continuity/search and diff checks are recorded in `TEST_LEDGER.md`.
- Accepted-main GitHub Actions run `32415566577` on `77d5567`: PASSED continuity, backend/PostgreSQL/Redis/Celery, TypeScript checks, live Expo dependency validation/Doctor, and iOS/Android exports.
- Web-first amendment GitHub Actions run `32413722581`: continuity PASSED; backend/PostgreSQL/Redis/Celery PASSED; TypeScript clean install, full check, and portability PASSED. The TypeScript job then FAILED `npx expo install --check` because Expo's live SDK 57 metadata advanced the recommended Expo patch from accepted-main 57.0.13 to 57.0.15. Doctor/exports were skipped after that failure. This is external baseline dependency drift, not a specification-diff failure, and remains outside this specification-only branch.
- M1.3a hardening: 48 SQLite security/lifecycle tests pass with four PostgreSQL-only skips; the complete 52-test PostgreSQL 14 + Redis 7.2 suite passes, including reset-vs-issuance in both lock orders, token consume-vs-reissue, and duplicate signup. Ruff/system/migration checks, npm full check/build and portability with 17 Vitest tests, Expo Doctor 20/20, iOS/Android production JS exports, continuity validation, and diff checks pass. Hosted Foundation CI also passes the exact-runtime continuity, backend/PostgreSQL/Redis/Celery, and TypeScript/Expo jobs.
- M1.3 local security/lifecycle suite: Ruff and Django checks PASSED; 25 Pytest tests PASSED on the available Python 3.11 SQLite path. `npm run check` and portability PASSED with four Web/native Vitest tests and production Web build; Expo dependency check, Doctor 20/20, and iOS/Android JS exports PASSED. Hosted exact-runtime PostgreSQL 17/Redis 7.2/Celery and Node 24 acceptance also PASSED on the pushed branch.
- `python3 scripts/validate_continuity.py` passes against the committed repository baseline and controlling-spec manifest.
- Clean hash-verified Python lock installation passes on exact Python 3.13.15; Django 5.2.17 system check and 2 health/readiness tests pass on isolated SQLite and on a temporary local PostgreSQL 14 cluster after applying all built-in migrations. CI uses Python 3.13.15 and PostgreSQL 17.
- Clean `npm ci`, ESLint, Prettier, all TypeScript workspace typechecks, three Vitest tests (including the ReactDOM mount), the portability gate, and the Vite production build pass on exact Node 24.19.0/npm 11.17.0.
- `npm ls react react-dom --all` resolves only React 19.2.3; the built web asset contains only that React patch marker.
- Expo dependency compatibility reports current, Expo Doctor passes 20/20, and iOS/Android production JS exports pass on exact Node 24.19.0. Simulator/device/store builds remain unverified because Xcode, Android SDK/adb, and EAS are not configured on this host.
- Remaining npm audit findings are upstream Expo/React Native build/config-tool paths documented in `SECURITY_ADVISORIES.md`; no forced downgrade was applied.

## Providers actually verified
Heroku app runtime, Essential-0 PostgreSQL, and Mini KVS remain `VERIFIED_NONPRODUCTION` from persistent staging evidence. Current public health/readiness remain healthy, but the authenticated Heroku account now receives `forbidden` and cannot inspect the app; ownership/collaborator access requires human restoration. Expo/EAS account and existing-project control are verified nonproduction. SendGrid, Apple signing, Google Play/signing, and all other providers remain `NOT_VERIFIED`.

## Known risks
Execution breadth remains the principal engineering risk. Curriculum completeness depends on automated official-scope/rule compilation, authority provenance, lawful multi-source reconciliation, subject certification, and strict inventory gates. NCBE Sourcebooks are optional enhanced reconciliation when lawfully available; do not make purchase/access a build or launch dependency.

## Exact next task
Complete M1.4 only: authenticate an authorized Expo/EAS account, verify Apple and Android project/signing/recovery ownership, produce both internal builds, exercise staging auth and SecureStore on actual iOS and Android runtimes, and record the platform-specific evidence. GitHub Actions run `31895608020` is green on commit `0be3789`. Do not begin M1.5 or any product domain.

## Resume commands
```bash
python3 scripts/validate_continuity.py
cd apps/backend && ../../.venv/bin/ruff check . && ../../.venv/bin/python manage.py check --settings=config.settings.test && ../../.venv/bin/pytest
npm run check
npm run portability
npm run doctor --workspace @barclimb/native
```
Use Python 3.13.15, Node 24.19.0, and npm 11.17.0 for baseline parity. Install Python requirements with `--require-hashes`. See `../implementation/ENVIRONMENT.md` for setup and the PostgreSQL smoke path. Expo Doctor requires network access for all checks.

For backend acceptance, also run PostgreSQL and Redis/Valkey, select `config.settings.postgres_test`, and execute the PostgreSQL concurrency and worker paths documented in `../implementation/ENVIRONMENT.md`. Staging is real and persistent; do not expose config values or test production there. Native acceptance still requires internal builds and actual platform runtimes.

## Final integration note
Before feature UI implementation, establish the canonical provider-agnostic billing domain, server projection schemas, orchestration models/state machines, and client-surface capability manifest. These prevent Visitor/Free/Plus and Web/iOS/Android from diverging.
