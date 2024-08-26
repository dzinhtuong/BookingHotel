from django.urls import path

from .views import HotelDetailView, HotelListView, HotelRoomListView, RoomDetailView, RoomListView, RoomTypeListView, \
    FeatureListView, ClassifyFeatureDetailView, ClassifyFeatureListView, FeatureDetailView, RoomTypeDetailView, \
    BedTypeListView, BedTypeDetailView

urlpatterns = [
    # For Hotel Manager

    path('<int:pk>', HotelDetailView.as_view(), name='hotel detail'),
    path('<int:pk>/room', HotelRoomListView.as_view(), name='list of room in particular hotel'),
    path('<int:hotel_id>/room/<int:pk>', RoomDetailView.as_view(), name='room detail'),
    path('<int:pk>/roomtype', RoomTypeListView.as_view(), name='list of room types in particular hotel'),
    path('<int:hotel_id>/roomtype/<int:pk>', RoomTypeDetailView.as_view(), name='room type detail'),

    # For Administrator
    path('', HotelListView.as_view(), name='hotel list'),
    path('room', RoomListView.as_view(), name='list of rooms'),
    path('feature', FeatureListView.as_view(), name='list of features'),
    path('feature/<int:pk>', FeatureDetailView.as_view(), name='feature detail'),
    path('classifyfeature', ClassifyFeatureListView.as_view(), name='list of classify feature'),
    path('classifyfeature/<int:pk>', ClassifyFeatureDetailView.as_view(), name='Classify feature detail'),
    path('bedtype', BedTypeListView.as_view(), name='list of bed type'),
    path('bedtype/<int:pk>', BedTypeDetailView.as_view(), name='Bed type detail')
]