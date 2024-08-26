from django.contrib import admin
from .models import Booking, RatingType, GuestViewRating, Score, GuestReview

# Register your models here.
admin.site.register(Booking)
admin.site.register(RatingType)
admin.site.register(GuestViewRating)
admin.site.register(Score)
admin.site.register(GuestReview)