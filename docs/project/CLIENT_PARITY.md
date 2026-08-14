# BarClimb Client Parity

Status values: NOT_STARTED / PARTIAL / VERIFIED / INTENTIONAL_DIFFERENCE.

M1.1 establishes proof shells only. `PARTIAL` below does not assert feature parity.

| Capability | Web | iOS | Android | Notes |
|---|---|---|---|---|
| Client shell/toolchain | PARTIAL | PARTIAL | PARTIAL | Web ReactDOM mount/build passes; Expo 57 iOS/Android JS exports pass; no simulator/device/store-build verification |
| Native navigation/deep links | N/A | NOT_STARTED | NOT_STARTED | Current shell buttons simulate destinations in local state; routing/universal/app links remain later M1 work |
| Auth/account | PARTIAL | PARTIAL | PARTIAL | One email-login/username-public identity; Web session+CSRF and native opaque session+SecureStore implemented; native device builds/deep-linked completion and real email delivery unverified |
| MCQ interaction | NOT_STARTED | NOT_STARTED | NOT_STARTED | highlight/strike/review required |
| IQS | NOT_STARTED | NOT_STARTED | NOT_STARTED | schema-driven |
| PT/LRPT | NOT_STARTED | NOT_STARTED | NOT_STARTED | long-form editor/recovery critical |
| Progress/recommendations | NOT_STARTED | NOT_STARTED | NOT_STARTED | same learner truth |
| Simulation | NOT_STARTED | NOT_STARTED | NOT_STARTED | blueprint fidelity |
| Community/discussion | NOT_STARTED | NOT_STARTED | NOT_STARTED | report/block/moderation required |
| Circles | NOT_STARTED | NOT_STARTED | NOT_STARTED | invite-only v1 |
| Subscription/restore | NOT_STARTED | NOT_STARTED | NOT_STARTED | Stripe / Apple / Google paths |
| Offline/recovery | NOT_STARTED | NOT_STARTED | NOT_STARTED | platform-specific implementation permitted |
