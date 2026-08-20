# BarClimb Client Parity

Status values: NOT_STARTED / PARTIAL / VERIFIED / INTENTIONAL_DIFFERENCE.

M1.1 establishes proof shells only. `PARTIAL` below does not assert feature parity.

Release sequencing is Web GA → iOS Native GA → Android Native GA. This table remains a required architecture and release ledger: a native UI gap may be intentional before Web GA only when shared contracts stay portable and the gap is explicit; every applicable gap remains a hard blocker for that platform's Native GA.

| Capability | Web | iOS | Android | Notes |
|---|---|---|---|---|
| Client shell/toolchain | PARTIAL | PARTIAL | PARTIAL | Web ReactDOM mount/build passes; Expo 57 iOS/Android JS exports pass; no simulator/device/store-build verification |
| Native navigation/deep links | N/A | NOT_STARTED | NOT_STARTED | Current shell buttons simulate destinations in local state; routing/universal/app links remain later M1 work |
| Auth/account | PARTIAL | PARTIAL | PARTIAL | One email-login/username-public identity; Web session+CSRF/query-free fragment completion and native generation-bound opaque session+recoverable SecureStore states implemented. Shared backend security semantics are tested; native device builds/deep-linked completion, deployed proxy, and real email delivery remain unverified |
| MCQ interaction | NOT_STARTED | NOT_STARTED | NOT_STARTED | highlight/strike/review required |
| IQS | NOT_STARTED | NOT_STARTED | NOT_STARTED | schema-driven |
| PT/LRPT | NOT_STARTED | NOT_STARTED | NOT_STARTED | long-form editor/recovery critical |
| Progress/recommendations | NOT_STARTED | NOT_STARTED | NOT_STARTED | same learner truth |
| Simulation | NOT_STARTED | NOT_STARTED | NOT_STARTED | blueprint fidelity |
| Community/discussion | NOT_STARTED | NOT_STARTED | NOT_STARTED | report/block/moderation required |
| Circles | NOT_STARTED | NOT_STARTED | NOT_STARTED | invite-only v1 |
| Subscription/restore | NOT_STARTED | NOT_STARTED | NOT_STARTED | Stripe / Apple / Google paths |
| Offline/recovery | NOT_STARTED | NOT_STARTED | NOT_STARTED | platform-specific implementation permitted |
