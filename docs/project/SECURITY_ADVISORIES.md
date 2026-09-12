# BarClimb Security Advisory Ledger

Review date: 2026-09-12. Re-review on each Expo SDK or React Native patch upgrade and before a native release candidate. This ledger records `npm audit` reachability; it is not a claim that scanner findings are false.

## Patched in M1.1a

- Vite advisories through 7.3.4, including development-server path traversal/file-read findings: upgraded the direct development dependency from 7.1.4 to 7.3.6. Vite is not shipped as an application runtime, but the compatible patch was available and applied.
- Vitest `GHSA-5xrq-8626-4rwp` (critical UI-server arbitrary file read/execution): upgraded both test-workspace declarations from 3.2.4 to 3.2.7. Vitest is test tooling and its UI server was not enabled, but the compatible patch was available and applied.

## Open upstream Expo/React Native toolchain advisories

| Advisory/package | Resolved path | Reachability and exploit relevance | Mitigation/upstream status |
|---|---|---|---|
| `uuid` `GHSA-w5hq-g745-h8pq` (moderate) | `expo@57.0.22` -> `@expo/config-plugins@57.0.9` -> `xcode@3.0.1` -> `uuid@7.0.3` | Native configuration/Xcode project tooling. The vulnerable buffer-supplied v3/v5/v6 API is not called by BarClimb application runtime code and is not a server endpoint. | Keep native config inputs trusted. No compatible stable SDK 57 fix is exposed by current Expo validation; npm's suggested Expo 46 downgrade violates the approved foundation. Recheck upstream patches before release. |
| `decode-uri-component` `GHSA-vcc3-ghjq-m6fr` (moderate) | React Navigation 7 -> `@react-navigation/core@7.16.0` -> `query-string@7.1.3` -> `decode-uri-component@0.2.2` | Malformed percent-encoded input can cause excessive decoding work. BarClimb does not pass arbitrary external query strings through this library in its current fixed-route foundation, but future deep-link and navigation-input work must treat all external route parameters as untrusted. | The advisory appeared in the npm feed without a package-version change during the Expo 57.0.19 review. npm exposes no compatible fix for the accepted React Navigation line. Retain fixed route parsing, bound external navigation inputs, and recheck before deep-link enablement or native release. |
| `js-yaml` `GHSA-2883-xcg3-v3hh` (high) | Expo CLI/configuration toolchain -> `js-yaml@4.1.1` | Crafted YAML with many empty merge sources can consume excessive CPU. BarClimb does not accept untrusted YAML through an application or server endpoint; exposure is limited to developer/build tooling operating on repository-controlled configuration. | Newly present in the 2026-09-12 npm advisory feed. npm reports a transitive fix, but this bounded Expo metadata task does not apply unrelated overrides or audit fixes. Keep repository/build inputs trusted and evaluate the compatible upstream resolution separately. |

`npm audit --omit=dev` reports 17 moderate aggregate nodes, 1 high, and 0 critical. Ten moderate nodes remain the `uuid` native-configuration family and seven remain the `decode-uri-component`/React Navigation family. The one high node is `js-yaml` in the Expo configuration toolchain. The aggregate count does not represent 18 separately exploitable BarClimb runtime paths. No audit fix was run; the maintenance task records rather than silently expands scope to repair unrelated advisory metadata.

The Expo 57.0.18/React Native 0.86.3 compatibility correction removed `image-size`; those two historical high advisories remain closed. Expo 57.0.22 leaves React Navigation versions unchanged. The newly reported `js-yaml` advisory is a distinct build-tooling family and is not a reappearance of `image-size`.

## M1.3 authentication review

- Session fixation: Django login rotation is integration-tested; logout flushes the Web session.
- CSRF: every browser mutation, including anonymous login/signup/reset/verification, has explicit CSRF middleware enforcement. Native bearer endpoints are non-cookie authenticated and do not use CSRF. No CORS middleware/origin wildcard was introduced.
- Credential persistence: passwords use Django hashing only. Native secrets are cryptographically random; reset/verification credentials are HMAC-derived from random immutable UUIDs and the signing secret. PostgreSQL stores action/native SHA-256 digests only. Native persists only the opaque secret in Expo SecureStore with device-only/unlocked iOS accessibility, never AsyncStorage.
- Enumeration and unsafe errors: login uses one generic credential error; reset and resend requests return the same generic response and create the same provider-neutral durable lifecycle for missing/existing identities, preventing provider failure from becoming an HTTP oracle. Broker arguments contain only redacted delivery UUIDs, not submitted email or credentials. Signup must report unavailable unique identity fields to resolve account creation and remains rate-limited.
- Revocation/expiry: email actions expire, rotate, are purpose-bound/single-use, and have one-active-token database enforcement. Native logout and password reset revoke durable native sessions; all requests recheck revocation/expiry/user-active state.
- Public identity: no anonymous account/profile endpoint exists. Authenticated `/me` returns private email only to the owning session. Owner checks compare authenticated user objects, not client-supplied IDs.
- Logging/providers: auth endpoints do not log credentials/tokens/payloads. Console email intentionally prints local-only action links; it must not be selected for deployed production. No real email provider, native device keychain, universal/app link, or deployed proxy behavior is verified yet.

