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
