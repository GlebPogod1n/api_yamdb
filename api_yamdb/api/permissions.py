from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Изменение контента доступно только Админу"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
        )
