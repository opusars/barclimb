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

M1.4 replaces the original native destination-button proof with React Navigation: an unauthenticated native-stack boundary and an authenticated bottom-tab shell. Practice, Simulate, and Progress are navigation-only placeholders; their product behavior remains out of scope. Canonical-link resolution is separated from navigation, and verified OS association data deliberately excludes credential-bearing verification/reset routes. Native orientation remains unrestricted for future phone/tablet and PT/LRPT layouts.

M1.1 creates infrastructure boundaries only. It does not implement business domains, authentication, learner state, assessment schemas, providers, or deployment.

## M1.2 asynchronous/runtime boundary

Django remains the authoritative server and PostgreSQL the sole canonical durable datastore. Celery is loaded through Django, uses an environment-driven Redis/Valkey-compatible broker, discovers registered tasks, and deliberately has no result backend. M1.2 initially introduced only `infrastructure.smoke`, a non-contractual execution probe. M1.3a adds the first scoped business tasks for durable authentication-email delivery and outbox recovery.

The same KVS endpoint backs Django's cache and Celery coordination. It is strictly ephemeral: a cache flush or broker loss may delay/repeat safe work but may not lose or change durable business truth. Future tasks must be idempotent at PostgreSQL/domain boundaries rather than relying on broker delivery semantics.

Local/test/review/staging/production settings share a typed environment contract. Liveness is dependency-free; readiness checks PostgreSQL plus required KVS connectivity. M1.2 established Heroku web + worker + release with no speculative scheduler; M1.3a adds beat for the now-concrete authentication-email outbox recovery schedule.

## M1.3/M1.3a identity boundary

The first application model is a deliberately minimal custom Django user shared by Web/iOS/Android. Email is private login authority; username is the future public identity; passwords remain exclusively in Django's password framework. Browser auth is same-origin Django session plus CSRF. Native auth is a revocable, expiring opaque credential stored with Expo SecureStore; PostgreSQL stores only its digest and lifecycle. See `AUTHENTICATION.md` for endpoints and security behavior.

M1.3a hardens that boundary with user-row/authentication-generation serialization across native issuance and reset, query-free Web-fragment action handoff, a PostgreSQL authentication-email outbox, HTTPS/proxy trust in every deployed environment, and recoverable native SecureStore states. PostgreSQL is authoritative for users, session generations, action tokens, and delivery lifecycle; Redis supports hashed auth-rate counters and broker coordination only. Identity still contains no learner profile, jurisdiction, entitlement, curriculum, analytics, preferences, or community state. Free/Plus and future role semantics remain outside M1.3a.

## M1.4 client and staging proof boundary

The deployed Web client is built once and served by Django/Gunicorn from \`apps/web/dist\`; \`/api/v1\` remains same-origin. Browser routing owns stable signup, login, verification, reset-request, reset-completion, and authenticated-proof paths, and Django returns the same client entry document for direct requests or refreshes. Immutable hashed assets are cached independently from the noncached entry document.

Native environment selection is fail-closed: local has isolated HTTP defaults, while staging/production require explicit HTTPS API and canonical Web origins. Environment-specific application IDs prevent a staging build from replacing production. Expo SDK 57's compatible \`react-native-safe-area-context\` and \`react-native-screens\` versions are root-overridden only to prevent npm workspace peer auto-installation from creating duplicate native modules.
