# BarClimb Provider Status

No implementation-environment provider has yet been verified. Secret values must never be committed here.

M1.2 verified local PostgreSQL 14 and Redis 7.2 behavior and adds equivalent PostgreSQL 17/Redis 7.2 CI services. These are dependency/runtime proofs, not verification of a Heroku app, Heroku Postgres plan, or managed KVS add-on; the provider status therefore remains unchanged.

| Provider | Intended role | Current status | Real nonprod verification | Launch relevance |
|---|---|---|---|---|
| OpenAI | generation/grading/compiler | NOT_VERIFIED | none | critical by assessment milestone |
| Stripe | web subscription | NOT_VERIFIED | none | GA blocker for web paid flow |
| Apple | iOS distribution/IAP | NOT_VERIFIED | none | GA blocker for iOS |
| Google Play | Android distribution/billing | NOT_VERIFIED | none | GA blocker for Android |
| SendGrid | transactional email | NOT_VERIFIED | none | launch requirement |
| S3 | durable objects/exports/creative | NOT_VERIFIED | none | launch requirement where used |
| Heroku/Postgres/KVS | runtime/data/queue | NOT_VERIFIED | none | critical |
| Sentry | observability | NOT_VERIFIED | none | launch requirement |
| AdSense | web external ads | NOT_VERIFIED | none | approval is activation blocker, not learner-GA blocker |
| AdMob | native external ads | NOT_VERIFIED | none | approval is activation blocker, not learner-GA blocker |
