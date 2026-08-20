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

## M1.5 portable assessment presentation proof

M1.5 answers the remaining Milestone 1 renderer-risk question affirmatively: one portable assessment presentation and workspace-state contract can support React Web and React Native for standalone MCQ, IQS, Standard PT, and Legal Research PT without a second client-specific assessment model.

`@barclimb/assessment-schema` now owns the JSON-serializable proof contract:

- canonical assessment family, response type, resource type, layout, navigation, capability, and registered-component identifiers;
- stable assessment/version, unit, choice, and resource identities;
- plain structured prompt/resource content—never arbitrary HTML or WebView instructions;
- portable choice/text responses, current unit/resource/view, review flags, inline formatting ranges, paragraph/list style, and indent level;
- explicit `UNSAVED_LOCAL`, `SAVE_PENDING`, `SAVED`, `RECOVERABLE_FAILURE`, and `RESTORED` persistence states; and
- runtime validation plus typed `UNSUPPORTED_COMPONENT` failures before rendering.

Web maps the two proof components to a semantic DOM radio group and textarea/resource workspace. React Native maps the same identifiers to accessible `Pressable` radio rows and a native multiline `TextInput` workspace. The two clients share no visual components and do not share React state; they consume the same schema, fixtures, registry semantics, state transitions, serialization, and persistence interface. Shared-package linting continues to reject DOM, React, and React Native dependencies.

The deterministic fixtures are marked `TEST_FIXTURE` and `DEVELOPMENT_ONLY`, contain synthetic fictional text, and are hidden in production client environments. They are not Django assessment records, corpus inventory, publications, learner evidence, grading input, or readiness input. No backend assessment endpoint/model was added because separately revalidating TypeScript fixtures in a temporary Python endpoint would create a second schema authority rather than prove the eventual API. Milestone 3 remains responsible for a server-owned presentation payload and structural validation against this portable boundary.

The persistence adapter is deliberately replaceable. Web uses local storage for the nonproduction proof; native uses a module-lifetime memory adapter plus background-transition save architecture. Automated tests prove component-remount restoration and last-complete-snapshot recovery after an interrupted write. They do not define production optimistic concurrency, cross-device conflict semantics, server attempt versions, encrypted durable native response storage, or process-kill/device behavior.

Remaining implementation risks are concrete rather than architectural blockers: selecting a production-grade editor/storage implementation; multi-block formatting, undo/redo, paste normalization, spellcheck, and keyboard ergonomics; server-authoritative autosave/idempotency/conflict behavior; highlighting/elimination/notepad/timer completeness; and physical-device accessibility/background/process-recovery evidence. Those remain Milestones 3–4 and the applicable Native GA work. The M1.5 proof does not grade, generate, publish, recommend, or create learner evidence.
