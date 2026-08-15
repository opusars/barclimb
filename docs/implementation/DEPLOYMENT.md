# M1.4 Staging Deployment Contract

M1.4 provisions the first persistent non-production Heroku staging topology. Evidence and current provider state belong in `docs/project/PROVIDER_STATUS.md` and `TEST_LEDGER.md`; this file defines its reproducible contract.

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
- `VITE_APP_ENV`; deployed Web must not set an alternate `VITE_API_BASE_URL`
- `EXPO_PUBLIC_APP_ENV`, `EXPO_PUBLIC_API_BASE_URL`, and `EXPO_PUBLIC_WEB_BASE_URL` for native builds
- `MOBILE_LINKS_ENABLED=false` until real signing identifiers and association evidence exist
- `EMAIL_BACKEND` and `DEFAULT_FROM_EMAIL`; staging may explicitly use the non-delivering `config.email_backends.StagingAuthEmailSink` with `ALLOW_STAGING_AUTH_EMAIL_SINK=true`, while production cannot

Do not add provider credentials before the corresponding integration slice. Deployed settings fail closed on missing/malformed mandatory runtime values and reject mismatched `APP_ENV`.

## Operational contract

- Heroku routes web traffic only to ready web processes according to the eventual platform health-check configuration.
- Scale at least one worker and one beat process when authentication email is enabled. Broker recovery is reconciled from durable PostgreSQL outbox rows; `python apps/backend/manage.py replay_auth_email_outbox` is the manual incident command.
- Review, staging, and production redirect direct HTTP to HTTPS and trust `X-Forwarded-Proto`/the rightmost router-appended `X-Forwarded-For` only at the Heroku boundary. Do not expose those trust settings behind an untrusted direct proxy path.
- Logs go to stdout/stderr as structured JSON and must be forwarded later without learner-response or secret content.
- Database migrations remain forward-safe; code rollback must not assume schema rollback.
- Review-app data is disposable. Staging database/object retention and backup procedures must be defined and tested before provider-backed feature verification. Production backup/recovery remains a launch gate.

The root `requirements.txt` delegates to the hash-locked backend requirements for Heroku Python detection. Heroku buildpacks run Node before Python; `heroku-postbuild` creates the Web distribution consumed by Django. Staging uses a distinct app, database, KVS, secret, public origins, and app identifiers. It never receives production credentials.

Custom domains, production deployment, backups, rollback drills, and real email-provider delivery remain separate gates. Console email is local-only and the staging sink must never become production delivery.
