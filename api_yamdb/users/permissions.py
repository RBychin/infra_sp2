from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdminUser(permissions.BasePermission):
    """Доступ разрешен Администратору."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == User.ADMIN
                     or request.user.is_superuser))
