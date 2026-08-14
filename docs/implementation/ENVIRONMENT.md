# M1.2 Runtime and Environment Contract

## Runtime baseline

- Python 3.13.15, Django 5.2.17, DRF 3.16.1, Celery 5.6.3.
- Node 24.19.0/npm 11.17.0; web/native versions remain as documented in `ARCHITECTURE.md`.
- PostgreSQL is the canonical durable datastore in every real environment.
- A Redis/Valkey-compatible service is the ephemeral KVS, Celery broker, and Django cache.

The application does not use a Celery result backend. Tasks ignore return values by default; durable task outcomes must eventually be written idempotently to PostgreSQL domain records. Global late acknowledgement, reject-on-worker-loss, and implicit autoretry are disabled. A future business task must define its own deterministic idempotency key, bounded retry/backoff policy, and transaction boundary.

KVS may support queue coordination, caching, rate limiting, ephemeral locks, and explicitly short-lived orchestration state. It must never be the only store for learner evidence, submitted answers, grades, assessment/curriculum/publication truth, subscription/entitlement truth, or any other authoritative durable business record.

## Environment contract

| Environment | Settings                                  | Lifetime and provider posture                                                                                                |
| ----------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Local       | `config.settings.local`                   | Developer-owned; PostgreSQL + KVS; provider-independent; no production secrets.                                              |
| Test/CI     | `config.settings.test` or `postgres_test` | Deterministic eager Celery; PostgreSQL path in CI; real KVS connectivity in integration CI; no providers/network.            |
| Review      | `config.settings.review`                  | Disposable production-like app; state may disappear; provider stubs/test modes only.                                         |
| Staging     | `config.settings.staging`                 | Persistent near-production topology; future home of real non-production provider integrations. Never production credentials. |
| Production  | `config.settings.production`              | Explicit fail-closed config; secure cookies/proxy; no development defaults.                                                  |

`APP_ENV` must be exactly `local`, `test`, `review`, `staging`, or `production`. Deployed settings reject an environment mismatch. Review/staging/production require a 50+ character `DJANGO_SECRET_KEY`, PostgreSQL `DATABASE_URL`, Redis/Valkey-compatible `REDIS_URL`, HTTPS `PUBLIC_BASE_URL`, nonempty `ALLOWED_HOSTS`, nonempty HTTPS `CSRF_TRUSTED_ORIGINS`, and `DJANGO_DEBUG=false`. Staging/production database URLs enable TLS. Review apps are equally fail-closed but disposable.

Safe variable names and examples are in `.env.example`. `VITE_API_BASE_URL` supplies only the local Vite `/api` proxy target; deployed Web remains same-origin. `EXPO_PUBLIC_API_BASE_URL` is public native build-time configuration. Neither value is secret storage. Email settings select Django's provider-neutral delivery boundary but do not verify a provider or add provider credentials.

Local identity email uses Django's console backend and tests/review apps use in-memory delivery. Staging/production fail closed unless `EMAIL_BACKEND` names a non-console/non-memory Django backend and `DEFAULT_FROM_EMAIL` is explicit; this selects a provider-neutral boundary without verifying any provider. Native clients require an origin-valued `EXPO_PUBLIC_API_BASE_URL` (a trailing `/api/v1` is tolerated and normalized); only the opaque native session secret is placed in Expo SecureStore.

## Clean-checkout local workflow

Install exact runtimes, then:

```bash
cp .env.example .env
python -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r apps/backend/requirements-dev.txt
npm ci
```

Run PostgreSQL and Redis/Valkey using local package-manager services or standalone processes. Create the `barclimb` database and verify the KVS:

```bash
createdb barclimb
redis-cli -u redis://localhost:6379/0 ping
```

Load `.env` with a trusted environment loader or export its values, then use separate terminals:

```bash
cd apps/backend && python manage.py migrate && python manage.py runserver
cd apps/backend && celery -A config worker --loglevel=INFO
npm run web:dev
npm run native:start
```

Docker is not required. Native PostgreSQL/KVS services keep the foundation simple; teams may use containers if their ports and URLs satisfy the same contract.

## Process and dependency health

The root `Procfile` defines:

- `web`: Gunicorn WSGI server;
- `worker`: Celery worker;
- `release`: deployment checks followed by safe Django migrations using the environment's explicit `DJANGO_SETTINGS_MODULE`.

No beat process exists because M1.2 has no scheduled business work. A future scheduler requires a documented need.

`GET /api/v1/health/` is process liveness and touches no dependencies. `GET /api/v1/ready/` verifies PostgreSQL and, where required, a KVS read/write round trip. Neither endpoint depends on future OpenAI, email, ads, community, or other optional providers. KVS is required because both web cache/runtime coordination and the worker broker depend on it; the endpoint reports dependency categories but never URLs or credentials.

Logs are one-line JSON with timestamp, level, logger, message, `APP_ENV`, and Heroku `DYNO`/local process identity. Do not log configuration values, secrets, learner responses, or business payloads. Sentry remains unverified and unimplemented.

## Verification

```bash
python3 scripts/validate_continuity.py
cd apps/backend && ruff check . && ruff format --check .
cd apps/backend && python manage.py check --settings=config.settings.test && pytest
npm run check
npm run portability
```

CI runs backend checks/migrations/tests against PostgreSQL and a real Redis-compatible service, starts a solo Celery worker, publishes the infrastructure-only smoke task, and confirms execution from worker logs. The smoke task is intentionally not a stable application API.

Never commit `.env`, credentials, signing material, database dumps, KVS snapshots, or provider secrets.
