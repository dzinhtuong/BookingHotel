from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Hotel(models.Model):
    owners = models.ManyToManyField(User, related_name='hotels', null=True, blank=True)
    name = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)
    website = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100, null=True)
    description = models.TextField(null=False, blank=False)
    image_path = models.CharField(max_length=100, null=False)
    lat_long = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.name}, {self.address}, {self.city}, {self.state}, {self.country}"

    class Meta:
        ordering = ['name']


class RoomType(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False, blank=False)
    base_price = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

    @property
    def total_capacity(self):
        total_capacity = 0
        for bed_type in self.bedtype_set.all():
            total_capacity += bed_type.capacity
        return total_capacity


class Room(models.Model):
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type_id = models.ForeignKey(RoomType, on_delete=models.CASCADE, null=True, blank=True)  # One room has one type
    room_number = models.CharField(max_length=50, null=False)  # Room number maybe A010 or number 100
    floor = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=19, decimal_places=2)  # one billion with a resolution of 2 decimal places
    description = models.TextField(null=False, blank=False)

    def __str__(self):
        return f"{self.hotel_id}, {self.room_type_id}"


class ClassificationFeature(models.Model):
    class_name = models.CharField(max_length=100, null=False)
    description = models.TextField()

    def __str__(self):
        return self.class_name


class Feature(models.Model):
    room_types = models.ManyToManyField(RoomType, blank=True)
    classify_feature_id = models.ForeignKey(ClassificationFeature, on_delete=models.CASCADE)
    value = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.value}"


class BedType(models.Model):
    room_types = models.ManyToManyField(RoomType, blank=True)
    name = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
