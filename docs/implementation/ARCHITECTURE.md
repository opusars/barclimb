# M1.1 Repository Architecture

The repository is an npm-workspace monorepo around one server-authoritative Django backend.

```text
apps/backend/   Django + DRF API
apps/web/       React + TypeScript DOM client
apps/native/    Expo + React Native TypeScript client for iOS/Android
packages/       Platform-neutral TypeScript contracts and tokens
scripts/        Repository tooling and continuity validation
docs/specs/     Four controlling product specifications
docs/project/   Continuity state and ledgers
```

Web and native own their presentation code. Shared packages are limited to portable API helpers, types, schema boundaries, tokens, validation, analytics envelopes, and feature-flag shapes. They contain no client-authoritative learner, entitlement, or assessment logic.

Portable packages compile against the ES2022 library only, with ambient runtime types disabled. ESLint rejects DOM/Node globals, Node built-ins, and React/React Native renderer imports in `packages/*`. Web and native receive separate lint environments. Package source remains directly consumable by the current bundlers; a compiled-output contract is deferred until a non-bundler consumer requires one.

The native shell's destination buttons are an M1.1 proof surface, not completed navigation parity. Proper routing and universal/app-link handling remain later Milestone 1 native-foundation work before feature UI. Native orientation is intentionally unrestricted for future phone/tablet and PT/LRPT layouts.

M1.1 creates infrastructure boundaries only. It does not implement business domains, authentication, learner state, assessment schemas, providers, or deployment.

## M1.2 asynchronous/runtime boundary

Django remains the authoritative server and PostgreSQL the sole canonical durable datastore. Celery is loaded through Django, uses an environment-driven Redis/Valkey-compatible broker, discovers registered tasks, and deliberately has no result backend. The only task in this slice is `infrastructure.smoke`, a non-contractual execution probe.

The same KVS endpoint backs Django's cache and Celery coordination. It is strictly ephemeral: a cache flush or broker loss may delay/repeat safe work but may not lose or change durable business truth. Future tasks must be idempotent at PostgreSQL/domain boundaries rather than relying on broker delivery semantics.

Local/test/review/staging/production settings share a typed environment contract. Liveness is dependency-free; readiness checks PostgreSQL plus required KVS connectivity. Heroku topology is web + worker + release, with no beat process until scheduled work actually exists.
