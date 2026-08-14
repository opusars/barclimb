from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated


class IsResourceOwner(BasePermission):
    """Foundation object permission for future user-owned resources."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "owner", getattr(obj, "user", None))
        return owner == request.user


class IsResourceOwnerOrStaff(IsResourceOwner):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or super().has_object_permission(request, view, obj)


__all__ = ("IsAdminUser", "IsAuthenticated", "IsResourceOwner", "IsResourceOwnerOrStaff")
