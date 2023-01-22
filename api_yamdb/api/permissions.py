from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Изменение контента доступно только Админу"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser)
        )


class AnonimReadOnly(permissions.BasePermission):
    """Анонимный пользователь может отправлять только безопасные запросы."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperUserOrIsAdminOnly(permissions.BasePermission):
    """
    Предоставляются права на осуществление запросов
    только суперпользователю, админу или
    аутентифицированному пользователю с ролью admin.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_staff
                 or request.user.is_superuser)
        )


class SuperUserOrAdminOrModeratorOrAuthor(permissions.BasePermission):
    """
    Предоставляется доступ к PATCH и DELETE только
    суперпользователю, админу, аутентифицированному
    пользователю с ролью admin или moderator, а также
    автору объекта.
    """
    def has_permission(self, request):
        return request.user.is_authenticated

    def has_object_permission(self, request, obj):
        return (request.user.is_superuser
                or request.user.is_staff
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author)


class AuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return ((request.method in permissions.SAFE_METHODS)
                or (obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin))
