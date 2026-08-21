from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CurriculumCompileVersion
from .serializers import CertifiedCurriculumSerializer


class CertifiedCurriculumView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = {"status": CurriculumCompileVersion.Status.CERTIFIED}
        if not settings.CURRICULUM_ALLOW_TEST_FIXTURE_API:
            filters["source_class"] = "PRODUCTION"
        compile_version = (
            CurriculumCompileVersion.objects.filter(**filters)
            .select_related("official_scope_version", "coverage_snapshot")
            .prefetch_related("obligations")
            .order_by("-certified_at")
            .first()
        )
        if compile_version is None:
            return Response({"detail": "No certified curriculum."}, status=404)
        return Response(CertifiedCurriculumSerializer(compile_version).data)
