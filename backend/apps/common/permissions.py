"""Shared permission and role helpers."""

from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    """Allow access only to users with one of the view-defined roles."""

    ROLE_ALIASES = {
        "patient": "guest",
        "receptionist": "front_desk",
        "doctor": "manager",
        "nurse": "housekeeping",
    }

    def has_permission(self, request, view):
        allowed_roles = getattr(view, "allowed_roles", None)
        current_role = getattr(request.user, "role", None)
        normalized_role = self.ROLE_ALIASES.get(current_role, current_role)
        if not allowed_roles:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and normalized_role in allowed_roles
