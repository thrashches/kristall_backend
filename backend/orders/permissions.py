from rest_framework import permissions


class IsOrderOwner(permissions.BasePermission):
    """
    Являестя ли пользователь владельцем заказа
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
