from rest_framework import serializers

from .models import OfficialScopeItem, OfficialScopeSource, OfficialScopeVersion


class ScopeItemSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(source="parent.stable_id", allow_null=True)
    source_artifact_id = serializers.CharField(source="source_artifact.stable_id")

    class Meta:
        model = OfficialScopeItem
        fields = (
            "stable_id",
            "parent_id",
            "official_label",
            "official_text",
            "ordering",
            "perimeter",
            "subject_group",
            "is_leaf",
            "source_artifact_id",
            "source_locator",
            "treatment_metadata",
            "knowledge_treatment",
            "normalization_status",
            "normalization_notes",
        )


class ScopeSourceSerializer(serializers.ModelSerializer):
    stable_id = serializers.CharField(source="artifact.stable_id")
    source_authority = serializers.CharField(source="artifact.source_authority")
    artifact_type = serializers.CharField(source="artifact.artifact_type")
    official_title = serializers.CharField(source="artifact.official_title")
    source_uri = serializers.CharField(source="artifact.source_uri")
    source_version = serializers.CharField(source="artifact.source_version")
    status = serializers.CharField(source="artifact.status")
    content_sha256 = serializers.CharField(source="artifact.content_sha256")
    media_type = serializers.CharField(source="artifact.media_type")
    storage_disposition = serializers.CharField(source="artifact.storage_disposition")
    publication_date = serializers.DateField(source="artifact.publication_date")
    effective_date = serializers.DateField(source="artifact.effective_date")
    effective_end_date = serializers.DateField(source="artifact.effective_end_date")
    retrieved_at = serializers.DateTimeField(source="artifact.retrieved_at")

    class Meta:
        model = OfficialScopeSource
        fields = (
            "stable_id",
            "source_authority",
            "artifact_type",
            "official_title",
            "source_uri",
            "source_version",
            "status",
            "content_sha256",
            "media_type",
            "storage_disposition",
            "publication_date",
            "effective_date",
            "effective_end_date",
            "retrieved_at",
            "role",
        )


class ActiveScopeSerializer(serializers.ModelSerializer):
    sources = serializers.SerializerMethodField()
    items = ScopeItemSerializer(many=True)

    class Meta:
        model = OfficialScopeVersion
        fields = (
            "exam_program",
            "exam_component",
            "version_identifier",
            "normalized_sha256",
            "administration_start",
            "administration_end",
            "release_class",
            "sources",
            "items",
        )

    def get_sources(self, obj):
        links = OfficialScopeSource.objects.filter(scope_version=obj).select_related("artifact")
        return ScopeSourceSerializer(links, many=True).data
