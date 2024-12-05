from rest_framework.permissions import BasePermission


class OR(BasePermission):
    """Класс для дизъюнкции разрешений."""

    def __init__(self, *permissions):
        self.permissions = permissions

    def has_permission(self, request, view):
        """Проверка разрешения."""
        return any(
            permission().has_permission(request, view)
            for permission in self.permissions
        )

    def has_object_permission(self, request, view, obj):
        """Проверка разрешения для объекта."""
        return any(
            permission().has_object_permission(request, view, obj)
            for permission in self.permissions
        )
