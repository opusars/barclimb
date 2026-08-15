# BarClimb Test Ledger

| Date | Scope | Environment | Command / Method | Result | Notes |
|---|---|---|---|---|---|
| 2026-08-12 | Continuity bootstrap | local artifact | `python3 scripts/validate_continuity.py` | PASSED | No application tests exist yet. |
## 2026-08-13 — Pre-build specification checks
- Verified four controlling Markdown specs are present and rehashed in `SPEC_MANIFEST.json`.
- Checked Build Constitution numbered headings for duplicate milestone/section numbers after milestone revision.
- Checked for stale “all nine milestone” / old Milestone 9 hardening language.
- Continuity validator must pass on the regenerated bootstrap before delivery.
- Added consistency requirement that release coverage counts only independently confirmed AssessmentScopeTargets, not GenerationSpecification tags alone.

## 2026-08-13 — Repository continuity reconciliation
- Ran `python3 scripts/validate_continuity.py`: PASSED.
- Verified `PROJECT_STATE.json` parses and records the actual baseline branch/commit.
- Verified all four controlling specifications remain present and manifest hashes match.
- Searched continuity/specification text for stale pre-kickoff initialization instructions, obsolete `python` validator invocations, and contradictory v1 jurisdiction requirements.
- Reviewed the final documentation-only diff; no application files or provider/toolchain setup were introduced.

## 2026-08-13 — M1.1 foundation verification
- `python3 scripts/validate_continuity.py`: PASSED.
- `.venv/bin/ruff check apps/backend`: PASSED; formatting check clean after scoped formatting.
- `DJANGO_SETTINGS_MODULE=config.settings.test .venv/bin/python apps/backend/manage.py check`: PASSED.
- `cd apps/backend && ../../.venv/bin/pytest`: PASSED, 2 tests (health and database readiness) on Python 3.11.2/Django 5.2.16.
- `npm run lint`: PASSED.
- `npm run typecheck`: PASSED for web, native, and all seven shared packages.
- `npm test`: PASSED, 2 Vitest smoke tests.
- `npm run build`: PASSED, Vite production bundle generated.
- `CI=1 npx expo export --platform ios`: PASSED, 575 modules bundled.
- `CI=1 npx expo export --platform android`: PASSED, 573 modules bundled.
- `npx expo install --check --json`: PASSED (`upToDate: true`).
- `npm run doctor --workspace @barclimb/native`: 16/17 locally; network-enabled package metadata check remains affected by unsupported host Node 23.1. CI targets supported Node 22.13. No simulator/device build was claimed.
- `npm audit --omit=dev`: 0 critical, 11 high, 7 moderate findings, all in the Expo/React Native toolchain graph; npm's offered fix incorrectly downgrades to Expo 53/React Native 0.72 and was not applied. Reassess with upstream SDK updates.

## 2026-08-13 — M1.1a correction verification
- Exact JavaScript runtime: Node 24.19.0 and npm 11.17.0 verified from the official Node distribution. Clean `npm ci`: PASSED; no unreviewed install scripts after pinned `esbuild@0.28.2` and `fsevents@2.3.3` review.
- `npm ls react react-dom --all`: PASSED; every resolved instance is React 19.2.3 and ReactDOM 19.2.3 is deduped. Web production bundle inspection found only the `19.2.3` React patch marker.
- `npm run check`: PASSED on Node 24.19.0/npm 11.17.0. Prettier, ESLint, all nine workspace typechecks, two web tests (including a real ReactDOM root-shell mount), one native smoke test, and Vite 7.3.6 production build passed.
- `npm run portability`: PASSED for all seven shared packages. An ESLint stdin negative probe importing `node:fs` at a shared-package path failed as expected with `no-restricted-imports`.
- `npx expo install --check`: PASSED; TypeScript 5.9.3 was explicitly skipped through `expo.install.exclude`, and all Expo SDK 57 dependencies were current.
- `npm run doctor --workspace @barclimb/native`: PASSED 20/20 with network access on Node 24.19.0.
- Expo SDK 57.0.12 production JS exports: PASSED for iOS (580 modules) and Android (578 modules). These are bundle exports, not simulator/device/store builds.
- Clean Python 3.13.15 hash-lock install: PASSED from `requirements-dev.txt`; exact packages include Django 5.2.17. Both locks were generated with pip-tools 7.6.1 under Python 3.13.15 and matched the prior candidates byte-for-byte.
- Python foundation checks: Ruff lint/format PASSED; Django SQLite system check PASSED; 2 health/readiness tests PASSED on Python 3.13.15/Django 5.2.17.
- PostgreSQL smoke: PASSED against a temporary local PostgreSQL 14 cluster on port 55432. Django system check passed, all built-in auth/contenttypes/sessions migrations applied, and 2 health/readiness tests passed with `config.settings.postgres_test`. The cluster was stopped afterward. CI targets PostgreSQL 17.
- `npm audit`: directly actionable Vite/Vitest findings were patched. `npm audit --omit=dev` retains 18 aggregate upstream Expo/React Native toolchain nodes (7 moderate, 11 high) rooted in `image-size` and `uuid`; reachability and mitigations are recorded in `SECURITY_ADVISORIES.md`.
- `python3 scripts/validate_continuity.py`: PASSED after continuity reconciliation. `git diff --check`: PASSED. Controlling specifications and `SPEC_MANIFEST.json` were unchanged.
- Native simulator/device/store build: NOT VERIFIED. Full Xcode is absent; Android SDK/adb and EAS are not configured.

