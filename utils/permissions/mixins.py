from rest_framework import permissions


class IsStaffOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # General user is prohibited
        if not user.is_authenticated:
            return False
                
        # Allow staff or admin users only
        if user.is_staff or user.is_superuser:
            return True
        return False


class StaffOrAdminViewSetMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsStaffOrAdminPermission()]
        return [permissions.AllowAny()]