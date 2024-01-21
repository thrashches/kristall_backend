from rest_framework import permissions


class IsOrderOwner(permissions.BasePermission):
    """
    Являестя ли пользователь владельцем заказа
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user and request.user.is_authenticated) and obj.user == request.user