## 2026-08-13 — M1.2 runtime/environment verification
- Clean Python 3.13.15 `pip --require-hashes` install from regenerated pip-tools 7.6.1 locks: PASSED; Celery 5.6.3 and Redis client 6.4.0 resolved.
- Ruff lint/format, Django test-settings system check, and 9 SQLite deterministic tests: PASSED. Coverage includes malformed environment values, HTTPS-origin validation, missing production configuration, eager Celery discovery/execution, and required-KVS readiness failure.
- Temporary PostgreSQL 14 + Redis 7.2 integration: migrations PASSED; 9 tests PASSED through `config.settings.postgres_test`; readiness reported database/KVS round trips healthy.
- Live Celery 5.6.3 solo worker against Redis 7.2: PASSED. Worker loaded Django configuration, reported `results: disabled`, discovered only `infrastructure.smoke`, and executed the published task successfully.
- `npm run check`: PASSED; Prettier, ESLint, all workspace typechecks, 3 Vitest tests, and Vite production build passed.
- `npm run portability`: PASSED for all seven shared packages.
- `python3 scripts/validate_continuity.py`: PASSED. `git diff --check`: PASSED. Four controlling specs and manifest remained unchanged.
- CI workflow now includes PostgreSQL 17, Redis 7.2, backend integration tests, and live worker smoke; GitHub Actions result pending branch push.

## 2026-08-13 — M1.3 identity/authentication verification
- Local SQLite path on the available Python 3.11 host: Django system check and 25 Pytest tests PASSED. Identity coverage includes user creation, deterministic email/username normalization and uniqueness, reserved-name rejection, password hashing/authentication, Web CSRF failure/success, session rotation, authenticated lookup, logout invalidation, generic reset responses, weak-password rollback, expiring/purpose-bound/rotating/single-use token behavior, password reset and native-session revocation, native signup/login/restoration/expiry/revocation, auth throttling, no-store private responses, deployed email fail-closed behavior, anonymous denial, and cross-user ownership rejection.
- Production-settings subprocess test PASSED for HTTPS redirect, HSTS, secure/HttpOnly session and CSRF cookies; missing mandatory production configuration still fails closed.
- `npm run check` and `npm run portability`: PASSED after updating the Web shell test; Prettier, ESLint, all workspace typechecks, four Web/native Vitest tests, and Vite build. Native SecureStore wrapper testing proves opaque-token save/restore/delete behavior through an injected platform-storage boundary.
- `npx expo install --check`: PASSED with Expo SecureStore 57.0.1 current for SDK 57. Expo Doctor: PASSED 20/20 with network access. Local production JS exports PASSED for iOS (584 modules) and Android (582 modules); these are bundles, not simulator/device/store builds.
- `npm audit --omit=dev`: unchanged 18 aggregate upstream Expo/React Native toolchain findings (7 moderate, 11 high) from the two documented `image-size`/`uuid` sources; the offered incompatible Expo 53 downgrade was not applied.
- GitHub Foundation CI: PASSED all continuity, backend, and TypeScript jobs on the pushed M1.3 branch. The backend job used exact Python 3.13.15 with PostgreSQL 17 + Redis 7.2, applied the custom-user migration, passed all 25 tests, and passed live Celery worker smoke. The TypeScript job used Node 24.19.0, clean `npm ci`, full checks/portability, Expo compatibility/Doctor, and iOS/Android production JS exports. Local device/simulator keychain behavior and real transactional-email delivery remain unverified.

