from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """Класс для доступа для админа или владельца записи."""

    def has_object_permission(self, request, view, obj):
        """Получить доступ на объект."""
        if request.user.is_staff or request.user.is_superuser:
            return True

        owner = getattr(obj, 'user')

        return owner == request.user
