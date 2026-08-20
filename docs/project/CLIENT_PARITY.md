# BarClimb Client Parity

Status values: NOT_STARTED / PARTIAL / VERIFIED / INTENTIONAL_DIFFERENCE.

M1.4 foundation acceptance establishes real client routing/build/auth seams. `PARTIAL` below does not assert product parity, Native GA readiness, or actual native runtime verification.

Release sequencing is Web GA → iOS Native GA → Android Native GA. This table remains a required architecture and release ledger: a native UI gap may be intentional before Web GA only when shared contracts stay portable and the gap is explicit; every applicable gap remains a hard blocker for that platform's Native GA.

| Capability | Web | iOS | Android | Notes |
|---|---|---|---|---|
| Client shell/toolchain | VERIFIED | PARTIAL | PARTIAL | Web builds and runs on persistent staging. Expo 57 iOS/Android JS exports pass. Signed Android internal build `2e340187-f441-4175-ba8b-852d044996f7` matches executable commit `2e32876`; iOS signing/build and both actual runtimes remain pending |
| Native navigation/deep links | N/A | PARTIAL | PARTIAL | React Navigation auth stack, authenticated tabs, canonical-link resolver, environment-specific IDs/intent configuration, and gated association endpoints are implemented and test-covered. Staging AASA/assetlinks remain unpublished and real OS routing remains a Native GA blocker. |
| Auth/account | VERIFIED | PARTIAL | PARTIAL | Web session/CSRF signup-login and deployed outbox/safe-sink proof run on staging; native bearer issuance/revocation and automated SecureStore states pass. Actual-device save/restore/delete/restart/uninstall and auth lifecycle remain unverified on both platforms; the signed Android APK is build-only evidence. |
| MCQ interaction | NOT_STARTED | NOT_STARTED | NOT_STARTED | highlight/strike/review required |
| IQS | NOT_STARTED | NOT_STARTED | NOT_STARTED | schema-driven |
| PT/LRPT | NOT_STARTED | NOT_STARTED | NOT_STARTED | long-form editor/recovery critical |
| Progress/recommendations | NOT_STARTED | NOT_STARTED | NOT_STARTED | same learner truth |
| Simulation | NOT_STARTED | NOT_STARTED | NOT_STARTED | blueprint fidelity |
| Community/discussion | NOT_STARTED | NOT_STARTED | NOT_STARTED | report/block/moderation required |
| Circles | NOT_STARTED | NOT_STARTED | NOT_STARTED | invite-only v1 |
| Subscription/restore | NOT_STARTED | NOT_STARTED | NOT_STARTED | Stripe / Apple / Google paths |
| Offline/recovery | NOT_STARTED | NOT_STARTED | NOT_STARTED | platform-specific implementation permitted |
