from rest_framework import permissions

class AnonimReadOnly(permissions.BasePermission):
    """Анонимный пользователь может отправлять только безопасные запросы"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
        