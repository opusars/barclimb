# M1.3 Identity and Authentication Contract

## Identity boundary

`accounts.User` is the single Web/iOS/Android identity. Login authority is normalized private email plus a Django-managed password; username is the normalized, unique future public identity. The account table contains no jurisdiction, real name, learner profile, analytics, curriculum, entitlement, subscription, preference, or community reputation state. `GET /api/v1/auth/me/` may return email only to that authenticated account; future public profile serializers must expose username and deliberately omit email.

Usernames are 3–30 lowercase ASCII letters, digits, or underscores, begin with a letter, and cannot use the reserved platform names in `accounts.validators`. Inputs are trimmed/lowercased before validation and persistence. Emails are trimmed/lowercased after Django email normalization and are unique. Password creation/reset uses Django validators and hashers; raw passwords are never stored or logged.

## Web contract

Web is same-origin and uses Django's opaque `HttpOnly`, `SameSite=Lax` session cookie. Django login rotates the session key; logout flushes it; password changes invalidate existing Django sessions through the authentication hash. All browser mutation endpoints are explicitly CSRF-protected, including anonymous signup, login, verification, and password reset. `GET /api/v1/auth/csrf/` supplies a token for the SPA; there is no CORS allowance and no JWT.

Production forces HTTPS, secure session/CSRF cookies, HSTS, explicit hosts, and explicit HTTPS CSRF origins. Review/staging also use secure cookies. Email is returned by authenticated self endpoints only, not by any anonymous/public endpoint.

Every auth response is marked `Cache-Control: no-store`, including responses containing private email or a newly issued native credential.

The Vite development server proxies `/api` to the configured local Django origin so browser semantics remain same-origin. Production must route the built Web client and `/api` on the same origin; no CORS middleware or wildcard is part of M1.3.

## Native contract

Native login/signup creates a 256-bit random opaque bearer credential. PostgreSQL stores only its SHA-256 digest, owning user, creation/last-use time, expiry (30 days), and revocation time. It is not a JWT and contains no claims. Every authenticated request rechecks server-side expiry, revocation, and user-active state. Native logout revokes the row before the client removes its credential; password reset revokes every active native session. Bearer requests do not use CSRF because the secret is supplied explicitly in `Authorization`, not ambiently by the browser.

The raw credential is persisted only with Expo SecureStore using `WHEN_UNLOCKED_THIS_DEVICE_ONLY` on iOS and the Android Keystore-backed implementation. It is never placed in AsyncStorage, logs, analytics, or source. App startup restores it, validates it against `/me/`, and erases it when invalid/expired/revoked. Device/simulator and backup-transfer behavior remain unverified until native build testing.

M1.3 has no refresh token or silent rotation protocol: a fresh login issues a new independent credential, current-session logout revokes it before local deletion, reset revokes all of the user's native credentials, and expiry requires login again. If revocation cannot reach the server, the app retains the secure credential and asks the user to reconnect instead of presenting a false successful logout. This keeps the lifecycle small and server-revocable; refresh/rotation must not be added without a separately reviewed threat model.

## Verification and reset

`EmailActionToken` supports exactly `VERIFY_EMAIL` and `RESET_PASSWORD`. Secrets are generated with `secrets.token_urlsafe(32)`; only SHA-256 digests are durable. Tokens expire after one hour, are single-use, purpose-bound, transactionally consumed, and rotated by invalidating the prior unused token for that user/purpose. A partial unique database constraint permits only one active token per purpose/user. Reset requests and verification resend responses are generic where identity existence is security-sensitive.

Delivery uses Django's provider-neutral email backend behind Celery tasks. Reset/resend enqueues an identical operation for existing and missing accounts so provider latency cannot become an HTTP timing oracle; only an internal numeric/sentinel ID reaches the broker, with redacted task argument representation. Local defaults to console and automated tests use eager/in-memory delivery. SendGrid is not configured or verified. Production provider selection remains a later bounded integration; secrets and message bodies must not enter structured application logs.

## Authorization and abuse controls

DRF authenticates the same `User` through native bearer or Django session. Reusable server-side primitives establish anonymous, authenticated, admin/staff, owner, and owner-or-staff boundaries. Free/Plus, sponsor, and moderation permissions intentionally wait for their owning domains; later clients may hide controls but the server must enforce every boundary.

Redis/compatible KVS counters limit auth operations by both source IP and normalized identity digest; KVS is not identity authority. Current defaults cover login, native session exchange, signup, verification resend, and reset request. Invalid login and reset responses do not reveal whether an account exists. Rate keys contain digests, not raw email/IP.

## Endpoint summary

- Browser: CSRF, signup, login/logout, session lookup, `/me`, verification request/confirm, reset request/confirm.
- Native: signup, session issue/revoke, reset request; `/me`, verification confirmation, and final reset confirmation use the shared authenticated/link contracts.
- Native verification/reset links intentionally open the same HTTPS Web completion flow so secrets are not claimed via an unverified deep-link association in M1.3.
