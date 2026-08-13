# M1.1 Environment and Setup

## Runtime baseline

- Python 3.13.x for production/development parity; Django 5.2.16 LTS and DRF 3.16.1.
- Node 22.13.x LTS-compatible baseline; npm 10.9.0.
- React 19.2 for web.
- Expo SDK 55 with its supported React 19.2 and React Native 0.83 pairing. SDK 57 was not selected because its required TypeScript 6 line conflicts with the controlling TypeScript 5.x kickoff baseline.
- PostgreSQL is required for real local, staging, and production environments.
- SQLite in-memory is permitted only for the isolated foundation unit tests in M1.1. Database-sensitive integration tests must use PostgreSQL when introduced.

## Setup

```bash
cp .env.example .env
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r apps/backend/requirements-dev.txt
npm ci
```

Create the local PostgreSQL database described by `DATABASE_URL`, then run:

```bash
cd apps/backend
python manage.py migrate
python manage.py runserver
```

From the repository root, `npm run web:dev` starts the web shell and `npm run native:start` starts Expo.

## Checks

```bash
python3 scripts/validate_continuity.py
cd apps/backend && ruff check . && python manage.py check --settings=config.settings.test && pytest
npm run check
npm run doctor --workspace @barclimb/native
```

Never commit `.env`, credentials, signing material, or provider secrets.
