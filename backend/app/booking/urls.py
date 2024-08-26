from django.urls import path

from .views import BookingDetailView, BookingListView, ReviewDetailView, ReviewListView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking list or create for particular guest'),
    path('<int:pk>', BookingDetailView.as_view(), name='booking detail'),
    path('<int:pk>/reviews', ReviewListView.as_view(), name='booking review'),
    path('<int:booking_id>/reviews/<int:pk>', ReviewDetailView.as_view(), name='booking'),
]