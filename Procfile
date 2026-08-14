web: gunicorn --chdir apps/backend config.wsgi --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
worker: celery --workdir apps/backend -A config worker --loglevel=INFO
release: python apps/backend/manage.py check --deploy && python apps/backend/manage.py migrate --noinput
