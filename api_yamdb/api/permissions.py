from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ разрешен только автору объекта."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ разрешен Администратору."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == User.ADMIN
                    or request.user.is_superuser)))

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsModeratorOrReadOnly(permissions.BasePermission):
    """Доступ разрешен Модератору."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == User.MODERATOR)


class IsUserOrReadOnly(permissions.BasePermission):
    """Доступ разрешен Пользователю (user)."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == User.USER)
