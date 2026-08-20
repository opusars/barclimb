# BarClimb Provider Status

Secret values must never be committed here. Status is service-specific and evidence-gated.

M1.2 verified local PostgreSQL 14 and Redis 7.2 behavior and adds equivalent PostgreSQL 17/Redis 7.2 CI services. These are dependency/runtime proofs, not verification of a Heroku app, Heroku Postgres plan, or managed KVS add-on; the provider status therefore remains unchanged.

M1.3 exercises Django console/in-memory email delivery behind a provider-neutral boundary. This does not verify SendGrid or any other transactional-email provider, so provider statuses remain unchanged.

M1.4 verifies the Heroku runtime, Essential-0 PostgreSQL add-on `postgresql-aerodynamic-56880`, and Mini KVS add-on `redis-flat-93728` in persistent non-production staging app `barclimb-staging` (deployed commit `6bec558`; code release v8; current post-rotation configuration release v12). Release migrations, Web/worker/beat processes, PostgreSQL and TLS KVS round trips, readiness, HTTPS, auth throttling, and durable outbox execution all succeeded. This is `VERIFIED_NONPRODUCTION`, not production readiness. The Heroku account displayed a delinquent-payment warning with a stated suspension date of 2026-08-18; payment/account standing is an external continuity risk.

On 2026-08-20 the public staging origin still returned 200 for health/readiness with database and KVS `ok`, HTTPS root 200, and HTTP→HTTPS 301. However, the currently authenticated Heroku account received `forbidden` for `barclimb-staging` and the app was absent from its app list. Historical provider proof remains valid, but current account/process control is blocked until ownership/collaborator access is restored; no replacement app was created.

Expo authentication now verifies Owner role on both `opusars` and `opusarss-team`; the repository is linked to the pre-existing `@opusarss-team/barclimb` project ID `8ed30301-53d9-4630-b2c4-70d6d51f465b`. This proves Expo account/project control only, not Apple/Android signing, internal builds, OS runtime, store, or production readiness.

Release relevance is gate-specific. Apple/Google store approval and native production billing are Native GA blockers, not Web GA blockers merely because incomplete. Stripe is a Web GA commerce dependency but never canonical entitlement truth; Apple and Google purchase lifecycles must later map into the same Django Subscription/Entitlement domain.

| Provider | Intended role | Current status | Real nonprod verification | Launch relevance |
|---|---|---|---|---|
| OpenAI | generation/grading/compiler | NOT_VERIFIED | none | Web GA blocker by assessment milestone |
| Stripe | Web subscription purchase source | NOT_VERIFIED | none | Web GA paid-flow blocker; not entitlement truth |
| Apple | iOS distribution/IAP purchase source | NOT_VERIFIED | Expo project owned; no Apple team/bundle/signing evidence yet | iOS Native GA blocker; not a Web GA blocker by itself |
| Google Play | Android distribution/billing purchase source | NOT_VERIFIED | Expo project owned; no Android signing/Play evidence yet | Android Native GA blocker; not a Web GA blocker by itself |
| Expo/EAS | native project/build orchestration | VERIFIED_NONPRODUCTION | authenticated Owner; existing BarClimb project linked | M1.4 build authority; signing/runtime evidence remains separate |
| SendGrid | transactional email | NOT_VERIFIED | staging validating sink only; no provider delivery | Web GA requirement and later native-account dependency |
| S3 | durable objects/exports/creative | NOT_VERIFIED | none | Web GA requirement where used; platform gates as applicable |
| Heroku/Postgres/KVS | runtime/data/queue | VERIFIED_NONPRODUCTION | staging app + managed PostgreSQL/KVS + Web/worker/beat exercised | Web GA critical runtime; production still unverified |
| Sentry | observability | NOT_VERIFIED | none | Web GA requirement; each Native GA also requires native observability |
| AdSense | Web external ads | NOT_VERIFIED | none | approval is activation blocker, not Web GA blocker when fallback works |
| AdMob | native external ads | NOT_VERIFIED | none | native activation concern; not a Web GA blocker |
