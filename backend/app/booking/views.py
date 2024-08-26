from datetime import datetime

from django.db.models import Q
from rest_framework import permissions
from rest_framework import status as http_status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView

from api.models import Role
from .models import Booking, GuestReview
from .permissions import StatusPermission
from .serializers import BookingWriteSerializer, BookingReadSerializer, GuestReviewReadSerializer, \
    GuestReviewWriteSerializer


class BookingListView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookingReadSerializer
        elif self.request.method == "POST":
            return BookingWriteSerializer

    def get_queryset(self):
        if self.request.user.roles.filter(name=Role.ADMIN).exists():
            _query_set = Booking.objects.all()
        elif self.request.user.roles.filter(name=Role.HOTEL_MANAGER).exists():
            _query_set = Booking.objects.filter(rooms__hotel_id__owners=self.request.user).distinct()
        else:
            _query_set = Booking.objects.filter(guest_id=self.request.user)

        # Support filter
        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        guest_ids = self.request.query_params.get('creation_guest', None)
        status = self.request.query_params.get('status', None)

        if (from_date is None and to_date) or (from_date and to_date is None):
            raise ValidationError(detail={"error": "Both 'from' and 'to' parameters are required"},
                                  code=http_status.HTTP_400_BAD_REQUEST)

        if status and status != "ALL":
            if status not in [choice[0] for choice in Booking.BookingStatus.choices]:
                raise ValidationError(detail={"error": "Invalid 'status' parameter"},
                                      code=status.HTTP_400_BAD_REQUEST)
            _query_set = _query_set.filter(status=status)

        if from_date and to_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
            _query_set = _query_set.filter(check_in_date__gte=from_date, check_out_date__lte=to_date)

        if guest_ids:
            guest_id_list = guest_ids.split(',')
            _query_set = _query_set.filter(guest_id__in=guest_id_list)

        return _query_set


class BookingDetailView(RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, StatusPermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BookingReadSerializer
        else:
            return BookingWriteSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if self.request.user.roles.filter(name__in=[Role.HOTEL_MANAGER, Role.ADMIN]).exists():
            return Booking.objects.filter(pk=pk)
        elif self.request.user.roles.filter(name=Role.GUEST).exists():
            return Booking.objects.filter(Q(guest_id=self.request.user) &
                                          Q(pk=pk))


class ReviewListView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        booking_id = self.kwargs.get('pk')
        return GuestReview.objects.filter(
            Q(booking_id__guest_id=self.request.user) &
            Q(booking_id=booking_id))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GuestReviewReadSerializer
        else:
            return GuestReviewWriteSerializer


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        booking_id = self.kwargs.get('booking_id')
        pk = self.kwargs.get('pk')
        return GuestReview.objects.filter(
            Q(booking_id__guest_id=self.request.user) &
            Q(booking_id=booking_id) &
            Q(pk=pk))

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GuestReviewReadSerializer
        else:
            return GuestReviewWriteSerializer
