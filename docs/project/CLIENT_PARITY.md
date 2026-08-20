# BarClimb Client Parity

Status values: NOT_STARTED / PARTIAL / VERIFIED / INTENTIONAL_DIFFERENCE.

M1.1 establishes proof shells only. `PARTIAL` below does not assert feature parity.

Release sequencing is Web GA → iOS Native GA → Android Native GA. This table remains a required architecture and release ledger: a native UI gap may be intentional before Web GA only when shared contracts stay portable and the gap is explicit; every applicable gap remains a hard blocker for that platform's Native GA.

| Capability | Web | iOS | Android | Notes |
|---|---|---|---|---|
| Client shell/toolchain | PARTIAL | PARTIAL | PARTIAL | Accepted main exports both clients. Separate M1.4 evidence verifies EAS ownership and a signed Android internal APK; no signed iOS build or actual-device runtime is verified. |
| Native navigation/deep links | N/A | PARTIAL | PARTIAL | Separate M1.4 branch replaces simulated destinations with React Navigation and test-covered gated link config/canonical parsing. Staging AASA/assetlinks stay unpublished and no real OS routing is verified; each remains a Native GA blocker. |
| Auth/account | PARTIAL | PARTIAL | PARTIAL | Shared Web session/CSRF and native opaque-session protocols are implemented; M1.4 proves deployed Web/backend auth and automated native SecureStore states. Actual-device save/restore/delete/restart/uninstall and auth lifecycle remain unverified on iOS/Android; SendGrid remains unverified. |
| MCQ interaction | NOT_STARTED | NOT_STARTED | NOT_STARTED | highlight/strike/review required |
| IQS | NOT_STARTED | NOT_STARTED | NOT_STARTED | schema-driven |
| PT/LRPT | NOT_STARTED | NOT_STARTED | NOT_STARTED | long-form editor/recovery critical |
| Progress/recommendations | NOT_STARTED | NOT_STARTED | NOT_STARTED | same learner truth |
| Simulation | NOT_STARTED | NOT_STARTED | NOT_STARTED | blueprint fidelity |
| Community/discussion | NOT_STARTED | NOT_STARTED | NOT_STARTED | report/block/moderation required |
| Circles | NOT_STARTED | NOT_STARTED | NOT_STARTED | invite-only v1 |
| Subscription/restore | NOT_STARTED | NOT_STARTED | NOT_STARTED | Stripe / Apple / Google paths |
| Offline/recovery | NOT_STARTED | NOT_STARTED | NOT_STARTED | platform-specific implementation permitted |
