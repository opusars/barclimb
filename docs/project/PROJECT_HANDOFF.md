# BarClimb Project Handoff

## Current state
Milestone 1 is in progress. M1.1 established the multi-client repository and toolchain foundation: a minimal Django/DRF backend, React web shell, Expo React Native shell, platform-neutral TypeScript packages, repeatable checks, and foundation CI. No BarClimb business domain, authentication, provider integration, or deployment behavior has been implemented.

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

## Completed in M1.1
- npm-workspace monorepo boundaries for `apps/backend`, `apps/web`, `apps/native`, and seven shared TypeScript packages.
- Django 5.2/DRF 3.16 environment-separated settings with PostgreSQL as the real-environment contract and SQLite isolated to foundation tests.
- Versioned `/api/v1/health/` and database-backed `/api/v1/ready/` endpoints with automated tests.
- React 19.2/Vite web proof shell and Expo SDK 55/React Native 0.83 native proof shell with Home/Practice/Simulate/Progress navigation placeholders.
- Python lint/test and TypeScript format/lint/typecheck/test/build commands plus GitHub Actions foundation CI.
- Implementation-facing architecture and environment/setup documentation.

## Tests actually run
- `python3 scripts/validate_continuity.py` passes against the committed repository baseline and controlling-spec manifest.
- Django system check passes and 2 health/readiness tests pass on local Python 3.11.2; production/CI remains pinned to Python 3.13.
- Ruff, ESLint, all TypeScript workspace typechecks, 2 Vitest smoke tests, and the Vite production build pass.
- Expo iOS and Android production bundle exports pass and `expo install --check --json` reports the SDK dependency set current.
- Full Expo Doctor passes 16/17 locally; the remaining package-meta check is affected by the unsupported host Node 23.1 runtime. CI is pinned to supported Node 22.13. Simulator/device launch has not been verified.

## Providers actually verified
None yet in an implementation environment. Do not infer provider readiness from product specs.

## Known risks
Execution breadth remains the principal engineering risk. Curriculum completeness depends on automated official-scope/rule compilation, authority provenance, lawful multi-source reconciliation, subject certification, and strict inventory gates. NCBE Sourcebooks are optional enhanced reconciliation when lawfully available; do not make purchase/access a build or launch dependency.

## Exact next task
Execute **M1.2 — runtime and environment foundation**: add the specification-required Celery/managed-KVS skeleton and local/review/staging runtime pipeline. Keep business tasks, authentication, providers, and later product features out of that slice.

## Resume commands
```bash
python3 scripts/validate_continuity.py
cd apps/backend && ../../.venv/bin/ruff check . && ../../.venv/bin/python manage.py check --settings=config.settings.test && ../../.venv/bin/pytest
npm run check
npm run doctor --workspace @barclimb/native
```
Use Python 3.13 and Node 22.13 for baseline parity. See `../implementation/ENVIRONMENT.md` for setup. Expo Doctor requires network access for all checks.

## Final integration note
Before feature UI implementation, establish the canonical provider-agnostic billing domain, server projection schemas, orchestration models/state machines, and client-surface capability manifest. These prevent Visitor/Free/Plus and Web/iOS/Android from diverging.
