from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.utils import DatabaseError
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(_request):
    return Response({"status": "ok", "service": "barclimb-api"})


@api_view(["GET"])
def readiness(_request):
    dependencies = {"database": "ok"}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        dependencies["database"] = "unavailable"

    if settings.READINESS_REQUIRE_KVS:
        try:
            cache.set("runtime-readiness", "ok", timeout=5)
            if cache.get("runtime-readiness") != "ok":
                raise RuntimeError("KVS round trip failed")
            dependencies["kvs"] = "ok"
        except Exception:  # Cache clients expose backend-specific connection errors.
            dependencies["kvs"] = "unavailable"

    ready = all(status == "ok" for status in dependencies.values())
    return Response(
        {"status": "ready" if ready else "not_ready", "dependencies": dependencies},
        status=200 if ready else 503,
    )
