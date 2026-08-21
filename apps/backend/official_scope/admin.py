from django.contrib import admin

from .models import (
    OfficialScopeItem,
    OfficialScopeSource,
    OfficialScopeVersion,
    OfficialSourceArtifact,
)


class ImmutableAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OfficialSourceArtifact)
class OfficialSourceArtifactAdmin(ImmutableAdmin):
    list_display = (
        "stable_id",
        "source_version",
        "source_authority",
        "artifact_type",
        "status",
        "has_been_superseded",
        "content_sha256",
    )
    search_fields = ("stable_id", "official_title", "content_sha256")


@admin.register(OfficialScopeVersion)
class OfficialScopeVersionAdmin(ImmutableAdmin):
    list_display = (
        "version_identifier",
        "exam_program",
        "exam_component",
        "status",
        "normalized_sha256",
    )


@admin.register(OfficialScopeItem)
class OfficialScopeItemAdmin(ImmutableAdmin):
    list_display = ("stable_id", "scope_version", "official_label", "is_leaf", "perimeter")
    list_filter = ("scope_version", "is_leaf", "perimeter")


@admin.register(OfficialScopeSource)
class OfficialScopeSourceAdmin(ImmutableAdmin):
    list_display = ("scope_version", "artifact", "role", "ordering")
