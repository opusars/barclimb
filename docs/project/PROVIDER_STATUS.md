# BarClimb Provider Status

Secret values must never be committed here. Status is service-specific and evidence-gated.

M1.2 verified local PostgreSQL 14 and Redis 7.2 behavior and adds equivalent PostgreSQL 17/Redis 7.2 CI services. These are dependency/runtime proofs, not verification of a Heroku app, Heroku Postgres plan, or managed KVS add-on; the provider status therefore remains unchanged.

M1.3 exercises Django console/in-memory email delivery behind a provider-neutral boundary. This does not verify SendGrid or any other transactional-email provider, so provider statuses remain unchanged.

M1.4 verifies the Heroku runtime, Essential-0 PostgreSQL add-on `postgresql-aerodynamic-56880`, and Mini KVS add-on `redis-flat-93728` in persistent non-production staging app `barclimb-staging` (deployed commit `6bec558`; code release v8; current post-rotation configuration release v12). Release migrations, Web/worker/beat processes, PostgreSQL and TLS KVS round trips, readiness, HTTPS, auth throttling, and durable outbox execution all succeeded. This is `VERIFIED_NONPRODUCTION`, not production readiness. The Heroku account displayed a delinquent-payment warning with a stated suspension date of 2026-08-18; payment/account standing is an external continuity risk.

| Provider | Intended role | Current status | Real nonprod verification | Launch relevance |
|---|---|---|---|---|
| OpenAI | generation/grading/compiler | NOT_VERIFIED | none | critical by assessment milestone |
| Stripe | web subscription | NOT_VERIFIED | none | GA blocker for web paid flow |
| Apple | iOS distribution/IAP | NOT_VERIFIED | EAS unauthenticated; no team/signing evidence | GA blocker for iOS |
| Google Play | Android distribution/billing | NOT_VERIFIED | EAS unauthenticated; no project/signing evidence | GA blocker for Android |
| SendGrid | transactional email | NOT_VERIFIED | staging validating sink only; no provider delivery | launch requirement |
| S3 | durable objects/exports/creative | NOT_VERIFIED | none | launch requirement where used |
| Heroku/Postgres/KVS | runtime/data/queue | VERIFIED_NONPRODUCTION | staging app + managed PostgreSQL/KVS + web/worker/beat exercised | critical; production still unverified |
| Sentry | observability | NOT_VERIFIED | none | launch requirement |
| AdSense | web external ads | NOT_VERIFIED | none | approval is activation blocker, not learner-GA blocker |
| AdMob | native external ads | NOT_VERIFIED | none | approval is activation blocker, not learner-GA blocker |
