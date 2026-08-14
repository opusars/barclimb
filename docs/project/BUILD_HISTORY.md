# BarClimb Build History

## 2026-08-12 — Pre-kickoff specification and continuity baseline
- Consolidated controlling specification set to four document families.
- Locked NextGen-only v1, learning network, Web+iOS+Android launch, complete official-scope coverage, and cross-platform commerce/moderation requirements.
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
- Corrected stale nine-milestone/web-first and old pricing/permission language in the master Constitution.
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
