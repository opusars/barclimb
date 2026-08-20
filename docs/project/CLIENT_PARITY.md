# BarClimb Client Parity

Status values: NOT_STARTED / PARTIAL / VERIFIED / INTENTIONAL_DIFFERENCE.

M1.4 establishes real client routing foundations. `PARTIAL` below does not assert product parity or actual native runtime verification.

Release sequencing is Web GA → iOS Native GA → Android Native GA. This table remains a required architecture and release ledger: a native UI gap may be intentional before Web GA only when shared contracts stay portable and the gap is explicit; every applicable gap remains a hard blocker for that platform's Native GA.

| Capability | Web | iOS | Android | Notes |
|---|---|---|---|---|
| Client shell/toolchain | VERIFIED | PARTIAL | PARTIAL | Web builds and runs on persistent staging. Expo/EAS project ownership is verified and Expo 57 iOS/Android JS exports pass; internal signed builds and actual runtimes remain pending |
| Native navigation/deep links | N/A | PARTIAL | PARTIAL | React Navigation auth stack + authenticated tabs and canonical-link resolver implemented. Environment-specific IDs/intent configuration and association endpoints exist; OS association stays disabled until signing identities are verified |
| Auth/account | VERIFIED | PARTIAL | PARTIAL | Web session/CSRF signup-login proof runs on staging; deployed outbox/safe sink and native bearer API issuance/revocation run. Native UI and SecureStore remain unverified on actual platforms |
| MCQ interaction | NOT_STARTED | NOT_STARTED | NOT_STARTED | highlight/strike/review required |
| IQS | NOT_STARTED | NOT_STARTED | NOT_STARTED | schema-driven |
| PT/LRPT | NOT_STARTED | NOT_STARTED | NOT_STARTED | long-form editor/recovery critical |
| Progress/recommendations | NOT_STARTED | NOT_STARTED | NOT_STARTED | same learner truth |
| Simulation | NOT_STARTED | NOT_STARTED | NOT_STARTED | blueprint fidelity |
| Community/discussion | NOT_STARTED | NOT_STARTED | NOT_STARTED | report/block/moderation required |
| Circles | NOT_STARTED | NOT_STARTED | NOT_STARTED | invite-only v1 |
| Subscription/restore | NOT_STARTED | NOT_STARTED | NOT_STARTED | Stripe / Apple / Google paths |
| Offline/recovery | NOT_STARTED | NOT_STARTED | NOT_STARTED | platform-specific implementation permitted |
