import pytest
from django.core.cache import cache


@pytest.mark.django_db
def test_health_endpoint(client):
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "barclimb-api"}


@pytest.mark.django_db
def test_readiness_checks_required_dependencies(client, settings):
    response = client.get("/api/v1/ready/")
    assert response.status_code == 200
    dependencies = {"database": "ok"}
    if settings.READINESS_REQUIRE_KVS:
        dependencies["kvs"] = "ok"
    assert response.json() == {"status": "ready", "dependencies": dependencies}


def test_celery_discovers_and_executes_infrastructure_smoke_task(settings):
    from config.celery import app

    app.loader.import_default_modules()
    result = app.tasks["infrastructure.smoke"].delay()

    assert settings.CELERY_TASK_ALWAYS_EAGER is True
    assert result.get() == {"status": "ok", "scope": "infrastructure-only"}


@pytest.mark.django_db
def test_readiness_fails_when_required_kvs_is_unavailable(client, monkeypatch, settings):
    settings.READINESS_REQUIRE_KVS = True

    def unavailable(*_args, **_kwargs):
        raise ConnectionError("test KVS unavailable")

    monkeypatch.setattr(cache, "set", unavailable)
    response = client.get("/api/v1/ready/")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "dependencies": {"database": "ok", "kvs": "unavailable"},
    }
