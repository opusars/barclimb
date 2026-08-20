# BarClimb Provider Status

Secret values must never be committed here. Provider evidence is scoped by environment and by the branch that contains it; `VERIFIED_NONPRODUCTION` is not production acceptance.

The separate, green, unmerged M1.4 branch at `4c1d2e6` verifies owner access to the existing Heroku staging app and EAS project. Heroku Web/worker/beat, Essential-0 PostgreSQL, Mini KVS, public readiness, and account standing were observed read-only. EAS produced a signed Android internal APK. This evidence may satisfy the clarified M1.4 foundation gate after that branch is brought forward and accepted; it does not verify production, an actual native runtime, Apple, or Google Play.

M1.3 exercises Django console/in-memory email delivery behind a provider-neutral boundary. This does not verify SendGrid or any other transactional-email provider, so provider statuses remain unchanged.

Release relevance is gate-specific. Apple/Google store approval and native production billing are Native GA blockers, not Web GA blockers merely because incomplete. Stripe is a Web GA commerce dependency but never canonical entitlement truth; Apple and Google purchase lifecycles must later map into the same Django Subscription/Entitlement domain.

| Provider | Intended role | Current status | Real nonprod verification | Launch relevance |
|---|---|---|---|---|
| OpenAI | generation/grading/compiler | NOT_VERIFIED | none | Web GA blocker by assessment milestone |
| Stripe | Web subscription purchase source | NOT_VERIFIED | none | Web GA paid-flow blocker; not entitlement truth |
| Apple | iOS distribution/IAP purchase source | NOT_VERIFIED / BLOCKED_EXTERNAL | no BarClimb Apple Developer Program team; no signed iOS build | iOS Native GA blocker; not an M1.4/Web-train blocker by itself |
| Google Play | Android distribution/billing purchase source | NOT_VERIFIED | EAS Android signing is verified, but Play ownership/recovery is not | Android Native GA blocker; not an M1.4/Web-train blocker by itself |
| Expo/EAS | native build-project control/internal builds | VERIFIED_NONPRODUCTION | owner access to existing project; signed Android internal build `2e340187-f441-4175-ba8b-852d044996f7` | satisfies available-platform M1.4 signed-build path; no iOS/runtime/store claim |
| SendGrid | transactional email | NOT_VERIFIED | none | Web GA requirement and later native-account dependency |
| S3 | durable objects/exports/creative | NOT_VERIFIED | none | Web GA requirement where used; platform gates as applicable |
| Heroku/Postgres/KVS | runtime/data/queue | VERIFIED_NONPRODUCTION | staging Web/worker/beat, Essential-0 PostgreSQL, Mini KVS, readiness, owner/account-standing evidence | M1.4 staging gate evidence; production remains a Web GA blocker |
| Sentry | observability | NOT_VERIFIED | none | Web GA requirement; each Native GA also requires native observability |
| AdSense | Web external ads | NOT_VERIFIED | none | approval is activation blocker, not Web GA blocker when fallback works |
| AdMob | native external ads | NOT_VERIFIED | none | native activation concern; not a Web GA blocker |
