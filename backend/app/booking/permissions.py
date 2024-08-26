from rest_framework import permissions
from api.models import Role
from booking.models import Booking

"""
After creating this, add IsOwnerOrReadOnly to permissions_classes in the SnippetDetail view class.
"""


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


class StatusPermission(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.data.get('status'):

            if obj.status == Booking.BookingStatus.APPROVED.name:
                return False

            if request.user.roles.filter(name__in=[Role.HOTEL_MANAGER, Role.ADMIN]).exists():
                return True if request.data.get('status') in (Booking.BookingStatus.APPROVED.name,
                                                              Booking.BookingStatus.REJECTED.name) else False

            elif request.user.roles.filter(name=Role.GUEST).exists():
                return True if request.data.get('status') in (Booking.BookingStatus.CANCELLED.name) else False

        return True
