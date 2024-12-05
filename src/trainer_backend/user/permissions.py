from rest_framework.permissions import BasePermission


class IsEmailVerified(BasePermission):
    """Пользователь с подтверждённым email."""

    def has_permission(self, request, view):
        """Email подтверждён."""
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.is_email_verified
