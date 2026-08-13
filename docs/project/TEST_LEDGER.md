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