## M1.3a adversarial-review remediation

- **Action-link leakage (HIGH, resolved):** verification/reset credentials moved from query strings to Web URL fragments. Web removes the fragment/query immediately and sends the credential only in a CSRF-protected POST body. Backend GET/query completion is unsupported. Router/access logs therefore receive only the clean completion path.
- **Native reset/issuance race (HIGH, resolved):** both flows serialize on the user row, issuance revalidates the password while locked, and reset increments authentication generation plus revokes active native rows. PostgreSQL tests cover both lock orders; existing Web sessions invalidate through Django's password hash.
- **Best-effort email publication (HIGH, resolved):** token plus `AuthEmailDelivery` are created atomically in PostgreSQL. Celery receives only a redacted delivery UUID. Leases, bounded retry/backoff, terminal states, a one-minute recovery sweep, and manual replay survive broker/provider failures without token-rotation races. Raw credentials are not persisted plaintext or placed in task args/results/logs.
- **Action-link origin and deployed transport (MEDIUM, resolved):** `PUBLIC_BASE_URL` is explicitly the canonical Web origin; local links target Vite port 5173. Review, staging, and production force HTTPS/secure cookies behind the declared Heroku proxy header contract.
- **Proxy/rate-limit identity (MEDIUM, resolved):** deployed extraction accepts only the canonicalized rightmost Heroku-router-appended forwarded address with `REMOTE_ADDR` fallback. Tests cover forged chains, shared proxies, IPv4/IPv6, malformed/missing values, and casing-resistant identity keys. KVS outage fails authentication closed with generic 503 and never changes PostgreSQL authority.
- **Native transient/SecureStore handling (MEDIUM, resolved):** only authoritative 401/403 validation removes a credential. Offline/5xx preserves it. Read/write/delete/revocation failures terminate loading and expose distinct recoverable states; logout does not claim secure completion before server revocation.
- **Low-cost findings (resolved):** Bearer scheme parsing is case-insensitive and Web auth handles non-JSON errors without exposing parser failures.

Still intentionally deferred: username rename policy, Terms acceptance, public-profile behavior, native session-management UI, refresh-token architecture, real SendGrid/provider idempotency verification, and real-device SecureStore/backup behavior. These are not silently treated as verified.

## M1.4 staging security evidence

- Persistent Heroku staging forces HTTP-to-HTTPS redirect, recognizes Heroku forwarded HTTPS without a redirect loop, and serves Web/API same-origin with secure cookies. PostgreSQL and KVS readiness passed after explicitly applying Heroku's documented self-signed KVS TLS option; certificate verification remains the default elsewhere.
- A deployed forged-forwarding test varied caller-prepended addresses across 11 unique native-login identities. Ten requests reached credential validation and the eleventh returned 429, confirming the router-appended rightmost address owns the shared source counter.
- The staging-only email sink validates exactly one canonical HTTPS fragment-token action and logs only its safe route. Production rejects this backend. Deployed worker/beat/outbox evidence passed; SendGrid remains unverified.
- A scan of 1,500 accessible staging application log lines found no fragment/query token, Authorization, Bearer, or password-shaped credential patterns. One controlled native API diagnostic displayed a generated bearer in local tool output (not Heroku logs); it was immediately revoked and a follow-up authenticated request returned 401.
- A read-only Heroku release inspection unexpectedly emitted staging configuration values into operator-tool output. PostgreSQL credentials, KVS credentials, and the Django signing secret were treated as compromised and rotated immediately. Current configuration release v12 restarted Web/worker/beat successfully, and database/KVS readiness returned `ok`; no secret value is retained in repository continuity records.
- Association files remain unpublished (404) until Apple/Android signing identifiers are verified. Credential-bearing verification/reset paths are excluded from association payloads even when enabled.

M1.4 now verifies EAS project ownership and one signed Android internal build path; that is build-only evidence. Still intentionally unverified and retained for the applicable later gate: Apple Developer team/signing/iOS builds, Google Play ownership/recovery, actual iOS/Android authentication, physical-device SecureStore/Keychain/Keystore read-write-delete/restart/uninstall behavior, real OS Universal/App Link resolution, native production purchase/restore, and SendGrid delivery.
