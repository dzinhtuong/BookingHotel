from django.contrib.auth.models import User
from django.db import models

from hotel.models import Hotel, Room


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        APPROVED = "APPROVED", "APPROVED"
        REJECTED = "REJECTED", "REJECTED"
        CANCELLED = "CANCELLED", "CANCELLED"

    rooms = models.ManyToManyField(Room)
    guest_id = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    numbers_of_adults = models.IntegerField(default=2)
    numbers_of_children = models.IntegerField(default=0)
    total_rooms = models.IntegerField(default=1)
    addition = models.TextField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    status = models.CharField(max_length=100, choices=BookingStatus.choices, default=BookingStatus.PENDING)


class GuestReview(models.Model):
    booking_id = models.OneToOneField(Booking, on_delete=models.CASCADE)
    comment = models.TextField()


class RatingType(models.Model):
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class Score(models.Model):
    quality = models.IntegerField()

    def __str__(self):
        return str(self.quality)


class GuestViewRating(models.Model):
    guest_review_id = models.ForeignKey(GuestReview, on_delete=models.CASCADE)
    rating_type_id = models.ForeignKey(RatingType, on_delete=models.CASCADE)
    score_id = models.ForeignKey(Score, on_delete=models.CASCADE)