# BarClimb Security Advisory Ledger

Review date: 2026-08-13. Re-review on each Expo SDK or React Native patch upgrade and before a native release candidate. This ledger records `npm audit` reachability; it is not a claim that scanner findings are false.

## Patched in M1.1a

- Vite advisories through 7.3.4, including development-server path traversal/file-read findings: upgraded the direct development dependency from 7.1.4 to 7.3.6. Vite is not shipped as an application runtime, but the compatible patch was available and applied.
- Vitest `GHSA-5xrq-8626-4rwp` (critical UI-server arbitrary file read/execution): upgraded both test-workspace declarations from 3.2.4 to 3.2.7. Vitest is test tooling and its UI server was not enabled, but the compatible patch was available and applied.

## Open upstream Expo/React Native toolchain advisories

| Advisory/package | Resolved path | Reachability and exploit relevance | Mitigation/upstream status |
|---|---|---|---|
| `image-size` `GHSA-w3rx-r6r6-pgpr` and `GHSA-5p2g-fcmc-qvqq` (high) | `expo@57.0.12` -> `@expo/metro@56.0.0` -> `metro@0.84.4` -> `image-size@1.2.1` | Build/development Metro image inspection. It is not imported by BarClimb application code or present as an independently invoked server-side parser in the shipped JS bundle. Exploitation would require an attacker-controlled malicious ICNS/JXL/HEIF asset to enter a trusted local/CI bundle input. | Keep build inputs repository-controlled and reviewed. No compatible Expo 57/RN 0.86 update currently resolves the scanner range. npm proposes incompatible downgrades to Expo 53/RN 0.72; do not apply. Recheck upstream patches before release. |
| `uuid` `GHSA-w5hq-g745-h8pq` (moderate) | `expo@57.0.12` -> `@expo/config-plugins@57.0.7` -> `xcode@3.0.1` -> `uuid@7.0.3` | Native configuration/Xcode project tooling. The vulnerable buffer-supplied v3/v5/v6 API is not called by BarClimb application runtime code and is not a server endpoint. | Keep native config inputs trusted. No compatible Expo 57 fix is exposed by npm; its suggested Expo 53 downgrade violates the approved foundation. Recheck upstream patches before release. |

`npm audit --omit=dev` reports 18 aggregate nodes (7 moderate, 11 high) because the two root advisories propagate through Expo CLI, Metro, config-plugin, and React Native dependency nodes. Those aggregate nodes share the two concrete advisory sources above; they do not represent 18 separately exploitable BarClimb code paths. `npm audit fix --force` was not run. The current repository has no released application, no production Metro server, and no untrusted asset-ingestion path.

## M1.3 authentication review

- Session fixation: Django login rotation is integration-tested; logout flushes the Web session.
- CSRF: every browser mutation, including anonymous login/signup/reset/verification, has explicit CSRF middleware enforcement. Native bearer endpoints are non-cookie authenticated and do not use CSRF. No CORS middleware/origin wildcard was introduced.
- Credential persistence: passwords use Django hashing only. Reset/verification/native raw secrets use cryptographic random generation; PostgreSQL stores SHA-256 digests only. Native persists only the opaque secret in Expo SecureStore with device-only/unlocked iOS accessibility, never AsyncStorage.
- Enumeration and unsafe errors: login uses one generic credential error; reset and resend requests return the same generic response and enqueue the same provider-neutral operation for missing/existing identities, preventing provider latency from becoming an HTTP timing oracle. Broker arguments contain only redacted internal/sentinel IDs, not submitted email. Signup must report unavailable unique identity fields to resolve account creation and remains rate-limited.
- Revocation/expiry: email actions expire, rotate, are purpose-bound/single-use, and have one-active-token database enforcement. Native logout and password reset revoke durable native sessions; all requests recheck revocation/expiry/user-active state.
- Public identity: no anonymous account/profile endpoint exists. Authenticated `/me` returns private email only to the owning session. Owner checks compare authenticated user objects, not client-supplied IDs.
- Logging/providers: auth endpoints do not log credentials/tokens/payloads. Console email intentionally prints local-only action links; it must not be selected for deployed production. No real email provider, native device keychain, universal/app link, or deployed proxy behavior is verified yet.
