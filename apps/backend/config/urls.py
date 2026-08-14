from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("health.urls")),
    path("api/v1/auth/", include("accounts.urls")),
]
