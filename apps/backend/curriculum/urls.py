from django.urls import path

from .views import CertifiedCurriculumView

urlpatterns = [path("certified/", CertifiedCurriculumView.as_view(), name="certified-curriculum")]