## 2026-08-13 — M1.3a authentication-boundary verification
- `.venv/bin/ruff check apps/backend`: PASSED. `manage.py makemigrations --check --dry-run --settings=config.settings.test`: PASSED, no model/migration drift.
- `.venv/bin/python -m pytest apps/backend/tests -q`: PASSED, 48 tests; four PostgreSQL-only concurrency tests skipped by design. Coverage includes query-free canonical-Web links, POST-only completion, Web-session and multi-device reset invalidation, Bearer variants, Heroku IPv4/IPv6/forged-chain handling, casing-resistant throttles, KVS generic fail-closed behavior, durable outbox publication/retry/duplicate/lease/key-rotation recovery, and HTTPS redirect/forwarding behavior.
- Temporary PostgreSQL 14 + Redis 7.2 authoritative run through `config.settings.postgres_test`: PASSED, all 52 backend tests. Both native-login/reset lock orders, token consume/reissue serialization, and duplicate-signup uniqueness raced in separate database connections; durable outbox worker locking/retry also ran under PostgreSQL semantics. Both temporary services were stopped afterward.
- `npm run lint`, `npm run typecheck`, and `npm test`: PASSED. Web has four Vitest tests including both fragment completion routes/history cleanup; native has 13 tests including authoritative rejection, offline/5xx preservation, SecureStore read/write/delete failures, server-revocation outcomes, and successful restoration/logout.
- `npm run check`: PASSED; Prettier, ESLint, all workspace typechecks, 17 Web/native Vitest tests, and the Vite production build passed. `npm run portability`: PASSED for all seven shared packages.
- Expo Doctor: PASSED 20/20. Dependency check reported current from the bundled offline map (TypeScript remains intentionally excluded). Fresh production JS exports PASSED for iOS (584 modules) and Android (582 modules); these remain bundle proofs, not simulator/device/store builds.
- `python3 scripts/validate_continuity.py`: PASSED. `git diff --check`: PASSED. The four controlling specs and `SPEC_MANIFEST.json` remain unchanged.
- Hosted Foundation CI: PASSED continuity, backend, and TypeScript jobs. The backend job used Python 3.13.15, PostgreSQL 17, Redis 7.2, hash-locked dependencies, Ruff lint/format, migrations, all 52 tests, and live Celery worker smoke. The TypeScript job used Node 24.19.0, clean `npm ci`, full checks/portability, Expo dependency/Doctor checks, and iOS/Android exports. Real Heroku routing/proxy headers, real transactional-email provider delivery/idempotency, native device SecureStore/keychain behavior, universal/app links, and simulator/store builds remain unverified.

## 2026-08-15 — Accepted-main Expo patch continuity correction
- Expo authority: `npx expo install --fix --npm` selected direct `expo@~57.0.13`; subsequent CI-mode dependency validation reported `Dependencies are up to date`. React Native remained 0.86.2 and TypeScript remained 5.9.3 under `expo.install.exclude`.
- Exact-runtime install: clean `npm ci` PASSED under Node 24.19.0/npm 11.17.0; 687 packages installed from the regenerated lock.
- Expo Doctor: PASSED 20/20. iOS production export PASSED (585 modules); Android production export PASSED (583 modules). These remain bundle exports, not device/store builds.
- `npm run check`: PASSED, including Prettier, ESLint, all workspace typechecks, 4 Web tests, 13 native tests, and the Vite production build. `npm run portability`: PASSED for all seven shared packages.
- Backend regression: Ruff lint/format and Django system check PASSED; 48 SQLite tests PASSED with four PostgreSQL-only concurrency tests skipped by design. The dependency-only correction does not alter backend dependencies or behavior.
- `npm audit --omit=dev`: unchanged 18 aggregate nodes (7 moderate, 11 high) rooted in the same `image-size` and `uuid` upstream toolchain advisories; Expo-owned path versions were refreshed in `SECURITY_ADVISORIES.md`. No forced/incompatible fix was applied.
- Continuity validation and `git diff --check`: PASSED locally. Controlling specifications and `SPEC_MANIFEST.json` remain unchanged. Hosted Foundation CI on the exact correction commit is the remaining acceptance observation at commit time.

