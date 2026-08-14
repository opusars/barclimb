from celery import shared_task


@shared_task(name="infrastructure.smoke", ignore_result=True)
def infrastructure_smoke() -> dict[str, str]:
    """Prove task discovery/execution; this is not an application or stability contract."""

    return {"status": "ok", "scope": "infrastructure-only"}
