# BarClimb Release Notes

No production application release yet. M1.4 has a non-production Heroku staging release only.

- Pre-build specs hardened for canonical Visitor/Free/Plus architecture, server projections, orchestration models, and cross-client parity.
- Repository continuity reconciled after kickoff; v1 jurisdiction behavior clarified and Milestone 1 marked ready to begin.
- M1.1 repository/toolchain foundation added for Django/DRF, React web, Expo iOS/Android, shared TypeScript packages, and CI. No application release or business feature is included.
- M1.1a corrected that foundation to Node 24/npm 11, Django 5.2.17, one React 19.2.3 web runtime, Expo 57/RN 0.86 with TypeScript 5, deterministic Python locks, PostgreSQL-backed CI, portable-package enforcement, and documented upstream toolchain advisories. No application release or business feature is included.
- M1.2 adds Celery/Redis-Valkey runtime wiring, explicit environment contracts, Heroku process definitions, PostgreSQL+KVS readiness, structured logs, deterministic eager tests, and real worker proof. No deployment, managed provider verification, business task, or product feature is included.
- M1.3 adds the shared custom account identity, Web session/CSRF flows, provider-neutral verification/reset lifecycle, revocable native sessions with Expo SecureStore, auth throttles/permissions, and Web/iOS/Android auth proof surfaces. No learner profile, onboarding, entitlement, curriculum, assessment, billing, or provider verification is included.
- M1.3a hardens that identity slice with query-free action links, canonical Web/API origin separation, reset-safe native authentication generations, deployed HTTPS/proxy rules, a durable PostgreSQL email outbox with scheduled recovery, and deterministic native SecureStore failure states. No application release, product domain, provider verification, or M1.4 work is included.
- M1.4 (in progress) adds stable Web auth routes, React Navigation auth/app boundaries, safe environment-specific client configuration, gated Universal/App Link scaffolding, and a production-rejected staging email sink. Persistent Heroku staging with managed PostgreSQL/KVS and Web/worker/beat is verified nonproduction. Internal native builds and actual iOS/Android SecureStore/auth runtime proof remain externally blocked, so M1.4 and Milestone 1 are not complete.
