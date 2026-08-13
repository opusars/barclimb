from django.urls import path

from .views import health, readiness

urlpatterns = [path("health/", health), path("ready/", readiness)]
