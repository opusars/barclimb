# BarClimb Client Parity

Status values: NOT_STARTED / PARTIAL / VERIFIED / INTENTIONAL_DIFFERENCE.

M1.5 extends the foundation with automated cross-client assessment presentation risk proofs. `PARTIAL` below does not assert production Practice, complete interaction parity, Native GA readiness, or actual native runtime verification.

Release sequencing is Web GA → iOS Native GA → Android Native GA. This table remains a required architecture and release ledger: a native UI gap may be intentional before Web GA only when shared contracts stay portable and the gap is explicit; every applicable gap remains a hard blocker for that platform's Native GA.

| Capability | Web | iOS | Android | Notes |
|---|---|---|---|---|
| Client shell/toolchain | VERIFIED | PARTIAL | PARTIAL | Web builds and runs on persistent staging. Expo 57 iOS/Android JS exports pass. Signed Android internal build `2e340187-f441-4175-ba8b-852d044996f7` matches executable commit `2e32876`; iOS signing/build and both actual runtimes remain pending |
| Native navigation/deep links | N/A | PARTIAL | PARTIAL | React Navigation auth stack, authenticated tabs, canonical-link resolver, environment-specific IDs/intent configuration, and gated association endpoints are implemented and test-covered. Staging AASA/assetlinks remain unpublished and real OS routing remains a Native GA blocker. |
| Auth/account | VERIFIED | PARTIAL | PARTIAL | Web session/CSRF signup-login and deployed outbox/safe-sink proof run on staging; native bearer issuance/revocation and automated SecureStore states pass. Actual-device save/restore/delete/restart/uninstall and auth lifecycle remain unverified on both platforms; the signed Android APK is build-only evidence. |
| MCQ interaction | PARTIAL | PARTIAL | PARTIAL | One shared schema/state fixture drives semantic Web radio rows and native accessible radio rows; selection/reselection/review persistence pass. Grading, answer keys, highlight, elimination, server attempts, and physical-device proof remain later gates. |
| IQS | PARTIAL | PARTIAL | PARTIAL | Stable resource identity and shared workspace state preserve an answer across text/email/statute resource switches on Web/native renderer paths. Release rules, server hydration, annotations, and device runtime remain unimplemented. |
| PT/LRPT | PARTIAL | PARTIAL | PARTIAL | Shared text/format/resource/autosave state drives Web textarea and native multiline-editor spikes for both canonical PT families. Interrupted-write and remount restoration pass through a replaceable adapter. This is not the production editor, durable native storage, server sync, or device recovery. |
| Progress/recommendations | NOT_STARTED | NOT_STARTED | NOT_STARTED | same learner truth |
| Simulation | NOT_STARTED | NOT_STARTED | NOT_STARTED | blueprint fidelity |
| Community/discussion | NOT_STARTED | NOT_STARTED | NOT_STARTED | report/block/moderation required |
| Circles | NOT_STARTED | NOT_STARTED | NOT_STARTED | invite-only v1 |
| Subscription/restore | NOT_STARTED | NOT_STARTED | NOT_STARTED | Stripe / Apple / Google paths |
| Offline/recovery | PARTIAL | PARTIAL | PARTIAL | M1.5 proves portable save-state transitions and local snapshot recovery; Web local storage and native module-memory/background-save adapters are replaceable. Cross-device conflicts, server idempotency, process-kill, encrypted native durability, and physical-device recovery remain open. |
