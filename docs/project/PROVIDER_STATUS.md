# BarClimb Provider Status

Secret values must never be committed here. Status is service-specific and evidence-gated; `VERIFIED_NONPRODUCTION` is not production acceptance.

The M1.4 branch now contains authoritative main and passes the clarified foundation gate. Fresh read-only checks verify owner access to the existing Heroku staging app and EAS project: Heroku Web/worker/beat, Essential-0 PostgreSQL, Mini KVS, public readiness, and auth routes are healthy; EAS confirms the finished signed Android internal APK. This evidence does not verify production, an actual native runtime, Apple, or Google Play.

M1.3 exercises Django console/in-memory email delivery behind a provider-neutral boundary. This does not verify SendGrid or any other transactional-email provider, so provider statuses remain unchanged.

M1.4 verifies the Heroku runtime, Essential-0 PostgreSQL add-on `postgresql-aerodynamic-56880`, and Mini KVS add-on `redis-flat-93728` in persistent non-production staging app `barclimb-staging` (deployed commit `6bec558`; code release v8; current post-rotation configuration release v12). Release migrations, Web/worker/beat processes, PostgreSQL and TLS KVS round trips, readiness, HTTPS, auth throttling, and durable outbox execution all succeeded. This is `VERIFIED_NONPRODUCTION`, not production readiness.

On 2026-08-20 the initial CLI session was authenticated to unrelated account `leor@cashcopawn.com`, which correctly received `forbidden`. After a fresh login, `apollonomios@gmail.com` was verified as the sole owner of `barclimb-staging`. Web, worker, and beat are up on release v12; Essential-0 PostgreSQL 18.3 and Mini KVS 8.1.9 are available; health/readiness return 200 with database/KVS `ok`; HTTPS root returns 200 and HTTP redirects 301. Heroku's account-delinquency endpoint reports both scheduled suspension and deletion as null. No app, add-on, credential, or unrelated Heroku app was changed.

Expo authentication verifies Owner role on both `opusars` and `opusarss-team`; the repository is linked to the pre-existing `@opusarss-team/barclimb` project ID `8ed30301-53d9-4630-b2c4-70d6d51f465b`. EAS build `2e340187-f441-4175-ba8b-852d044996f7` used the existing EAS-managed Android keystore and produced a signed internal-distribution staging APK from exact executable-state commit `2e32876bce0ecf315b174071fa6505d408f29258`. This proves non-production Android build/signing orchestration, not Google Play ownership/recovery, actual Android runtime, store, or production readiness. No iOS build can proceed until a BarClimb Apple Developer Program team exists.

Release relevance is gate-specific. Apple/Google store approval and native production billing are Native GA blockers, not Web GA blockers merely because incomplete. Stripe is a Web GA commerce dependency but never canonical entitlement truth; Apple and Google purchase lifecycles must later map into the same Django Subscription/Entitlement domain.

| Provider | Intended role | Current status | Real nonprod verification | Launch relevance |
|---|---|---|---|---|
| OpenAI | generation/grading/compiler | NOT_VERIFIED | none | Web GA blocker by assessment milestone |
| Stripe | Web subscription purchase source | NOT_VERIFIED | none | Web GA paid-flow blocker; not entitlement truth |
| Apple | iOS distribution/IAP purchase source | NOT_VERIFIED / BLOCKED_EXTERNAL | no BarClimb Apple Developer Program team; no signed iOS build | iOS Native GA blocker; not an M1.4/Web-train blocker by itself |
| Google Play | Android distribution/billing purchase source | NOT_VERIFIED | signed EAS internal APK exists; Play ownership/recovery remains unverified | Android Native GA blocker; not an M1.4/Web-train blocker by itself |
| Expo/EAS | native build-project control/internal builds | VERIFIED_NONPRODUCTION | authenticated Owner; existing project linked; signed Android internal build `2e340187-f441-4175-ba8b-852d044996f7` | satisfies available-platform M1.4 signed-build path; no iOS/runtime/store claim |
| SendGrid | transactional email | NOT_VERIFIED | staging validating sink only; no provider delivery | Web GA requirement and later native-account dependency |
| S3 | durable objects/exports/creative | NOT_VERIFIED | none | Web GA requirement where used; platform gates as applicable |
| Heroku/Postgres/KVS | runtime/data/queue | VERIFIED_NONPRODUCTION | staging Web/worker/beat, Essential-0 PostgreSQL, Mini KVS, readiness, owner/account-standing evidence | M1.4 staging gate evidence; production remains a Web GA blocker |
| Sentry | observability | NOT_VERIFIED | none | Web GA requirement; each Native GA also requires native observability |
| AdSense | Web external ads | NOT_VERIFIED | none | approval is activation blocker, not Web GA blocker when fallback works |
| AdMob | native external ads | NOT_VERIFIED | none | native activation concern; not a Web GA blocker |
