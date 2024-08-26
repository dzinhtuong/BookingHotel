from rest_framework import permissions

from api.models import Role

"""
After creating this, add IsOwnerOrReadOnly to permissions_classes in the SnippetDetail view class.
"""


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return True if request.method in permissions.SAFE_METHODS else False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.guest_id == request.user


class GuestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True if request.user.roles.filter(name=Role.GUEST).exists() else False


class HotelManagerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return True if request.user.roles.filter(name=Role.HOTEL_MANAGER).exists() else False


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return True if request.user.roles.filter(name=Role.ADMIN).exists() else False
