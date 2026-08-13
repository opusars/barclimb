# M1.1 Environment and Setup

## Runtime baseline

- Python 3.13.15 for production/development parity; Django 5.2.17 LTS and DRF 3.16.1.
- Node 24.19.0 LTS; its bundled npm 11.17.0.
- React and ReactDOM 19.2.3 for web, resolved as one runtime.
- Expo SDK 57.0.12 with React 19.2.3 and React Native 0.86.2. TypeScript remains on the controlling 5.x line at 5.9.3; Expo's supported dependency exclusion prevents `expo install --fix` from replacing it with the template-recommended TypeScript 6 line.
- PostgreSQL is required for real local, staging, and production environments.
- SQLite in-memory is permitted only for the isolated foundation unit tests in M1.1. Database-sensitive integration tests must use PostgreSQL when introduced.

## Setup

```bash
cp .env.example .env
pyenv install 3.13.15 # omit when already installed
pyenv local 3.13.15
python -m venv .venv
. .venv/bin/activate
nvm install 24.19.0 # omit when already installed
nvm use
python -m pip install --require-hashes -r apps/backend/requirements-dev.txt
npm ci
```

`.python-version`, `.nvmrc`, root `engines`, `packageManager`, and CI encode the same baseline. `pyenv`/`nvm` are the documented cross-platform version-manager path; equivalent managers may be used if they select the exact versions.

## Python dependency locking

`requirements.in` and `requirements-dev.in` are the small, human-maintained inputs. `requirements.txt` and `requirements-dev.txt` are complete, hash-verified locks generated with pip-tools. To update deliberately under Python 3.13.15:

```bash
python -m pip install pip-tools==7.6.1
cd apps/backend
python -m piptools compile --generate-hashes --strip-extras --resolver=backtracking --output-file=requirements.txt requirements.in
python -m piptools compile --generate-hashes --strip-extras --resolver=backtracking --output-file=requirements-dev.txt requirements-dev.in
```

Review both generated diffs and install with `--require-hashes`. Add future dependencies to the `.in` files, never directly to the lock outputs.

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
npm run portability
npm run doctor --workspace @barclimb/native
```

CI also runs migrations, system checks, health, and readiness tests against PostgreSQL. The default local test settings retain in-memory SQLite only for fast framework-foundation tests; use `config.settings.postgres_test` with `DATABASE_URL` for database-sensitive work.

Never commit `.env`, credentials, signing material, or provider secrets.
