from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role and request.user.role.name == 'admin'
