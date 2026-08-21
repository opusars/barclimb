from django.contrib import admin
from django.urls import include, path, re_path

from config.mobile_association import android_asset_links, apple_app_site_association
from config.web import web_asset, web_index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("health.urls")),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/official-scope/", include("official_scope.urls")),
    path(".well-known/apple-app-site-association", apple_app_site_association),
    path(".well-known/assetlinks.json", android_asset_links),
    path("assets/<path:asset_path>", web_asset),
    re_path(r"^(?:login|signup|verify-email|forgot-password|reset-password|app)/?$", web_index),
    path("", web_index),
]