## 2026-08-15 — M1.4 staging/auth/client proof (in progress)
- Preflight: clean accepted `main` at `fa476bff604578c0825a70db61b1d5ef7dee3b2d`, equal to `origin/main`; GitHub Actions run `31892309877` passed all three jobs. Continuity validation passed before the slice.
- Exact Node 24.19.0/npm 11.17.0 clean dependency install passed after lock regeneration. Expo-compatible `react-native-safe-area-context@5.7.0` and `react-native-screens@4.26.2` resolve once each. `CI=1 npx expo install --check` reported current; Expo Doctor passed 20/20 with network.
- `npm run check`: PASSED with all nine workspace typechecks, lint/format, 9 Web tests, 18 native tests, and production Web build. `npm run portability`: PASSED. iOS export passed at 854 modules; Android export passed at 849 modules. These remain JS bundle proofs, not internal builds.
- Backend Ruff lint/format: PASSED. SQLite test suite: 60 passed, 4 PostgreSQL-only tests skipped. New coverage includes deployed-environment validation, staging sink safety, direct Web routes/assets, association publication gating, environment selection, and canonical-link credential redaction.
- Heroku release v8 deployed commit `6bec558`: Node 24.19.0/npm 11.17.0 Web build, Python 3.13.15 hash-locked install, collectstatic, deployment check, and migrations passed. Web, worker, and beat each ran one Basic dyno.
- `GET /api/v1/health/`: 200. `GET /api/v1/ready/`: 200 with database and KVS both `ok`. Direct HTTP root returned 301 to HTTPS; HTTPS root/auth destinations returned 200. Direct/refresh routes verified: login, signup, verify-email, forgot-password, reset-password, and app.
- Controlled Web proof: signup 201, authenticated session true, login 200, authenticated session true. The first scripted logout used the pre-login CSRF token and correctly failed 403 after Django rotated the CSRF secret; automated local logout-rotation coverage remains green.
- Proxy/rate-limit proof: 11 native-login failures used 11 different caller-supplied `X-Forwarded-For` values and unique identities. Results were ten 400 responses followed by 429, proving the Heroku-appended rightmost address—not caller-prepended spoof values—owned the shared IP counter.
- Native API proof: staging issued a bearer for a generated account, accepted revocation with 204, then returned 401. One controlled diagnostic printed that test bearer; it was immediately revoked before further work. This is backend protocol evidence, not native-client/runtime evidence.
- Outbox proof: staging aggregate showed one verification delivery in `SENT`. Logs showed beat publishing the one-minute recovery task, worker pickup/success, delivery-task pickup, and `staging auth email accepted action=/verify-email`. A 1,500-line app-log scan found zero fragment/query-token, Authorization, Bearer, or password-shaped credential patterns.
- Universal/App Link endpoints returned 404 on staging because `MOBILE_LINKS_ENABLED=false`; unit tests prove the gated payload shape and auth-route exclusion. No OS/domain association is claimed.
- Local platform probe: `xcodebuild` reports only Command Line Tools; `simctl` is unavailable; Android SDK, `adb`, and emulator are absent. EAS `whoami` reported `Not logged in`; final noninteractive iOS and Android internal-build attempts both stopped with `An Expo user account is required`. Internal builds, simulator/emulator/device auth, and actual SecureStore read/write/delete/restart/uninstall behavior are NOT VERIFIED.
- `npm audit --omit=dev`: 18 aggregate nodes (7 moderate, 11 high), unchanged from the documented `image-size` and `uuid` upstream toolchain roots; no compatible fix appeared. Final clean `npm ci`, full checks/portability, Expo validation, Doctor 20/20, both exports, 60 backend tests, continuity validation, and diff checks passed.
- GitHub Foundation CI run `31895220658`: PASSED on exact commit `68ef81a2d4ec7cdbfb4290c046c221ad9d0f2016`. Continuity passed; backend used PostgreSQL 17 + Redis 7.2, passed all 64 tests and live Celery smoke; TypeScript used Node 24.19.0/npm 11.17.0 and passed clean install, full checks/portability, Expo validation/Doctor, and both JS exports.
