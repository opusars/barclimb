from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OfficialScopeVersion
from .serializers import ActiveScopeSerializer


class ActiveScopeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filters = {
            "exam_program": OfficialScopeVersion.EXAM_PROGRAM,
            "exam_component": OfficialScopeVersion.EXAM_COMPONENT,
            "status": OfficialScopeVersion.Status.ACTIVE,
        }
        if not settings.OFFICIAL_SCOPE_ALLOW_TEST_FIXTURE_API:
            filters["is_test_fixture"] = False
        scope = OfficialScopeVersion.objects.filter(**filters).prefetch_related("items").first()
        if scope is None:
            return Response({"detail": "No active official scope."}, status=404)
        return Response(ActiveScopeSerializer(scope).data)
