from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """Класс доступа для преподавателя."""

    def has_permission(self, request, view):
        return request.user.is_teacher