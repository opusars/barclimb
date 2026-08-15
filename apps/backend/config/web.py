import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponseNotAllowed


def web_index(request):
    if request.method not in {"GET", "HEAD"}:
        return HttpResponseNotAllowed(["GET", "HEAD"])
    return _file(Path(settings.WEB_DIST_DIR) / "index.html", cache="no-cache")


def web_asset(request, asset_path):
    root = (Path(settings.WEB_DIST_DIR) / "assets").resolve()
    requested = (root / asset_path).resolve()
    if root not in requested.parents:
        raise Http404
    return _file(requested, cache="public, max-age=31536000, immutable")


def _file(path, cache):
    if not path.is_file():
        raise Http404
    response = FileResponse(path.open("rb"), content_type=mimetypes.guess_type(path.name)[0])
    response["Cache-Control"] = cache
    return response
