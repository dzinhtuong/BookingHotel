from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db.models import Q
from api.models import Role
from permissions.permission import HotelManagerPermission, AdminPermission, ReadOnly
from .models import Hotel, Room, RoomType, Feature, ClassificationFeature, BedType
from .serializers import HotelSerializer, RoomTypeWriteSerializer, \
    HotelReadSerializer, RoomReadSerializer, RoomWriteSerializer, \
    RoomDetailWriteSerializer, RoomTypeReadSerializer, RoomTypeDetailWriteSerializer, FeatureReadSerializer, \
    FeatureWriteSerializer, BedTypeWriteSerializer, BedTypeReadSerializer, ClassificationFeatureReadSerializer, \
    ClassificationFeatureWriteSerializer


# Hotel section
class HotelListView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, HotelManagerPermission | AdminPermission)
    queryset = Hotel.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HotelReadSerializer
        elif self.request.method == "POST":
            return HotelSerializer

    def perform_create(self, serializer):
        serializer.save(owners=[self.request.user])

    def get_queryset(self):
        if self.request.user.roles.filter(name=Role.ADMIN).exists():
            return Hotel.objects.all()
        elif self.request.user.roles.filter(name=Role.HOTEL_MANAGER).exists():
            return Hotel.objects.filter(owners=self.request.user)
        else:
            pass


class HotelDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, HotelManagerPermission | AdminPermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return HotelReadSerializer
        else:
            return HotelSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('pk')
        if self.request.user.roles.filter(name=Role.ADMIN).exists():
            return Hotel.objects.filter(id=hotel_id)
        elif self.request.user.roles.filter(name=Role.HOTEL_MANAGER).exists():
            return Hotel.objects.filter(owners=self.request.user,
                                        id=hotel_id)
        else:
            pass


# Room section
class HotelRoomListView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission | HotelManagerPermission)

    def get_queryset(self):
        hotel_id = self.kwargs.get('pk')
        if self.request.user.roles.filter(name=Role.ADMIN).exists():
            return Room.objects.filter(hotel_id=hotel_id)
        elif self.request.user.roles.filter(name=Role.HOTEL_MANAGER).exists():
            _query_set = Room.objects.filter(Q(hotel_id=hotel_id) &
                                             Q(hotel_id__owners=self.request.user))
            return _query_set

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RoomReadSerializer
        else:
            return RoomWriteSerializer


class RoomListView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission)
    queryset = Room.objects.all()
    serializer_class = RoomReadSerializer


class RoomDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission | HotelManagerPermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RoomReadSerializer
        else:
            return RoomDetailWriteSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        room_id = self.kwargs.get('pk')

        if self.request.user.roles.filter(name=Role.ADMIN).exists():
            _query_set = Room.objects.filter(Q(hotel_id=hotel_id) &
                                             Q(pk=room_id))
        elif self.request.user.roles.filter(name=Role.HOTEL_MANAGER).exists():

            _query_set = Room.objects.filter(Q(hotel_id=hotel_id) &
                                             Q(pk=room_id) &
                                             Q(hotel_id__owners=self.request.user))
        return _query_set


class RoomTypeListView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, HotelManagerPermission | AdminPermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RoomTypeReadSerializer
        else:
            return RoomTypeWriteSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('pk')

        if self.request.user.roles.filter(name=Role.ADMIN).exists():
            _query_set = RoomType.objects.filter(Q(hotel_id=hotel_id))

        elif self.request.user.roles.filter(name=Role.HOTEL_MANAGER).exists():

            _query_set = RoomType.objects.filter(Q(hotel_id=hotel_id) &
                                                 Q(hotel_id__owners=self.request.user))

        return _query_set


class RoomTypeDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, HotelManagerPermission | AdminPermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RoomTypeReadSerializer
        else:
            return RoomTypeDetailWriteSerializer

    def get_queryset(self):
        hotel_id = self.kwargs.get('hotel_id')
        room_id = self.kwargs.get('pk')

        if self.request.user.roles.filter(name=Role.ADMIN).exists():
            _query_set = RoomType.objects.filter(Q(hotel_id=hotel_id) &
                                                 Q(pk=room_id))

        elif self.request.user.roles.filter(name=Role.HOTEL_MANAGER).exists():

            _query_set = RoomType.objects.filter(Q(hotel_id=hotel_id) &
                                                 Q(pk=room_id) &
                                                 Q(hotel_id__owners=self.request.user))

        return _query_set


class FeatureListView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission | ReadOnly)
    queryset = Feature.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FeatureReadSerializer
        else:
            return FeatureWriteSerializer


class FeatureDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission | ReadOnly)
    queryset = Feature.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return FeatureReadSerializer
        else:
            return FeatureWriteSerializer


class ClassifyFeatureListView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission | ReadOnly)
    queryset = ClassificationFeature.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClassificationFeatureReadSerializer
        else:
            return ClassificationFeatureWriteSerializer


class ClassifyFeatureDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission | ReadOnly)
    queryset = ClassificationFeature.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ClassificationFeatureReadSerializer
        else:
            return ClassificationFeatureWriteSerializer


class BedTypeListView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission | ReadOnly)
    queryset = BedType.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BedTypeReadSerializer
        else:
            return BedTypeWriteSerializer


class BedTypeDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, AdminPermission | ReadOnly)
    queryset = BedType.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BedTypeReadSerializer
        else:
            return BedTypeWriteSerializer
