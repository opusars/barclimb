# BarClimb Provider Status

No implementation-environment provider has yet been verified. Secret values must never be committed here.

M1.2 verified local PostgreSQL 14 and Redis 7.2 behavior and adds equivalent PostgreSQL 17/Redis 7.2 CI services. These are dependency/runtime proofs, not verification of a Heroku app, Heroku Postgres plan, or managed KVS add-on; the provider status therefore remains unchanged.

M1.3 exercises Django console/in-memory email delivery behind a provider-neutral boundary. This does not verify SendGrid or any other transactional-email provider, so provider statuses remain unchanged.

Release relevance is gate-specific. Apple/Google store approval and native production billing are Native GA blockers, not Web GA blockers merely because incomplete. Stripe is a Web GA commerce dependency but never canonical entitlement truth; Apple and Google purchase lifecycles must later map into the same Django Subscription/Entitlement domain.

| Provider | Intended role | Current status | Real nonprod verification | Launch relevance |
|---|---|---|---|---|
| OpenAI | generation/grading/compiler | NOT_VERIFIED | none | Web GA blocker by assessment milestone |
| Stripe | Web subscription purchase source | NOT_VERIFIED | none | Web GA paid-flow blocker; not entitlement truth |
| Apple | iOS distribution/IAP purchase source | NOT_VERIFIED | none | iOS Native GA blocker; not a Web GA blocker by itself |
| Google Play | Android distribution/billing purchase source | NOT_VERIFIED | none | Android Native GA blocker; not a Web GA blocker by itself |
| SendGrid | transactional email | NOT_VERIFIED | none | Web GA requirement and later native-account dependency |
| S3 | durable objects/exports/creative | NOT_VERIFIED | none | Web GA requirement where used; platform gates as applicable |
| Heroku/Postgres/KVS | runtime/data/queue | NOT_VERIFIED | none | Web GA critical runtime |
| Sentry | observability | NOT_VERIFIED | none | Web GA requirement; each Native GA also requires native observability |
| AdSense | Web external ads | NOT_VERIFIED | none | approval is activation blocker, not Web GA blocker when fallback works |
| AdMob | native external ads | NOT_VERIFIED | none | native activation concern; not a Web GA blocker |
