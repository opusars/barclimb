# M1.2 Deployment Foundation

No environment has been deployed or provider-verified in M1.2. This document defines the contract a later Heroku pipeline must implement.

## Heroku pipeline shape

- Review apps: disposable, built from pull-request branches, `APP_ENV=review`, `config.settings.review`; never assume data survives rebuild/destruction.
- Staging: persistent near-production app, `APP_ENV=staging`, `config.settings.staging`; later real non-production OpenAI, Stripe, SendGrid, S3, Sentry, consent, sponsor, and store-service verification belongs here.
- Production: persistent production app, `APP_ENV=production`, `config.settings.production`; production credentials are never copied to review/staging.

Each deployed app needs attached PostgreSQL and Redis/Valkey-compatible managed KVS services. Provider/plan selection and provisioning remain unverified. PostgreSQL is durable authority; KVS is disposable coordination/cache state.

The root `Procfile` defines `web`, `worker`, and `release`. The release phase runs Django's deployment checks before migrations. A failed check/migration blocks the release. There is no beat dyno because no scheduled work exists.

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
- `PUBLIC_BASE_URL` (HTTPS)
- `READINESS_REQUIRE_KVS=true`
- `LOG_LEVEL`
- web/native public API base variables at client build time as applicable
- production-grade provider-neutral Django `EMAIL_BACKEND` and `DEFAULT_FROM_EMAIL` before transactional-email verification

Do not add provider credentials before the corresponding integration slice. Deployed settings fail closed on missing/malformed mandatory runtime values and reject mismatched `APP_ENV`.

## Operational contract

- Heroku routes web traffic only to ready web processes according to the eventual platform health-check configuration.
- Scale at least one worker when asynchronous features are introduced; M1.2 proves the process can start and consume a smoke task.
- Logs go to stdout/stderr as structured JSON and must be forwarded later without learner-response or secret content.
- Database migrations remain forward-safe; code rollback must not assume schema rollback.
- Review-app data is disposable. Staging database/object retention and backup procedures must be defined and tested before provider-backed feature verification. Production backup/recovery remains a launch gate.

Deployment, custom domains, SSL, pipelines, add-ons, scaling, backups, rollback drills, and provider connectivity are all explicitly unverified in M1.2.

M1.3 adds secure-cookie/HSTS enforcement and the identity schema but does not verify a deployed email provider, Heroku runtime, universal/app links, or native device keychain behavior. Console email is local-only and must not be used as production delivery.
