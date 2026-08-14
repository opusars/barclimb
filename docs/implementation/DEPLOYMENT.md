# M1.2 Deployment Foundation

No environment has been deployed or provider-verified in M1.2. This document defines the contract a later Heroku pipeline must implement.

## Heroku pipeline shape

- Review apps: disposable, built from pull-request branches, `APP_ENV=review`, `config.settings.review`; never assume data survives rebuild/destruction.
- Staging: persistent near-production app, `APP_ENV=staging`, `config.settings.staging`; later real non-production OpenAI, Stripe, SendGrid, S3, Sentry, consent, sponsor, and store-service verification belongs here.
- Production: persistent production app, `APP_ENV=production`, `config.settings.production`; production credentials are never copied to review/staging.

Each deployed app needs attached PostgreSQL and Redis/Valkey-compatible managed KVS services. Provider/plan selection and provisioning remain unverified. PostgreSQL is durable authority; KVS is disposable coordination/cache state.

The root `Procfile` defines `web`, `worker`, `beat`, and `release`. The release phase runs Django's deployment checks before migrations. A failed check/migration blocks the release. M1.3a's beat process is required when authentication email is enabled; its only current schedule is the one-minute PostgreSQL outbox recovery sweep.

## Required deployment configuration

Set all values explicitly:

- `APP_ENV`
- `DJANGO_SETTINGS_MODULE`
- `DJANGO_SECRET_KEY` (random, 50+ characters)
- `DJANGO_DEBUG=false`
- `DATABASE_URL`
- `REDIS_URL`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS` (HTTPS)
- `PUBLIC_BASE_URL` (HTTPS canonical Web origin for completion links, not an API-only origin)
- `READINESS_REQUIRE_KVS=true`
- `LOG_LEVEL`
- `VITE_API_BASE_URL` for the local Vite proxy and `EXPO_PUBLIC_API_BASE_URL` for native API calls at client build time, as applicable
- production-grade provider-neutral Django `EMAIL_BACKEND` and `DEFAULT_FROM_EMAIL` before transactional-email verification

Do not add provider credentials before the corresponding integration slice. Deployed settings fail closed on missing/malformed mandatory runtime values and reject mismatched `APP_ENV`.

## Operational contract

- Heroku routes web traffic only to ready web processes according to the eventual platform health-check configuration.
- Scale at least one worker and one beat process when authentication email is enabled. Broker recovery is reconciled from durable PostgreSQL outbox rows; `python apps/backend/manage.py replay_auth_email_outbox` is the manual incident command.
- Review, staging, and production redirect direct HTTP to HTTPS and trust `X-Forwarded-Proto`/the rightmost router-appended `X-Forwarded-For` only at the Heroku boundary. Do not expose those trust settings behind an untrusted direct proxy path.
- Logs go to stdout/stderr as structured JSON and must be forwarded later without learner-response or secret content.
- Database migrations remain forward-safe; code rollback must not assume schema rollback.
- Review-app data is disposable. Staging database/object retention and backup procedures must be defined and tested before provider-backed feature verification. Production backup/recovery remains a launch gate.

Deployment, custom domains, SSL, pipelines, add-ons, scaling, backups, rollback drills, and provider connectivity are all explicitly unverified in M1.2.

M1.3a adds HTTPS enforcement in every deployed auth environment, the explicit Heroku proxy/IP contract, and durable provider-neutral email delivery state. It does not verify a deployed email provider, Heroku runtime, universal/app links, or native device keychain behavior. Console email is local-only and must not be used as production delivery.
